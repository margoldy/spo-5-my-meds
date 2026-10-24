<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import TimeInput from '../components/ui/TimeInput.vue'
import { dateInTimeZone } from '../utils/date'
import { go, loadCatalog, saveCourse, showError } from '../store/store'
import { state } from '../store/state'

const source = ref(state.coursePreset ? 'catalog' : 'custom')
const mode = ref('scheduled')
const schedules = ref([])
const editingIndex = ref(null)
const form = reactive({
  medicationId: state.coursePreset?.id || '',
  name: state.coursePreset?.name || '',
  startDate: dateInTimeZone(new Date(), state.user?.timezone),
  endDate: '',
  notes: '',
})
const schedule = reactive({ time: '09:00', amount: 1, unit: state.coursePreset?.form === 'Суспензия' ? 'мл' : 'таблетка', days: [1, 2, 3, 4, 5, 6, 7] })
const selectedMedication = computed(() => state.catalog.find(item => item.id === Number(form.medicationId)))

function selectMedication() {
  const item = selectedMedication.value
  if (!item) return
  form.name = item.name
  if (item.form === 'Суспензия' || item.form === 'Раствор') schedule.unit = 'мл'
}

function toggleDay(day) {
  if (schedule.days.includes(day)) schedule.days = schedule.days.filter(item => item !== day)
  else schedule.days = [...schedule.days, day].sort()
}

function resetSchedule() {
  schedule.time = '09:00'
  schedule.amount = 1
  schedule.unit = 'таблетка'
  schedule.days = [1, 2, 3, 4, 5, 6, 7]
  editingIndex.value = null
}

function addDraftSchedule() {
  if (!schedule.days.length) return showError(new Error('Выберите хотя бы один день'))
  if (!schedule.unit.trim() || Number(schedule.amount) <= 0) return showError(new Error('Укажите дозировку'))
  const value = { time: schedule.time, amount: Number(schedule.amount), unit: schedule.unit.trim(), days: [...schedule.days] }
  if (editingIndex.value === null) schedules.value.push(value)
  else schedules.value.splice(editingIndex.value, 1, value)
  resetSchedule()
}

function editDraft(index) {
  const item = schedules.value[index]
  schedule.time = item.time
  schedule.amount = item.amount
  schedule.unit = item.unit
  schedule.days = [...item.days]
  editingIndex.value = index
}

async function submit() {
  try {
    if (source.value === 'catalog') selectMedication()
    else form.medicationId = ''
    if (!form.name.trim()) throw new Error('Укажите название лекарства')
    if (mode.value === 'scheduled' && !schedules.value.length) throw new Error('Добавьте хотя бы одно время приёма')
    await saveCourse(form, mode.value === 'scheduled' ? schedules.value : [])
    state.coursePreset = null
    go('course-detail')
  } catch (error) {
    showError(error)
  }
}

onMounted(async () => {
  if (state.catalog.length) return
  try {
    await loadCatalog()
  } catch (error) {
    showError(error)
  }
})
</script>

<template>
  <section class="screen no-nav">
    <AppHeader title="Добавить лекарство" back @back="go('courses')" />
    <form @submit.prevent="submit">
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Шаг 1</span><strong>Выберите лекарство</strong></div>
        <div class="segmented-control">
          <button type="button" :class="{ active: source === 'catalog' }" @click="source = 'catalog'">Из справочника</button>
          <button type="button" :class="{ active: source === 'custom' }" @click="source = 'custom'">Ввести своё</button>
        </div>
        <template v-if="source === 'catalog'">
          <label class="field-label">Лекарство</label>
          <select v-model="form.medicationId" class="detail-field" required @change="selectMedication">
            <option disabled value="">Выберите лекарство</option>
            <option v-for="item in state.catalog.filter(item => item.is_active)" :key="item.id" :value="item.id">{{ item.name }}{{ item.strength ? ` — ${item.strength}` : '' }}</option>
          </select>
        </template>
        <template v-else>
          <label class="field-label">Название</label>
          <input v-model.trim="form.name" class="detail-field" required placeholder="Например, витамин D">
        </template>
      </div>
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Шаг 2</span><strong>Укажите период</strong></div>
        <div class="two-columns">
          <label>Начало<input v-model="form.startDate" class="detail-field" type="date" required></label>
          <label>Конец<input v-model="form.endDate" class="detail-field" type="date" :min="form.startDate"></label>
        </div>
        <label class="field-label">Как принимать</label>
        <div class="segmented-control">
          <button type="button" :class="{ active: mode === 'scheduled' }" @click="mode = 'scheduled'">По расписанию</button>
          <button type="button" :class="{ active: mode === 'as-needed' }" @click="mode = 'as-needed'">По необходимости</button>
        </div>
        <p v-if="mode === 'as-needed'" class="field-hint">Без расписания и напоминаний</p>
      </div>
      <div v-if="mode === 'scheduled'" class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Шаг 3</span><strong>Добавьте время</strong></div>
        <div class="schedule-list draft-schedules">
          <div v-for="(item, index) in schedules" :key="`${item.time}-${index}`" class="schedule-row">
            <button class="schedule-main" type="button" @click="editDraft(index)">
              <strong>{{ item.time }} — {{ item.amount }} {{ item.unit }}</strong>
              <span>{{ item.days.length === 7 ? 'Ежедневно' : item.days.map(day => ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'][day - 1]).join(', ') }}</span>
            </button>
            <button class="mini-button danger" type="button" aria-label="Удалить" @click="schedules.splice(index, 1)">×</button>
          </div>
        </div>
        <div class="schedule-editor">
          <label class="field-label">Время</label>
          <TimeInput v-model="schedule.time" />
          <div class="dose-row">
            <label>Количество<input v-model.number="schedule.amount" class="detail-field" type="number" min="0.01" step="0.01"></label>
            <label>Единица<input v-model.trim="schedule.unit" class="detail-field" placeholder="мг"></label>
          </div>
          <label class="field-label">Дни недели</label>
          <div class="weekdays">
            <button v-for="(day, index) in ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']" :key="day" type="button" :class="{ selected: schedule.days.includes(index + 1) }" @click="toggleDay(index + 1)">{{ day }}</button>
          </div>
          <button class="secondary-button add-time-button" type="button" @click="addDraftSchedule">{{ editingIndex === null ? '＋ Добавить это время' : 'Сохранить изменения' }}</button>
        </div>
      </div>
      <div class="form-section optional-section">
        <div class="form-section-heading"><span class="section-kicker">Необязательно</span><strong>Заметки</strong></div>
        <textarea v-model="form.notes" class="notes" placeholder="Например, принимать после еды"></textarea>
      </div>
      <button class="primary-button form-submit" type="submit">Сохранить курс</button>
    </form>
  </section>
</template>
