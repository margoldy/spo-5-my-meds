<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import { dateTimeInTimeZone } from '../utils/date'
import { editIntake, go, loadCatalog, saveUnplannedIntake, showError } from '../store/store'
import { state } from '../store/state'

const editing = computed(() => state.intakes.find(item => item.id === state.selectedIntakeId))
const mode = ref('course')
const otherSource = ref('catalog')
const form = reactive({ courseId: '', medicationId: '', medicationName: '', amount: 1, unit: 'таблетка', takenAt: dateTimeInTimeZone(new Date(), state.user?.timezone) })

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
  if (!editing.value && state.courses.length) {
    form.courseId = state.courses.find(item => item.is_active)?.id || ''
    useCourse()
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
  <section class="screen no-nav">
    <AppHeader :title="editing ? 'Изменить приём' : 'Внеплановый приём'" back @back="go(editing ? 'history' : 'calendar')" />
    <form @submit.prevent="submit">
      <div v-if="!editing" class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Лекарство</span><strong>Что вы приняли?</strong></div>
        <div class="segmented-control">
          <button type="button" :class="{ active: mode === 'course' }" @click="mode = 'course'">Из моего курса</button>
          <button type="button" :class="{ active: mode === 'other' }" @click="mode = 'other'">Другое</button>
        </div>
        <template v-if="mode === 'course'">
          <label class="field-label">Курс</label>
          <select v-model="form.courseId" class="detail-field" required @change="useCourse">
            <option disabled value="">Выберите курс</option>
            <option v-for="course in state.courses.filter(item => item.is_active)" :key="course.id" :value="course.id">{{ course.name }}</option>
          </select>
        </template>
        <template v-else>
          <label class="field-label">Где найти название</label>
          <div class="segmented-control compact">
            <button type="button" :class="{ active: otherSource === 'catalog' }" @click="otherSource = 'catalog'">Справочник</button>
            <button type="button" :class="{ active: otherSource === 'custom' }" @click="otherSource = 'custom'">Ввести самой</button>
          </div>
          <template v-if="otherSource === 'catalog'">
            <label class="field-label">Лекарство</label>
            <select v-model="form.medicationId" class="detail-field" required @change="useMedication">
              <option disabled value="">Выберите лекарство</option>
              <option v-for="item in state.catalog.filter(item => item.is_active)" :key="item.id" :value="item.id">{{ item.name }}{{ item.strength ? ` — ${item.strength}` : '' }}</option>
            </select>
          </template>
          <template v-else>
            <label class="field-label">Название</label>
            <input v-model.trim="form.medicationName" class="detail-field" required placeholder="Название лекарства">
          </template>
        </template>
      </div>
      <div v-else class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Лекарство</span><strong>Название</strong></div>
        <input v-model.trim="form.medicationName" class="detail-field" required>
      </div>
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Приём</span><strong>Сколько и когда?</strong></div>
        <div class="dose-row">
          <label>Количество<input v-model.number="form.amount" class="detail-field" type="number" min="0.01" step="0.01" required></label>
          <label>Единица<input v-model.trim="form.unit" class="detail-field" required placeholder="мг"></label>
        </div>
        <label class="field-label">Дата и время</label>
        <input v-model="form.takenAt" class="detail-field" type="datetime-local" required>
      </div>
      <button class="primary-button form-submit" type="submit">{{ editing ? 'Сохранить изменения' : 'Записать приём' }}</button>
    </form>
  </section>
</template>
