<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import { calendarDays, dateInTimeZone, formatDate, isoDate, monthTitle, zonedDateTimeToIso } from '../utils/date'
import { go, loadIntakes, showError } from '../store/store'
import { state } from '../store/state'

const today = dateInTimeZone(new Date(), state.user?.timezone)
const month = ref(new Date(`${today}T12:00:00`))
const selected = ref(today)
const days = computed(() => calendarDays(month.value))
const courses = computed(() => state.courses)

function monthRange() {
  const first = new Date(month.value.getFullYear(), month.value.getMonth(), 1)
  const last = new Date(month.value.getFullYear(), month.value.getMonth() + 1, 0)
  return {
    from: zonedDateTimeToIso(`${isoDate(first)}T00:00:00`, state.user?.timezone),
    to: zonedDateTimeToIso(`${isoDate(last)}T23:59:59.999`, state.user?.timezone),
  }
}

function monthDates() {
  const first = new Date(month.value.getFullYear(), month.value.getMonth(), 1)
  const last = new Date(month.value.getFullYear(), month.value.getMonth() + 1, 0)
  const result = []
  for (const date = new Date(first); date <= last; date.setDate(date.getDate() + 1)) result.push(isoDate(date))
  return result
}

function weekDay(value) {
  const day = new Date(`${value}T12:00:00`).getDay()
  return day === 0 ? 7 : day
}

const intakeMap = computed(() => {
  const result = new Map()
  state.intakes.forEach(item => {
    if (!item.schedule_id) return
    const date = dateInTimeZone(new Date(item.taken_at), state.user?.timezone)
    result.set(`${item.schedule_id}|${date}`, item)
  })
  return result
})

const occurrences = computed(() => {
  const now = Date.now()
  return monthDates().flatMap(date => courses.value.flatMap(course => {
    if (date < course.start_date || (course.end_date && date > course.end_date)) return []
    return course.schedules
      .filter(schedule => schedule.days_of_week.includes(weekDay(date)))
      .map(schedule => {
        const plannedAt = zonedDateTimeToIso(`${date}T${schedule.time}:00`, state.user?.timezone)
        return {
          date,
          course,
          schedule,
          plannedAt,
          due: new Date(plannedAt).getTime() <= now,
          intake: intakeMap.value.get(`${schedule.id}|${date}`) || null,
        }
      })
  }))
})

const daySummary = computed(() => {
  const result = new Map()
  monthDates().forEach(date => {
    const planned = occurrences.value.filter(item => item.date === date)
    const taken = planned.filter(item => item.intake)
    const due = planned.filter(item => item.due)
    let status = ''
    if (planned.length) {
      if (taken.length === planned.length) status = 'complete'
      else if (taken.length) status = 'partial'
      else if (due.length) status = 'missed'
      else status = 'planned'
    }
    result.set(date, { planned: planned.length, taken: taken.length, due: due.length, status })
  })
  return result
})

const dueOccurrences = computed(() => occurrences.value.filter(item => item.due))
const hasDueData = computed(() => dueOccurrences.value.length > 0)
const completed = computed(() => dueOccurrences.value.filter(item => item.intake).length)
const adherence = computed(() => dueOccurrences.value.length ? Math.round(completed.value / dueOccurrences.value.length * 100) : 0)
const selectedSummary = computed(() => daySummary.value.get(selected.value) || { planned: 0, taken: 0, status: '' })

const streak = computed(() => {
  const scheduledDays = monthDates()
    .filter(date => date <= today && (daySummary.value.get(date)?.due || 0) > 0)
    .sort()
    .reverse()
  let result = 0
  for (const date of scheduledDays) {
    const day = daySummary.value.get(date)
    if (day.taken < day.due) break
    result += 1
  }
  return result
})

const bestCourse = computed(() => {
  const values = courses.value.map(course => {
    const planned = dueOccurrences.value.filter(item => item.course.id === course.id)
    const taken = planned.filter(item => item.intake).length
    return { name: course.name, total: planned.length, percent: planned.length ? Math.round(taken / planned.length * 100) : 0 }
  }).filter(item => item.total)
  return values.sort((a, b) => b.percent - a.percent || b.total - a.total)[0] || null
})

const missedPeriod = computed(() => {
  const missed = dueOccurrences.value.filter(item => !item.intake)
  if (!missed.length) return ''
  const periods = { morning: 0, day: 0, evening: 0 }
  missed.forEach(item => {
    const hour = Number(item.schedule.time.slice(0, 2))
    periods[hour < 12 ? 'morning' : hour < 18 ? 'day' : 'evening'] += 1
  })
  const [period, count] = Object.entries(periods).sort((a, b) => b[1] - a[1])[0]
  if (!count) return ''
  return { morning: 'утренние', day: 'дневные', evening: 'вечерние' }[period]
})

const insight = computed(() => {
  if (!dueOccurrences.value.length) return 'В выбранном месяце пока нет наступивших приёмов.'
  if (adherence.value === 100) return 'Все запланированные приёмы отмечены — отличный результат.'
  if (missedPeriod.value) return `Чаще остаются неотмеченными ${missedPeriod.value} приёмы.`
  return 'Отмечайте приёмы в расписании, и здесь появится более точная картина.'
})

async function refresh() {
  try {
    await loadIntakes(monthRange())
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

watch(month, refresh)
onMounted(refresh)
</script>

<template>
  <section class="screen no-nav progress-screen">
    <AppHeader title="Статистика" back @back="go('history')" />
    <div v-if="hasDueData" class="progress-hero">
      <div class="progress-ring" :style="{ '--progress': `${adherence * 3.6}deg` }">
        <div><strong>{{ adherence }}%</strong><span>соблюдение</span></div>
      </div>
      <div class="progress-hero-copy">
        <span>За {{ monthTitle(month).toLowerCase() }}</span>
        <strong>{{ completed }} из {{ dueOccurrences.length }}</strong>
        <small>наступивших приёмов отмечено</small>
      </div>
    </div>

    <div class="progress-calendar-card">
      <div class="month-heading progress-month-heading">
        <button type="button" aria-label="Предыдущий месяц" @click="changeMonth(-1)">‹</button>
        <h2>{{ monthTitle(month) }}</h2>
        <button type="button" aria-label="Следующий месяц" @click="changeMonth(1)">›</button>
      </div>
      <div class="calendar-grid progress-calendar-grid">
        <div v-for="day in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']" :key="day" class="weekday">{{ day }}</div>
        <button
          v-for="item in days"
          :key="item.value"
          class="progress-day"
          :class="[daySummary.get(item.value)?.status, { other: !item.current, selected: item.value === selected }]"
          type="button"
          @click="selectDay(item)"
        >{{ item.date.getDate() }}</button>
      </div>
      <div class="progress-legend">
        <span><i class="complete"></i>Принято</span>
        <span><i class="partial"></i>Частично</span>
        <span><i class="missed"></i>Пропущено</span>
        <span><i class="planned"></i>Впереди</span>
      </div>
    </div>

    <div v-if="selectedSummary.planned" class="selected-progress-day">
      <span>{{ formatDate(selected) }}</span>
      <strong>{{ selectedSummary.taken }} из {{ selectedSummary.planned }} приёмов</strong>
    </div>

    <div v-if="hasDueData" class="progress-stat-grid">
      <article><span class="stat-flower">✿</span><strong>{{ streak }}</strong><small>дней подряд без пропусков</small></article>
      <article><span class="stat-check">✓</span><strong>{{ state.intakes.length }}</strong><small>всего записей за месяц</small></article>
    </div>

    <article v-if="hasDueData && bestCourse" class="progress-favorite">
      <span>Самый стабильный курс</span>
      <strong>{{ bestCourse.name }}</strong>
      <small>{{ bestCourse.percent }}% запланированных приёмов отмечено</small>
    </article>
    <article v-if="hasDueData" class="progress-insight">
      <span>Наблюдение</span>
      <p>{{ insight }}</p>
    </article>
    <div v-else class="progress-empty">
      <span>✿</span>
      <strong>Пока нечего считать</strong>
      <p>Здесь появится статистика после первых запланированных приёмов.</p>
    </div>
  </section>
</template>
