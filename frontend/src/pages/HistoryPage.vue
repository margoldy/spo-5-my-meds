<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { calendarDays, dateInTimeZone, formatDate, formatTime, isoDate, monthTitle, zonedDateTimeToIso } from '../utils/date'
import { go, loadIntakes, removeIntake, showError } from '../store/store'
import { state } from '../store/state'

const initialDate = dateInTimeZone(new Date(), state.user?.timezone)
const selected = ref(initialDate)
const month = ref(new Date(`${initialDate}T12:00:00`))
const filters = reactive({ course_id: state.previousPage === 'course-detail' ? state.selectedCourseId : '' })
const days = computed(() => calendarDays(month.value))
const intakeDates = computed(() => new Set(state.intakes.map(item => dateInTimeZone(new Date(item.taken_at), state.user?.timezone))))
const visibleIntakes = computed(() => state.intakes.filter(item => dateInTimeZone(new Date(item.taken_at), state.user?.timezone) === selected.value))
const selectedTitle = computed(() => formatDate(selected.value))
const fromCourse = computed(() => state.previousPage === 'course-detail')

function monthRange() {
  const first = new Date(month.value.getFullYear(), month.value.getMonth(), 1)
  const last = new Date(month.value.getFullYear(), month.value.getMonth() + 1, 0)
  return {
    from: zonedDateTimeToIso(`${isoDate(first)}T00:00:00`, state.user?.timezone),
    to: zonedDateTimeToIso(`${isoDate(last)}T23:59:59.999`, state.user?.timezone),
  }
}

async function refresh() {
  try {
    await loadIntakes({ ...monthRange(), course_id: filters.course_id || undefined })
  } catch (error) {
    showError(error)
  }
}

function changeMonth(direction) {
  const next = new Date(month.value.getFullYear(), month.value.getMonth() + direction, 1)
  month.value = next
  selected.value = isoDate(next)
}

function selectDay(item) {
  selected.value = item.value
  if (!item.current) month.value = new Date(item.date.getFullYear(), item.date.getMonth(), 1)
}

function edit(item) {
  state.selectedIntakeId = item.id
  go('intake-form')
}

async function remove(id) {
  if (!confirm('Удалить запись о приёме?')) return
  try {
    await removeIntake(id)
    await refresh()
  } catch (error) {
    showError(error)
  }
}

watch(month, refresh)
watch(() => filters.course_id, refresh)
onMounted(refresh)
</script>

<template>
  <section class="screen history-screen">
    <AppHeader v-if="fromCourse" title="История приёмов" back @back="go('course-detail')" />
    <div v-else class="history-heading">
      <span>Архив приёмов</span>
      <h1 class="title">История</h1>
      <p>Выберите день, чтобы посмотреть записи</p>
    </div>

    <div class="history-filter">
      <label for="history-course">Лекарство</label>
      <select id="history-course" v-model="filters.course_id">
        <option value="">Все лекарства</option>
        <option v-for="course in state.courses" :key="course.id" :value="course.id">{{ course.name }}</option>
      </select>
    </div>

    <div class="history-calendar-card">
      <div class="month-heading history-month-heading">
        <button type="button" aria-label="Предыдущий месяц" @click="changeMonth(-1)">‹</button>
        <h2>{{ monthTitle(month) }}</h2>
        <button type="button" aria-label="Следующий месяц" @click="changeMonth(1)">›</button>
      </div>
      <div class="calendar-grid history-calendar-grid">
        <div v-for="day in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']" :key="day" class="weekday">{{ day }}</div>
        <button
          v-for="item in days"
          :key="item.value"
          class="history-day"
          :class="{ other: !item.current, selected: item.value === selected, marked: intakeDates.has(item.value) }"
          type="button"
          @click="selectDay(item)"
        >
          <span>{{ item.date.getDate() }}</span>
          <i v-if="intakeDates.has(item.value)"></i>
        </button>
      </div>
    </div>

    <div class="history-date-heading">
      <div>
        <span>Выбранный день</span>
        <strong>{{ selectedTitle }}</strong>
      </div>
      <b>{{ visibleIntakes.length }}</b>
    </div>

    <div class="history-list">
      <article v-for="item in visibleIntakes" :key="item.id" class="history-card">
        <div class="history-time">
          <strong>{{ formatTime(item.taken_at, state.user?.timezone) }}</strong>
          <span>{{ item.course_id ? 'курс' : 'разово' }}</span>
        </div>
        <button class="history-main" type="button" @click="edit(item)">
          <strong>{{ item.medicationName }}</strong>
          <span>{{ item.amount }} {{ item.unit }}</span>
          <small>{{ item.course_id ? 'Приём из курса' : 'Отдельная запись без курса' }}</small>
        </button>
        <button class="history-delete" type="button" aria-label="Удалить" @click="remove(item.id)">×</button>
      </article>
      <EmptyState v-if="!visibleIntakes.length" title="В этот день записей нет" text="Выберите отмеченную дату или добавьте приём в расписании" />
    </div>
  </section>
</template>
