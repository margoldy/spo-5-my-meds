<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { calendarDays, dateInTimeZone, formatTime, isoDate, monthTitle } from '../utils/date'
import { cancelScheduled, go, loadDay, showError, takeScheduled } from '../store/store'
import { state } from '../store/state'

const initialDate = dateInTimeZone(new Date(), state.user?.timezone)
const selected = ref(initialDate)
const month = ref(new Date(`${initialDate}T12:00:00`))
const days = computed(() => calendarDays(month.value))
const groupedItems = computed(() => state.dayItems.slice().sort((a, b) => a.planned_at.localeCompare(b.planned_at)))

async function refresh() {
  try {
    await loadDay(selected.value)
  } catch (error) {
    showError(error)
  }
}

function changeMonth(direction) {
  month.value = new Date(month.value.getFullYear(), month.value.getMonth() + direction, 1)
  selected.value = isoDate(month.value)
}

function selectDay(item) {
  selected.value = item.value
  if (!item.current) month.value = new Date(item.date.getFullYear(), item.date.getMonth(), 1)
}

function openCourse(id) {
  state.selectedCourseId = id
  go('course-detail')
}

function openUnplanned() {
  state.selectedIntakeId = null
  go('intake-form')
}

async function toggleIntake(item) {
  try {
    if (item.intake) await cancelScheduled(item)
    else await takeScheduled(item)
    await refresh()
  } catch (error) {
    showError(error)
  }
}

watch(selected, refresh)
onMounted(refresh)
</script>

<template>
  <section class="screen schedule-screen">
    <div class="schedule-intro">
      <span>План приёмов</span>
      <strong>Что принять сегодня</strong>
    </div>
    <div class="month-heading">
      <button type="button" aria-label="Предыдущий месяц" @click="changeMonth(-1)">‹</button>
      <h1 class="title">{{ monthTitle(month) }}</h1>
      <button type="button" aria-label="Следующий месяц" @click="changeMonth(1)">›</button>
    </div>
    <div class="calendar schedule-calendar">
      <div class="calendar-grid">
        <div v-for="day in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']" :key="day" class="weekday">{{ day }}</div>
        <button v-for="item in days" :key="item.value" class="day" :class="{ other: !item.current, selected: item.value === selected }" type="button" @click="selectDay(item)">{{ item.date.getDate() }}</button>
      </div>
    </div>
    <button class="inline-action" type="button" @click="openUnplanned">+ Внеплановый приём</button>
    <EmptyState v-if="!groupedItems.length" title="Приёмов нет" action="Записать внеплановый приём" @action="openUnplanned" />
    <section v-for="item in groupedItems" :key="item.schedule_id" class="time-group">
      <h2 class="time-label">{{ item.planned_at.slice(11, 16) }}</h2>
      <article class="intake-card">
        <button class="intake-main plain-card-button" type="button" @click="openCourse(item.course_id)">
          <span class="medicine-name">{{ item.courseData.name }}</span>
          <span class="dose">{{ item.intakeData?.amount ?? item.scheduleData.amount }} {{ item.intakeData?.unit ?? item.scheduleData.unit }}</span>
          <span v-if="item.intake" class="taken-at">Принято в {{ formatTime(item.intake.taken_at, state.user?.timezone) }}</span>
        </button>
        <button class="check-button" :class="{ taken: item.intake }" type="button" :aria-label="item.intake ? 'Отменить приём' : 'Отметить приём'" @click="toggleIntake(item)">
          <svg v-if="item.intake" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><path d="M12 5v14M5.9 8.5l12.2 7M18.1 8.5l-12.2 7"/></svg>
        </button>
      </article>
    </section>
  </section>
</template>
