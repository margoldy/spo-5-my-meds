<script setup>
import { onMounted, reactive } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { formatDateTime, zonedDateTimeToIso } from '../utils/date'
import { go, loadIntakes, removeIntake, showError } from '../store/store'
import { state } from '../store/state'

const filters = reactive({ course_id: state.previousPage === 'course-detail' ? state.selectedCourseId : '', from: '', to: '' })

async function refresh() {
  try {
    const values = {}
    if (filters.course_id) values.course_id = filters.course_id
    if (filters.from) values.from = zonedDateTimeToIso(`${filters.from}T00:00:00`, state.user?.timezone)
    if (filters.to) values.to = zonedDateTimeToIso(`${filters.to}T23:59:59.999`, state.user?.timezone)
    await loadIntakes(values)
  } catch (error) {
    showError(error)
  }
}

function edit(item) {
  state.selectedIntakeId = item.id
  go('intake-form')
}

async function remove(id) {
  if (!confirm('Удалить запись о приёме?')) return
  try {
    await removeIntake(id)
  } catch (error) {
    showError(error)
  }
}

onMounted(refresh)
</script>

<template>
  <section class="screen no-nav">
    <AppHeader title="История приёмов" back @back="go(state.previousPage === 'course-detail' ? 'course-detail' : 'settings')" />
    <div class="form-section history-filters">
      <div class="form-section-heading"><span class="section-kicker">Фильтры</span><strong>Что показать</strong></div>
      <label class="field-label">Лекарство</label>
      <select v-model="filters.course_id" class="detail-field" @change="refresh">
        <option value="">Все лекарства</option>
        <option v-for="course in state.courses" :key="course.id" :value="course.id">{{ course.name }}</option>
      </select>
      <div class="two-columns history-dates">
        <label>С<input v-model="filters.from" class="detail-field" type="date" @change="refresh"></label>
        <label>По<input v-model="filters.to" class="detail-field" type="date" @change="refresh"></label>
      </div>
    </div>
    <div class="history-list">
      <article v-for="item in state.intakes" :key="item.id" class="history-card">
        <button class="history-main" type="button" @click="edit(item)">
          <strong>{{ item.medicationName }}</strong>
          <span>{{ item.amount }} {{ item.unit }}</span>
          <small>{{ formatDateTime(item.taken_at, state.user?.timezone) }}</small>
          <small>{{ item.course_id ? 'Из курса' : 'Разовая запись' }}</small>
        </button>
        <button class="mini-button danger" type="button" aria-label="Удалить" @click="remove(item.id)">×</button>
      </article>
      <EmptyState v-if="!state.intakes.length" title="Записей нет" />
    </div>
  </section>
</template>
