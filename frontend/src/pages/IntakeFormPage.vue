<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import TimeInput from '../components/ui/TimeInput.vue'
import { dateTimeInTimeZone } from '../utils/date'
import { editIntake, go, loadCatalog, saveUnplannedIntake, showError } from '../store/store'
import { state } from '../store/state'

const editing = computed(() => state.intakes.find(item => item.id === state.selectedIntakeId))
const mode = ref('course')
const otherSource = ref('catalog')
const form = reactive({ courseId: '', medicationId: '', medicationName: '', amount: 1, unit: 'таблетка', takenAt: dateTimeInTimeZone(new Date(), state.user?.timezone) })
const activeCourses = computed(() => state.courses.filter(item => item.is_active))
const selectedCourse = computed(() => state.courses.find(item => item.id === form.courseId))
const intakeDate = computed({
  get: () => form.takenAt.slice(0, 10),
  set: value => form.takenAt = `${value}T${intakeTime.value}`,
})
const intakeTime = computed({
  get: () => form.takenAt.slice(11, 16),
  set: value => form.takenAt = `${intakeDate.value}T${value}`,
})

function selectMode(value) {
  mode.value = value
  if (value === 'course') {
    form.courseId = activeCourses.value[0]?.id || ''
    useCourse()
    return
  }
  form.courseId = ''
  form.medicationId = ''
  form.medicationName = ''
}

function selectOtherSource(value) {
  otherSource.value = value
  form.medicationId = ''
  form.medicationName = ''
}

function useCourse() {
  const course = state.courses.find(item => item.id === form.courseId)
  if (!course) return
  form.medicationName = course.name
  const schedule = course.schedules[0]
  if (schedule) {
    form.amount = schedule.amount
    form.unit = schedule.unit
  }
}

function useMedication() {
  const medication = state.catalog.find(item => item.id === Number(form.medicationId))
  if (!medication) return
  form.medicationName = medication.name
  form.unit = ['Суспензия', 'Раствор'].includes(medication.form) ? 'мл' : 'таблетка'
}

function changeAmount(value) {
  const amount = Number(form.amount) || 0
  form.amount = Math.max(0.01, Number((amount + value).toFixed(2)))
}

function setCurrentTime() {
  form.takenAt = dateTimeInTimeZone(new Date(), state.user?.timezone)
}

async function submit() {
  try {
    if (!form.medicationName.trim()) throw new Error('Укажите лекарство')
    if (editing.value) await editIntake(editing.value.id, form)
    else {
      form.courseId = mode.value === 'course' ? form.courseId : ''
      await saveUnplannedIntake(form)
    }
    go(editing.value ? 'history' : 'calendar')
  } catch (error) {
    showError(error)
  }
}

watch(editing, item => {
  if (!item) return
  Object.assign(form, {
    courseId: item.course_id || '',
    medicationName: item.medicationName,
    amount: item.amount,
    unit: item.unit,
    takenAt: dateTimeInTimeZone(new Date(item.taken_at), state.user?.timezone),
  })
}, { immediate: true })

onMounted(async () => {
  if (!editing.value) {
    if (activeCourses.value.length) {
      form.courseId = activeCourses.value[0].id
      useCourse()
    } else {
      mode.value = 'other'
    }
  }
  if (!state.catalog.length) {
    try {
      await loadCatalog()
    } catch (error) {
      showError(error)
    }
  }
})
</script>

<template>
  <section class="screen no-nav intake-form-screen">
    <AppHeader :title="editing ? 'Изменить приём' : 'Внеплановый приём'" back @back="go(editing ? 'history' : 'calendar')" />
    <p class="intake-form-lead">{{ editing ? 'Исправьте данные сохранённого приёма' : 'Запишите лекарство, дозировку и фактическое время приёма' }}</p>
    <form class="intake-form" @submit.prevent="submit">
      <div v-if="!editing" class="intake-section">
        <div class="intake-section-heading">
          <span>1</span>
          <div><strong>Выберите лекарство</strong><small>Из курса или отдельная запись</small></div>
        </div>
        <div class="intake-source-choice">
          <button type="button" :class="{ active: mode === 'course' }" @click="selectMode('course')">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8"/><path d="M7.5 16.5l9-9"/></svg>
            <span><strong>Из курса</strong><small>Выбрать назначенное лекарство</small></span>
          </button>
          <button type="button" :class="{ active: mode === 'other' }" @click="selectMode('other')">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14"/></svg>
            <span><strong>Другое</strong><small>Справочник или своё название</small></span>
          </button>
        </div>
        <template v-if="mode === 'course'">
          <label class="intake-field-label">Курс лечения</label>
          <select v-model="form.courseId" class="intake-field" required @change="useCourse">
            <option disabled value="">Выберите курс</option>
            <option v-for="course in activeCourses" :key="course.id" :value="course.id">{{ course.name }}</option>
          </select>
          <div v-if="selectedCourse" class="selected-medication">
            <span>Выбрано</span>
            <strong>{{ selectedCourse.name }}</strong>
            <small v-if="selectedCourse.schedules.length">Дозировка подставлена из расписания — её можно изменить ниже</small>
          </div>
        </template>
        <template v-else>
          <div class="intake-source-tabs">
            <button type="button" :class="{ active: otherSource === 'catalog' }" @click="selectOtherSource('catalog')">Из справочника</button>
            <button type="button" :class="{ active: otherSource === 'custom' }" @click="selectOtherSource('custom')">Ввести название</button>
          </div>
          <template v-if="otherSource === 'catalog'">
            <label class="intake-field-label">Лекарство</label>
            <select v-model="form.medicationId" class="intake-field" required @change="useMedication">
              <option disabled value="">Выберите лекарство</option>
              <option v-for="item in state.catalog.filter(item => item.is_active)" :key="item.id" :value="item.id">{{ item.name }}{{ item.strength ? ` — ${item.strength}` : '' }}</option>
            </select>
          </template>
          <template v-else>
            <label class="intake-field-label">Название лекарства</label>
            <input v-model.trim="form.medicationName" class="intake-field" required placeholder="Например, Ибупрофен">
          </template>
        </template>
      </div>
      <div v-else class="intake-section">
        <div class="intake-section-heading">
          <span>1</span>
          <div><strong>Лекарство</strong><small>Название в истории приёмов</small></div>
        </div>
        <input v-model.trim="form.medicationName" class="intake-field" required>
      </div>

      <div class="intake-section">
        <div class="intake-section-heading">
          <span>2</span>
          <div><strong>Укажите дозировку</strong><small>Фактически принятое количество</small></div>
        </div>
        <div class="intake-dose-grid">
          <label>
            <span>Количество</span>
            <div class="amount-control">
              <button type="button" aria-label="Уменьшить количество" @click="changeAmount(-0.5)">−</button>
              <input v-model.number="form.amount" type="number" min="0.01" step="0.01" required>
              <button type="button" aria-label="Увеличить количество" @click="changeAmount(0.5)">+</button>
            </div>
          </label>
          <label>
            <span>Единица</span>
            <input v-model.trim="form.unit" class="intake-field" list="intake-units" required placeholder="мг">
            <datalist id="intake-units">
              <option value="таблетка"></option>
              <option value="капсула"></option>
              <option value="мл"></option>
              <option value="мг"></option>
              <option value="капля"></option>
              <option value="доза"></option>
            </datalist>
          </label>
        </div>
      </div>

      <div class="intake-section intake-date-section">
        <div class="intake-section-heading">
          <span>3</span>
          <div><strong>Когда приняли?</strong><small>Дата и точное время</small></div>
          <button class="now-button" type="button" @click="setCurrentTime">Сейчас</button>
        </div>
        <label class="intake-field-label">Дата</label>
        <input v-model="intakeDate" class="intake-field intake-date" type="date" required>
        <label class="intake-field-label">Время</label>
        <TimeInput v-model="intakeTime" />
      </div>

      <div class="intake-submit-wrap">
        <button class="primary-button intake-submit" type="submit">
          <span>{{ editing ? 'Сохранить изменения' : 'Записать приём' }}</span>
          <svg viewBox="0 0 24 24" fill="none"><path d="m8 12 3 3 5-6"/></svg>
        </button>
      </div>
    </form>
  </section>
</template>
