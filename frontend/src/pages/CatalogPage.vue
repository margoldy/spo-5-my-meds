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
  <section class="screen" :class="{ 'no-nav': guest }">
    <AppHeader v-if="guest" title="Справочник" back @back="closeGuest" />
    <h1 v-else class="title">Справочник</h1>
    <input v-model.trim="search" class="search" placeholder="Найти лекарство..." @input="delayedRefresh">
    <div class="filter-row">
      <select v-model="category" @change="refresh"><option value="">Все категории</option><option v-for="item in categories" :key="item">{{ item }}</option></select>
      <select v-model="medicationForm" @change="refresh"><option value="">Все формы</option><option v-for="item in forms" :key="item">{{ item }}</option></select>
    </div>
    <button v-if="admin" class="secondary-button admin-add" type="button" @click="openAdmin()">+ Добавить в справочник</button>
    <div class="catalog-list">
      <article v-for="item in state.catalog" :key="item.id" class="catalog-row" :class="{ inactive: !item.is_active }">
        <button class="catalog-main" type="button" @click="selected = item">
          <strong>{{ item.name }}<template v-if="item.international_name"> ({{ item.international_name }})</template></strong>
          <small v-if="item.strength">{{ item.strength }}</small>
        </button>
        <button v-if="admin" class="mini-button" type="button" aria-label="Изменить" @click="openAdmin(item)">✎</button>
      </article>
      <EmptyState v-if="!state.catalog.length" :text="search ? 'Ничего не найдено' : 'Справочник пока пуст'" />
    </div>
  </section>
  <button v-if="guest" class="guest-bottom" type="button" @click="closeGuest">Войти</button>
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
      <input v-model.trim="form.name" class="detail-field" required placeholder="Название">
      <input v-model.trim="form.internationalName" class="detail-field" placeholder="Международное название">
      <input v-model.trim="form.manufacturer" class="detail-field" placeholder="Производитель">
      <input v-model.trim="form.category" class="detail-field" placeholder="Категория">
      <input v-model.trim="form.form" class="detail-field" placeholder="Форма">
      <input v-model.trim="form.strength" class="detail-field" placeholder="Дозировка">
      <input v-model.trim="form.instructionUrl" class="detail-field" type="url" placeholder="Ссылка на инструкцию">
      <label v-if="editingId" class="toggle-row"><span>Опубликовано</span><input v-model="form.isActive" type="checkbox"></label>
      <div class="modal-actions"><button class="action-button" type="button" @click="adminModal = false">Отмена</button><button class="action-button primary" type="submit">Сохранить</button></div>
    </form>
  </AppModal>
</template>
