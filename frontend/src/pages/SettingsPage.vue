<script setup>
import { computed, reactive, ref } from 'vue'
import AppModal from '../components/ui/AppModal.vue'
import { changeEncryptionPassword, forgetDevice, go, logout, showError, updatePreferences } from '../store/store'
import { state } from '../store/state'
import { requestNotifications } from '../utils/notifications'

const passwordModal = ref(false)
const passwords = reactive({ current: '', next: '', confirmation: '' })
const initials = computed(() => (state.user?.name || state.user?.email || '?').trim().slice(0, 2).toUpperCase())
const notificationAllowed = ref(typeof Notification !== 'undefined' && Notification.permission === 'granted')

function changePreference(name, value) {
  updatePreferences({ [name]: value })
}

async function changeNotifications(value) {
  if (!value) return changePreference('notifications', false)
  const allowed = await requestNotifications()
  notificationAllowed.value = allowed
  changePreference('notifications', allowed)
  if (!allowed) showError(new Error('Браузер не разрешил уведомления'))
}

async function submitPassword() {
  try {
    if (passwords.next.length < 8) throw new Error('Новый пароль должен содержать не меньше 8 символов')
    if (passwords.next !== passwords.confirmation) throw new Error('Новые пароли не совпадают')
    await changeEncryptionPassword(passwords.current, passwords.next)
    passwordModal.value = false
    Object.assign(passwords, { current: '', next: '', confirmation: '' })
  } catch (error) {
    showError(error)
  }
}

async function forget() {
  if (!confirm('Забыть ключ на этом устройстве? Для открытия данных потребуется пароль шифрования.')) return
  try {
    await forgetDevice()
  } catch (error) {
    showError(error)
  }
}
</script>

<template>
  <section class="screen">
    <h1 class="title">Настройки</h1>
    <button class="settings-card" type="button" @click="go('profile')">
      <span class="avatar">{{ initials }}</span>
      <span><strong>{{ state.user?.name || 'Без имени' }}</strong><small>{{ state.user?.email }}</small></span>
      <span class="row-arrow">›</span>
    </button>
    <section class="settings-section">
      <div class="form-section-heading"><span class="section-kicker">Расписание</span><strong>Напоминания</strong></div>
      <label class="toggle-row">
        <span><strong>Уведомления</strong><small>Напоминать о ближайшем приёме</small></span>
        <input :checked="state.preferences.notifications && notificationAllowed" type="checkbox" @change="changeNotifications($event.target.checked)">
      </label>
      <label class="field-label">За сколько минут</label>
      <select :value="state.preferences.reminderMinutes" class="detail-field" @change="changePreference('reminderMinutes', Number($event.target.value))">
        <option :value="5">5 минут</option>
        <option :value="10">10 минут</option>
        <option :value="15">15 минут</option>
        <option :value="30">30 минут</option>
        <option :value="60">1 час</option>
      </select>
    </section>
    <span class="menu-caption">Данные и безопасность</span>
    <div class="menu-list">
      <button type="button" @click="go('emergency-card')"><span class="menu-icon emergency-menu-icon"><svg viewBox="0 0 24 24"><path d="M12 3v18M3 12h18"/></svg></span><span class="menu-copy"><strong>Медицинская карточка</strong><small>Аллергии и активные лекарства</small></span><span class="row-arrow">›</span></button>
      <button type="button" @click="passwordModal = true"><span class="menu-icon"><svg viewBox="0 0 24 24"><rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v2"/></svg></span><span class="menu-copy"><strong>Пароль шифрования</strong><small>Изменить пароль</small></span><span class="row-arrow">›</span></button>
      <button type="button" @click="forget"><span class="menu-icon"><svg viewBox="0 0 24 24"><path d="M5 8a8 8 0 1 1-1 7M5 8V3M5 8h5"/></svg></span><span class="menu-copy"><strong>Забыть устройство</strong><small>Удалить локальный ключ</small></span><span class="row-arrow">›</span></button>
      <button class="danger-text" type="button" @click="logout"><span class="menu-icon"><svg viewBox="0 0 24 24"><path d="M10 5H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h4M14 8l4 4-4 4M18 12H9"/></svg></span><span class="menu-copy"><strong>Выйти</strong></span><span class="row-arrow">›</span></button>
    </div>
  </section>
  <AppModal v-if="passwordModal" title="Пароль шифрования" @close="passwordModal = false">
    <form @submit.prevent="submitPassword">
      <label class="field-label">Текущий пароль</label>
      <input v-model="passwords.current" class="detail-field" type="password" required>
      <label class="field-label">Новый пароль</label>
      <input v-model="passwords.next" class="detail-field" type="password" required>
      <label class="field-label">Повторите новый пароль</label>
      <input v-model="passwords.confirmation" class="detail-field" type="password" required>
      <div class="modal-actions"><button class="action-button" type="button" @click="passwordModal = false">Отмена</button><button class="action-button primary" type="submit">Сохранить</button></div>
    </form>
  </AppModal>
</template>
