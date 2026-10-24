<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import AppModal from '../components/ui/AppModal.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { go, loadCatalog, saveMedication, showError, toggleMedication } from '../store/store'
import { state } from '../store/state'

const search = ref('')
const category = ref('')
const medicationForm = ref('')
const selected = ref(null)
const adminModal = ref(false)
const editingId = ref(null)
const admin = computed(() => state.user?.role === 'admin')
const guest = computed(() => state.phase === 'guest')
const categories = computed(() => [...new Set(state.catalog.map(item => item.category).filter(Boolean))].sort())
const forms = computed(() => [...new Set(state.catalog.map(item => item.form).filter(Boolean))].sort())
const hasFilters = computed(() => Boolean(search.value || category.value || medicationForm.value))
const form = reactive({ name: '', internationalName: '', manufacturer: '', category: '', instructionUrl: '', form: '', strength: '', isActive: true })
let searchTimer

async function refresh() {
  try {
    await loadCatalog({ search: search.value, category: category.value, form: medicationForm.value })
  } catch (error) {
    showError(error)
  }
}

function delayedRefresh() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(refresh, 300)
}

function clearFilters() {
  search.value = ''
  category.value = ''
  medicationForm.value = ''
  refresh()
}

function addToCourses(item) {
  state.coursePreset = item
  go('course-form')
}

function openAdmin(item = null) {
  editingId.value = item?.id || null
  Object.assign(form, item ? {
    name: item.name,
    internationalName: item.international_name || '',
    manufacturer: item.manufacturer || '',
    category: item.category || '',
    instructionUrl: item.instruction_url || '',
    form: item.form || '',
    strength: item.strength || '',
    isActive: item.is_active,
  } : { name: '', internationalName: '', manufacturer: '', category: '', instructionUrl: '', form: '', strength: '', isActive: true })
  adminModal.value = true
}

async function submitAdmin() {
  try {
    await saveMedication(form, editingId.value)
    adminModal.value = false
  } catch (error) {
    showError(error)
  }
}

async function toggle(item) {
  try {
    await toggleMedication(item)
    if (selected.value?.id === item.id) selected.value = state.catalog.find(value => value.id === item.id)
  } catch (error) {
    showError(error)
  }
}

function closeGuest() {
  state.phase = 'auth'
  state.page = 'calendar'
}

onMounted(refresh)
</script>

<template>
  <section class="screen" :class="{ 'no-nav guest-screen': guest }">
    <AppHeader v-if="guest" title="Справочник" back @back="closeGuest" />
    <h1 v-else class="title">Справочник</h1>
    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m16 16 4 4"/></svg>
      <input v-model.trim="search" class="search" placeholder="Название или действующее вещество" @input="delayedRefresh">
      <button v-if="search" type="button" aria-label="Очистить поиск" @click="search = ''; refresh()">×</button>
    </div>
    <div class="filter-panel">
      <label><span>Категория</span><select v-model="category" @change="refresh"><option value="">Все</option><option v-for="item in categories" :key="item">{{ item }}</option></select></label>
      <label><span>Форма выпуска</span><select v-model="medicationForm" @change="refresh"><option value="">Все</option><option v-for="item in forms" :key="item">{{ item }}</option></select></label>
    </div>
    <div class="catalog-summary">
      <span>{{ state.catalog.length ? `Найдено: ${state.catalog.length}` : 'Результатов нет' }}</span>
      <button v-if="hasFilters" type="button" @click="clearFilters">Сбросить</button>
    </div>
    <button v-if="admin" class="secondary-button admin-add" type="button" @click="openAdmin()"><span>＋</span> Добавить лекарство</button>
    <div class="catalog-list">
      <article v-for="item in state.catalog" :key="item.id" class="catalog-row" :class="{ inactive: !item.is_active }">
        <button class="catalog-main" type="button" @click="selected = item">
          <strong>{{ item.name }}</strong>
          <small v-if="item.international_name">{{ item.international_name }}</small>
          <span class="catalog-meta"><i v-if="item.form">{{ item.form }}</i><i v-if="item.strength">{{ item.strength }}</i></span>
        </button>
        <span v-if="!admin" class="row-arrow">›</span>
        <button v-if="admin" class="mini-button" type="button" aria-label="Изменить" @click="openAdmin(item)">✎</button>
      </article>
      <EmptyState
        v-if="!state.catalog.length"
        :title="hasFilters ? 'Ничего не найдено' : 'Справочник пуст'"
        :action="hasFilters ? 'Сбросить фильтры' : ''"
        @action="clearFilters"
      />
    </div>
  </section>
  <button v-if="guest" class="guest-bottom" type="button" @click="closeGuest">Войти в «Мою аптечку»</button>
  <AppModal v-if="selected" title="Информация о лекарстве" @close="selected = null">
    <div class="medication-detail">
      <h3 class="medicine-name">{{ selected.name }}</h3>
      <p v-if="selected.international_name" class="international-name">{{ selected.international_name }}</p>
      <div class="detail-card info-grid">
        <template v-if="selected.manufacturer"><span class="info-label">Производитель</span><span>{{ selected.manufacturer }}</span></template>
        <template v-if="selected.category"><span class="info-label">Категория</span><span>{{ selected.category }}</span></template>
        <template v-if="selected.form"><span class="info-label">Форма</span><span>{{ selected.form }}</span></template>
        <template v-if="selected.strength"><span class="info-label">Дозировка</span><span>{{ selected.strength }}</span></template>
      </div>
      <a v-if="selected.instruction_url" class="secondary-button link-button" :href="selected.instruction_url" target="_blank" rel="noreferrer">Открыть инструкцию</a>
      <button v-if="!guest && selected.is_active" class="primary-button" type="button" @click="addToCourses(selected)">Добавить в мои лекарства</button>
      <div v-if="admin" class="button-row"><button class="secondary-button" type="button" @click="openAdmin(selected)">Изменить</button><button class="secondary-button danger-text" type="button" @click="toggle(selected)">{{ selected.is_active ? 'Скрыть' : 'Опубликовать' }}</button></div>
    </div>
  </AppModal>
  <AppModal v-if="adminModal" :title="editingId ? 'Изменить лекарство' : 'Новое лекарство'" @close="adminModal = false">
    <form class="admin-form" @submit.prevent="submitAdmin">
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Основное</span><strong>Название и группа</strong></div>
        <label class="field-label">Название</label>
        <input v-model.trim="form.name" class="detail-field" required placeholder="Например, Маалокс">
        <label class="field-label">Международное название</label>
        <input v-model.trim="form.internationalName" class="detail-field" placeholder="Действующее вещество">
        <label class="field-label">Категория</label>
        <input v-model.trim="form.category" class="detail-field" placeholder="Например, антацид">
      </div>
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Описание</span><strong>Форма и дозировка</strong></div>
        <label class="field-label">Производитель</label>
        <input v-model.trim="form.manufacturer" class="detail-field" placeholder="Название производителя">
        <div class="two-columns">
          <label>Форма<input v-model.trim="form.form" class="detail-field" placeholder="Таблетки"></label>
          <label>Дозировка<input v-model.trim="form.strength" class="detail-field" placeholder="500 мг"></label>
        </div>
        <label class="field-label">Инструкция</label>
        <input v-model.trim="form.instructionUrl" class="detail-field" type="url" placeholder="https://...">
      </div>
      <label v-if="editingId" class="toggle-row"><span>Опубликовано</span><input v-model="form.isActive" type="checkbox"></label>
      <div class="modal-actions"><button class="action-button" type="button" @click="adminModal = false">Отмена</button><button class="action-button primary" type="submit">Сохранить</button></div>
    </form>
  </AppModal>
</template>
