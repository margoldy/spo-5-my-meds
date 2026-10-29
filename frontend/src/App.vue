<script setup>
import { computed, onMounted } from 'vue'
import temporaryLogo from './assets/temporary-logo.png'
import BottomNav from './components/ui/BottomNav.vue'
import AuthPage from './pages/AuthPage.vue'
import CalendarPage from './pages/CalendarPage.vue'
import CatalogPage from './pages/CatalogPage.vue'
import CourseDetailPage from './pages/CourseDetailPage.vue'
import CourseFormPage from './pages/CourseFormPage.vue'
import CoursesPage from './pages/CoursesPage.vue'
import EncryptionPage from './pages/EncryptionPage.vue'
import HistoryPage from './pages/HistoryPage.vue'
import IntakeFormPage from './pages/IntakeFormPage.vue'
import ProgressPage from './pages/ProgressPage.vue'
import EmergencyCardPage from './pages/EmergencyCardPage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import SettingsPage from './pages/SettingsPage.vue'
import { bootstrap, go } from './store/store'
import { state } from './store/state'

const pages = {
  calendar: CalendarPage,
  courses: CoursesPage,
  'course-detail': CourseDetailPage,
  'course-form': CourseFormPage,
  catalog: CatalogPage,
  'intake-form': IntakeFormPage,
  history: HistoryPage,
  progress: ProgressPage,
  'emergency-card': EmergencyCardPage,
  profile: ProfilePage,
  settings: SettingsPage,
}

const currentPage = computed(() => pages[state.page] || CalendarPage)
const hasNavigation = computed(() => state.phase === 'app' && ['calendar', 'courses', 'history', 'settings'].includes(state.page))

onMounted(bootstrap)
</script>

<template>
  <main class="phone">
    <div v-if="state.phase === 'loading'" class="loading-screen">
      <img class="brand-logo" :src="temporaryLogo" alt="">
      <p>Загрузка...</p>
    </div>
    <AuthPage v-else-if="state.phase === 'auth'" />
    <EncryptionPage v-else-if="state.phase === 'encryption'" />
    <component :is="currentPage" v-else />
    <BottomNav v-if="hasNavigation" :active="state.page" @change="go" />
    <div v-if="state.toast" class="toast">{{ state.toast }}</div>
  </main>
</template>
