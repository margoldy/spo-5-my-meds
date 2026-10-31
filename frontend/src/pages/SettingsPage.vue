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
    <span class="menu-caption">Напоминания</span>
    <section class="settings-section">
      <label class="toggle-row">
        <span><strong>Уведомления</strong><small class="reminder-hint">Напоминать о ближайшем приёме</small></span>
        <input :checked="state.preferences.notifications && notificationAllowed" type="checkbox" @change="changeNotifications($event.target.checked)">
      </label>
      <label class="setting-line">
        <span class="setting-line-copy">
          <strong>Время</strong>
          <small class="reminder-hint">Когда прислать уведомление</small>
        </span>
        <select :value="state.preferences.reminderMinutes" class="setting-line-select" @change="changePreference('reminderMinutes', Number($event.target.value))">
          <option :value="5">за 5 минут</option>
          <option :value="10">за 10 минут</option>
          <option :value="15">за 15 минут</option>
          <option :value="30">за 30 минут</option>
          <option :value="60">за 1 час</option>
        </select>
      </label>
    </section>
    <span class="menu-caption">Данные и безопасность</span>
    <div class="menu-list">
      <button type="button" @click="go('emergency-card')">
        <span class="menu-icon emergency-menu-icon"><img src="../assets/icons/med_cross.svg" alt=""></span>
        <span class="menu-copy"><strong>Медицинская карточка</strong><small>Аллергии и активные лекарства</small></span>
        <span class="row-arrow">›</span>
      </button>

      <button type="button" @click="passwordModal = true">
        <span class="menu-icon"><img src="../assets/icons/lock.svg" alt=""></span>
        <span class="menu-copy"><strong>Пароль шифрования</strong><small>Изменить пароль</small></span>
        <span class="row-arrow">›</span>
      </button>

      <button type="button" @click="forget">
        <span class="menu-icon"><img src="../assets/icons/refresh.svg" alt=""></span>
        <span class="menu-copy"><strong>Забыть устройство</strong><small>Удалить локальный ключ</small></span>
        <span class="row-arrow">›</span>
      </button>

      <button class="danger-text" type="button" @click="logout">
        <span class="menu-icon"><img src="../assets/icons/logout.svg" alt=""></span>
        <span class="menu-copy"><strong>Выйти</strong><small>Выход из аккаунта</small></span>
        <span class="row-arrow">›</span>
      </button>
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
