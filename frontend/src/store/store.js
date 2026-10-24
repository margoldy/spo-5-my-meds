import * as authApi from '../api/auth'
import * as coursesApi from '../api/courses'
import * as intakesApi from '../api/intakes'
import * as medicationsApi from '../api/medications'
import * as schedulesApi from '../api/schedules'
import * as usersApi from '../api/users'
import {
  createEncryptionKey,
  decryptData,
  encryptData,
  getDeviceKey,
  removeDeviceKey,
  saveDeviceKey,
  unwrapEncryptionKey,
  wrapEncryptionKey,
} from '../utils/crypto'
import { clearTokens, getAccessToken, getRefreshToken, savePreferences, saveTokens } from '../utils/storage'
import { dateInTimeZone, zonedDateTimeToIso } from '../utils/date'
import { scheduleReminders } from '../utils/notifications'
import { state } from './state'

let toastTimer

export function showToast(message) {
  state.toast = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { state.toast = '' }, 2200)
}

export function showError(error) {
  state.error = error?.message || 'Не удалось выполнить действие'
  showToast(state.error)
}

export function go(page) {
  state.previousPage = state.page
  state.page = page
  state.error = ''
}

async function encrypted(value) {
  if (!state.key) throw new Error('Ключ шифрования не открыт')
  return encryptData(state.key, value)
}

async function decrypted(value) {
  if (!state.key) throw new Error('Ключ шифрования не открыт')
  return decryptData(state.key, value)
}

async function prepareSession(user) {
  state.user = user
  state.key = await getDeviceKey(user.id)
  if (state.key) {
    state.phase = 'app'
    await Promise.all([loadCourses(), loadCatalog()])
    return
  }
  try {
    await usersApi.getEncryptionKey()
    state.encryptionExists = true
  } catch (error) {
    if (error.status !== 404) throw error
    state.encryptionExists = false
  }
  state.phase = 'encryption'
}

export async function bootstrap() {
  if (!getAccessToken() && !getRefreshToken()) {
    state.phase = 'auth'
    return
  }
  try {
    await prepareSession(await usersApi.getMe())
  } catch (error) {
    clearTokens()
    state.phase = 'auth'
    showError(error)
  }
}

export async function requestAuthCode(email) {
  state.busy = true
  try {
    await authApi.requestCode(email)
    showToast('Код отправлен на почту')
  } finally {
    state.busy = false
  }
}

export async function verifyAuthCode(email, code) {
  state.busy = true
  try {
    const result = await authApi.verifyCode(email, code)
    saveTokens(result.access_token, result.refresh_token)
    await prepareSession(result.user)
  } finally {
    state.busy = false
  }
}

export async function setupEncryption(password) {
  state.busy = true
  try {
    const result = await createEncryptionKey(password)
    await usersApi.saveEncryptionKey(result.encrypted)
    await saveDeviceKey(state.user.id, result.key)
    state.key = result.key
    state.phase = 'app'
    await Promise.all([loadCourses(), loadCatalog()])
    showToast('Защита данных настроена')
  } finally {
    state.busy = false
  }
}

export async function unlockEncryption(password) {
  state.busy = true
  try {
    const result = await usersApi.getEncryptionKey()
    const { key } = await unwrapEncryptionKey(result.encrypted_dek, password)
    await saveDeviceKey(state.user.id, key)
    state.key = key
    state.phase = 'app'
    await Promise.all([loadCourses(), loadCatalog()])
  } finally {
    state.busy = false
  }
}

export async function changeEncryptionPassword(currentPassword, newPassword) {
  const result = await usersApi.getEncryptionKey()
  const { rawKey } = await unwrapEncryptionKey(result.encrypted_dek, currentPassword)
  const wrapped = await wrapEncryptionKey(rawKey, newPassword)
  await usersApi.saveEncryptionKey(wrapped)
  showToast('Пароль шифрования изменён')
}

export async function forgetDevice() {
  if (state.user) await removeDeviceKey(state.user.id)
  state.key = null
  state.encryptionExists = true
  state.phase = 'encryption'
}

export function logout() {
  clearTokens()
  state.phase = 'auth'
  state.page = 'calendar'
  state.user = null
  state.key = null
  state.courses = []
  state.dayItems = []
  state.intakes = []
}

export async function loadCatalog(filters = {}) {
  const result = await medicationsApi.getMedications({ limit: 100, ...filters })
  state.catalog = result.items
  state.catalogTotal = result.total
}

export async function openGuestCatalog() {
  state.phase = 'guest'
  state.page = 'catalog'
  await loadCatalog()
}

async function mapSchedule(item) {
  const data = await decrypted(item.encrypted_data)
  return {
    ...item,
    time: item.scheduled_at.slice(0, 5),
    amount: data.amount,
    unit: data.unit,
  }
}

async function mapCourse(item) {
  const data = await decrypted(item.encrypted_data)
  const schedules = await Promise.all(item.schedules.map(mapSchedule))
  return {
    ...item,
    name: data.name,
    medicationId: data.medicationId ?? null,
    notes: data.notes || '',
    schedules,
  }
}

export async function loadCourses() {
  const result = await coursesApi.getCourses()
  state.courses = await Promise.all(result.items.map(mapCourse))
  scheduleReminders(state.courses, state.preferences, state.user?.timezone)
}

export async function saveCourse(form, schedules) {
  const encryptedData = await encrypted({
    name: form.name.trim(),
    medicationId: form.medicationId || null,
    notes: form.notes.trim(),
  })
  const course = await coursesApi.createCourse({
    start_date: form.startDate,
    end_date: form.endDate || null,
    encrypted_data: encryptedData,
  })
  for (const schedule of schedules) {
    await schedulesApi.createSchedule(course.id, {
      scheduled_at: schedule.time,
      days_of_week: schedule.days,
      encrypted_data: await encrypted({ amount: Number(schedule.amount), unit: schedule.unit.trim() }),
    })
  }
  await loadCourses()
  state.selectedCourseId = course.id
  showToast('Курс добавлен')
  return course.id
}

export async function editCourse(id, form) {
  const current = state.courses.find(item => item.id === id)
  const encryptedData = await encrypted({
    name: form.name.trim(),
    medicationId: form.medicationId || null,
    notes: form.notes.trim(),
  })
  await coursesApi.updateCourse(id, {
    start_date: form.startDate,
    end_date: form.endDate || null,
    is_active: form.isActive,
    encrypted_data: encryptedData,
  })
  await loadCourses()
  if (current?.name !== form.name.trim()) showToast('Название обновлено')
  else showToast('Курс обновлён')
}

export async function removeCourse(id) {
  await coursesApi.deleteCourse(id)
  await loadCourses()
  showToast('Курс удалён')
}

export async function addSchedule(courseId, form) {
  await schedulesApi.createSchedule(courseId, {
    scheduled_at: form.time,
    days_of_week: form.days,
    encrypted_data: await encrypted({ amount: Number(form.amount), unit: form.unit.trim() }),
  })
  await loadCourses()
  showToast('Время добавлено')
}

export async function editSchedule(id, form) {
  await schedulesApi.updateSchedule(id, {
    scheduled_at: form.time,
    days_of_week: form.days,
    encrypted_data: await encrypted({ amount: Number(form.amount), unit: form.unit.trim() }),
  })
  await loadCourses()
  showToast('Расписание обновлено')
}

export async function removeSchedule(id) {
  await schedulesApi.deleteSchedule(id)
  await loadCourses()
  showToast('Время удалено')
}

export async function loadDay(date) {
  const result = await schedulesApi.getSchedulesForDay(date)
  state.dayItems = await Promise.all(result.items.map(async item => {
    const courseData = await decrypted(item.course_data)
    const scheduleData = await decrypted(item.schedule_data)
    const intakeData = item.intake ? await decrypted(item.intake.encrypted_data) : null
    return { ...item, courseData, scheduleData, intakeData }
  }))
}

export async function takeScheduled(item) {
  const now = new Date()
  const today = dateInTimeZone(now, state.user?.timezone)
  const plannedDate = item.planned_at.slice(0, 10)
  await intakesApi.createIntake({
    course_id: item.course_id,
    schedule_id: item.schedule_id,
    taken_at: plannedDate === today ? now.toISOString() : item.planned_at,
    encrypted_data: await encrypted({
      medicationName: item.courseData.name,
      amount: item.scheduleData.amount,
      unit: item.scheduleData.unit,
    }),
  })
  showToast('Приём отмечен')
}

export async function cancelScheduled(item) {
  await intakesApi.deleteIntake(item.intake.id)
  showToast('Отметка отменена')
}

export async function saveUnplannedIntake(form) {
  await intakesApi.createIntake({
    course_id: form.courseId || null,
    schedule_id: null,
    taken_at: zonedDateTimeToIso(form.takenAt, state.user?.timezone),
    encrypted_data: await encrypted({
      medicationName: form.medicationName.trim(),
      amount: Number(form.amount),
      unit: form.unit.trim(),
    }),
  })
  showToast('Приём записан')
}

async function mapIntake(item) {
  const data = await decrypted(item.encrypted_data)
  return { ...item, ...data }
}

export async function loadIntakes(filters = {}) {
  const result = await intakesApi.getIntakes(filters)
  state.intakes = await Promise.all(result.items.map(mapIntake))
}

export async function editIntake(id, form) {
  await intakesApi.updateIntake(id, {
    taken_at: zonedDateTimeToIso(form.takenAt, state.user?.timezone),
    encrypted_data: await encrypted({
      medicationName: form.medicationName.trim(),
      amount: Number(form.amount),
      unit: form.unit.trim(),
    }),
  })
  await loadIntakes()
  showToast('Запись обновлена')
}

export async function removeIntake(id) {
  await intakesApi.deleteIntake(id)
  await loadIntakes()
  showToast('Запись удалена')
}

export async function saveProfile(form) {
  state.user = await usersApi.updateMe({
    name: form.name || null,
    birth_date: form.birthDate || null,
    timezone: form.timezone,
  })
  scheduleReminders(state.courses, state.preferences, state.user.timezone)
  showToast('Профиль сохранён')
}

export function updatePreferences(value) {
  state.preferences = { ...state.preferences, ...value }
  savePreferences(state.preferences)
  scheduleReminders(state.courses, state.preferences, state.user?.timezone)
}

export async function saveMedication(form, id = null) {
  const body = {
    name: form.name.trim(),
    international_name: form.internationalName || null,
    manufacturer: form.manufacturer || null,
    category: form.category || null,
    instruction_url: form.instructionUrl || null,
    form: form.form || null,
    strength: form.strength || null,
  }
  if (id) await medicationsApi.updateMedication(id, { ...body, is_active: form.isActive })
  else await medicationsApi.createMedication(body)
  await loadCatalog()
  showToast(id ? 'Лекарство обновлено' : 'Лекарство добавлено')
}

export async function toggleMedication(item) {
  await medicationsApi.updateMedication(item.id, { is_active: !item.is_active })
  await loadCatalog()
  showToast(item.is_active ? 'Лекарство скрыто' : 'Лекарство опубликовано')
}
