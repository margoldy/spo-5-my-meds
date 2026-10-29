<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import AppModal from '../components/ui/AppModal.vue'
import TimeInput from '../components/ui/TimeInput.vue'
import { daysText, formatDate } from '../utils/date'
import { addSchedule, editCourse, editSchedule, go, loadCourseIntakes, removeCourse, removeSchedule, showError, showToast } from '../store/store'
import { state } from '../store/state'
import { getCourseInventory, removeCourseInventory, saveCourseInventory } from '../utils/storage'

const course = computed(() => state.courses.find(item => item.id === state.selectedCourseId))
const editing = ref(false)
const scheduleModal = ref(false)
const inventoryModal = ref(false)
const scheduleId = ref(null)
const form = reactive({ name: '', medicationId: null, notes: '', startDate: '', endDate: '', isActive: true })
const schedule = reactive({ time: '09:00', amount: 1, unit: 'таблетка', days: [1, 2, 3, 4, 5, 6, 7] })
const inventory = ref(getCourseInventory(state.user?.id, state.selectedCourseId))
const inventoryForm = reactive({ amount: 0, unit: 'таблетка' })

const usedAmount = computed(() => {
  if (!inventory.value) return 0
  return state.courseIntakes
    .filter(item => new Date(item.taken_at) >= new Date(inventory.value.countedAt))
    .filter(item => item.unit.trim().toLowerCase() === inventory.value.unit.trim().toLowerCase())
    .reduce((total, item) => total + Number(item.amount || 0), 0)
})
const remainingAmount = computed(() => Math.max(0, Number(inventory.value?.amount || 0) - usedAmount.value))
const dailyAmount = computed(() => {
  if (!course.value || !inventory.value) return 0
  return course.value.schedules
    .filter(item => item.unit.trim().toLowerCase() === inventory.value.unit.trim().toLowerCase())
    .reduce((total, item) => total + Number(item.amount) * item.days_of_week.length / 7, 0)
})
const daysLeft = computed(() => dailyAmount.value ? Math.floor(remainingAmount.value / dailyAmount.value) : null)

function fillForm() {
  if (!course.value) return
  Object.assign(form, {
    name: course.value.name,
    medicationId: course.value.medicationId,
    notes: course.value.notes,
    startDate: course.value.start_date,
    endDate: course.value.end_date || '',
    isActive: course.value.is_active,
  })
}

function openSchedule(item = null) {
  scheduleId.value = item?.id || null
  Object.assign(schedule, item ? {
    time: item.time,
    amount: item.amount,
    unit: item.unit,
    days: [...item.days_of_week],
  } : { time: '09:00', amount: 1, unit: 'таблетка', days: [1, 2, 3, 4, 5, 6, 7] })
  scheduleModal.value = true
}

function openInventory() {
  inventoryForm.amount = inventory.value ? remainingAmount.value : 0
  inventoryForm.unit = inventory.value?.unit || course.value?.schedules[0]?.unit || 'таблетка'
  inventoryModal.value = true
}

function saveInventory() {
  if (inventoryForm.amount < 0 || !inventoryForm.unit.trim()) return
  inventory.value = {
    amount: Number(inventoryForm.amount),
    unit: inventoryForm.unit.trim(),
    countedAt: new Date().toISOString(),
  }
  saveCourseInventory(state.user?.id, course.value.id, inventory.value)
  inventoryModal.value = false
  showToast('Остаток сохранён на устройстве')
}

function disableInventory() {
  removeCourseInventory(state.user?.id, course.value.id)
  inventory.value = null
  inventoryModal.value = false
  showToast('Учёт остатка отключён')
}

function toggleDay(day) {
  if (schedule.days.includes(day)) schedule.days = schedule.days.filter(item => item !== day)
  else schedule.days = [...schedule.days, day].sort()
}

async function saveDetails() {
  try {
    await editCourse(course.value.id, form)
    editing.value = false
  } catch (error) {
    showError(error)
  }
}

async function saveSchedule() {
  try {
    if (!schedule.days.length) throw new Error('Выберите хотя бы один день')
    if (scheduleId.value) await editSchedule(scheduleId.value, schedule)
    else await addSchedule(course.value.id, schedule)
    scheduleModal.value = false
  } catch (error) {
    showError(error)
  }
}

async function deleteScheduleItem(id) {
  if (!confirm('Удалить это время приёма?')) return
  try {
    await removeSchedule(id)
  } catch (error) {
    showError(error)
  }
}

async function deleteCurrentCourse() {
  if (!confirm('Удалить курс и его расписание?')) return
  try {
    await removeCourse(course.value.id)
    go('courses')
  } catch (error) {
    showError(error)
  }
}

function openHistory() {
  go('history')
}

watch(course, fillForm, { immediate: true })
onMounted(async () => {
  try {
    await loadCourseIntakes(state.selectedCourseId)
  } catch (error) {
    showError(error)
  }
})
</script>

<template>
  <section v-if="course" class="screen no-nav">
    <AppHeader title="Информация о лекарстве" back @back="go('courses')" />
    <form v-if="editing" @submit.prevent="saveDetails">
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Курс</span><strong>Основные данные</strong></div>
        <label class="field-label">Название</label>
        <input v-model.trim="form.name" class="detail-field" required>
        <div class="two-columns">
          <label>Начало<input v-model="form.startDate" class="detail-field" type="date" required></label>
          <label>Конец<input v-model="form.endDate" class="detail-field" type="date" :min="form.startDate"></label>
        </div>
        <label class="field-label">Заметки</label>
        <textarea v-model="form.notes" class="notes"></textarea>
      </div>
      <label class="toggle-row"><span><strong>Курс активен</strong><small>Показывать в календаре</small></span><input v-model="form.isActive" type="checkbox"></label>
      <div class="button-row"><button class="secondary-button" type="button" @click="editing = false; fillForm()">Отмена</button><button class="primary-button" type="submit">Сохранить</button></div>
    </form>
    <template v-else>
      <div class="course-detail-hero">
        <span class="section-kicker">Лекарство</span>
        <h2>{{ course.name }}</h2>
        <span class="badge" :class="{ inactive: !course.is_active }">{{ course.is_active ? 'Активный курс' : 'Курс завершён' }}</span>
      </div>
      <h2 class="section-title">Период курса</h2>
      <div class="detail-card info-grid course-period">
        <span class="info-label">Начало</span><span>{{ formatDate(course.start_date) }}</span>
        <span class="info-label">Конец</span><span>{{ formatDate(course.end_date) }}</span>
      </div>
      <h2 class="section-title">Расписание</h2>
      <div v-if="course.schedules.length" class="schedule-list">
        <div v-for="item in course.schedules" :key="item.id" class="schedule-row">
          <button class="schedule-main" type="button" @click="openSchedule(item)"><strong>{{ item.time }} — {{ item.amount }} {{ item.unit }}</strong><span>{{ daysText(item.days_of_week) }}</span></button>
          <button class="mini-button danger" type="button" aria-label="Удалить расписание" @click="deleteScheduleItem(item.id)">×</button>
        </div>
      </div>
      <div v-else class="as-needed-note"><strong>По необходимости</strong><span>Без расписания</span></div>
      <button class="secondary-button add-time-button" type="button" @click="openSchedule()">＋ Добавить время</button>
      <h2 class="section-title detail-section">Остаток лекарства</h2>
      <button v-if="inventory" class="inventory-card" type="button" @click="openInventory">
        <span class="inventory-amount"><strong>{{ Number(remainingAmount.toFixed(2)) }}</strong><small>{{ inventory.unit }}</small></span>
        <span class="inventory-copy"><strong>Сейчас в наличии</strong><small v-if="daysLeft !== null">Примерно на {{ daysLeft }} дн.</small><small v-else>Нажмите, чтобы изменить количество</small></span>
        <span class="row-arrow">›</span>
      </button>
      <button v-else class="inventory-empty" type="button" @click="openInventory"><span>＋</span><div><strong>Указать остаток</strong><small>Количество будет храниться только на этом устройстве</small></div></button>
      <h2 class="section-title detail-section">Заметки</h2>
      <div class="read-field notes-view">{{ course.notes || 'Нет заметок' }}</div>
      <div class="menu-list detail-actions">
        <button type="button" @click="editing = true"><span>Изменить курс</span><span>›</span></button>
        <button type="button" @click="openHistory"><span>История приёмов</span><span>›</span></button>
        <button class="danger-text" type="button" @click="deleteCurrentCourse"><span>Удалить курс</span><span>×</span></button>
      </div>
    </template>
  </section>
  <AppModal v-if="scheduleModal" :title="scheduleId ? 'Изменить время' : 'Добавить время'" @close="scheduleModal = false">
    <form @submit.prevent="saveSchedule">
      <TimeInput v-model="schedule.time" />
      <div class="dose-row">
        <label>Количество<input v-model.number="schedule.amount" class="detail-field" type="number" min="0.01" step="0.01" required></label>
        <label>Единица<input v-model.trim="schedule.unit" class="detail-field" required></label>
      </div>
      <div class="weekdays">
        <button v-for="(day, index) in ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']" :key="day" type="button" :class="{ selected: schedule.days.includes(index + 1) }" @click="toggleDay(index + 1)">{{ day }}</button>
      </div>
      <div class="modal-actions"><button class="action-button" type="button" @click="scheduleModal = false">Отмена</button><button class="action-button primary" type="submit">Сохранить</button></div>
    </form>
  </AppModal>
  <AppModal v-if="inventoryModal" title="Остаток лекарства" @close="inventoryModal = false">
    <form @submit.prevent="saveInventory">
      <p class="inventory-modal-note">Введите, сколько лекарства есть сейчас. После отмеченных приёмов остаток будет пересчитываться автоматически.</p>
      <div class="dose-row">
        <label>Количество<input v-model.number="inventoryForm.amount" class="detail-field" type="number" min="0" step="0.01" required></label>
        <label>Единица<input v-model.trim="inventoryForm.unit" class="detail-field" required></label>
      </div>
      <button v-if="inventory" class="text-button inventory-remove" type="button" @click="disableInventory">Отключить учёт остатка</button>
      <div class="modal-actions"><button class="action-button" type="button" @click="inventoryModal = false">Отмена</button><button class="action-button primary" type="submit">Сохранить</button></div>
    </form>
  </AppModal>
</template>
