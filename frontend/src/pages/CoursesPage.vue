<script setup>
import { computed, onMounted, ref } from 'vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { daysText, formatDate } from '../utils/date'
import { go, loadCourses, showError } from '../store/store'
import { state } from '../store/state'

const query = ref('')
const filtered = computed(() => state.courses.filter(item => item.name.toLowerCase().includes(query.value.toLowerCase())))

function openCourse(id) {
  state.selectedCourseId = id
  go('course-detail')
}

function addCourse() {
  state.coursePreset = null
  go('course-form')
}

onMounted(async () => {
  try {
    await loadCourses()
  } catch (error) {
    showError(error)
  }
})
</script>

<template>
  <section class="screen">
    <div class="page-title-row">
      <h1 class="title">Мои лекарства</h1>
      <button class="catalog-shortcut" type="button" @click="go('catalog')">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 5.5c3.4-.8 6.4 0 9 2.2v12c-2.6-2.2-5.6-3-9-2.2zM21 5.5c-3.4-.8-6.4 0-9 2.2v12c2.6-2.2 5.6-3 9-2.2z"/></svg>
        <span>Справочник</span>
      </button>
    </div>
    <input v-model.trim="query" class="search" placeholder="Найти лекарство...">
    <div class="course-list">
      <article v-for="course in filtered" :key="course.id" class="course-card" :class="{ inactive: !course.is_active }" @click="openCourse(course.id)">
        <div class="card-heading">
          <h2 class="medicine-name">{{ course.name }}</h2>
          <span v-if="!course.is_active" class="badge">Завершён</span>
        </div>
        <div class="info-grid">
          <span class="info-label">Частота</span>
          <span>{{ course.schedules.length ? daysText([...new Set(course.schedules.flatMap(item => item.days_of_week))]) : 'По необходимости' }}</span>
          <template v-if="course.schedules.length">
            <span class="info-label">Время</span>
            <span><template v-for="schedule in course.schedules" :key="schedule.id">{{ schedule.time }} — {{ schedule.amount }} {{ schedule.unit }}<br></template></span>
          </template>
          <span class="info-label">Длительность</span>
          <span>Начало: {{ formatDate(course.start_date) }}<br v-if="course.end_date">{{ course.end_date ? `Конец: ${formatDate(course.end_date)}` : '' }}</span>
        </div>
      </article>
      <EmptyState
        v-if="!filtered.length"
        :title="query ? 'Ничего не найдено' : 'Лекарств нет'"
        :action="query ? '' : 'Добавить лекарство'"
        @action="addCourse"
      />
    </div>
  </section>
  <button class="floating-button" type="button" aria-label="Добавить лекарство" @click="addCourse">+</button>
</template>
