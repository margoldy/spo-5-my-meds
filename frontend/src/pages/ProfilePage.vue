<script setup>
import { computed, reactive } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import { go, saveProfile, showError } from '../store/store'
import { state } from '../store/state'

const form = reactive({
  name: state.user?.name || '',
  birthDate: state.user?.birth_date || '',
  timezone: state.user?.timezone || 'Europe/Moscow',
})
const initials = computed(() => (form.name || state.user?.email || '?').trim().slice(0, 2).toUpperCase())

async function submit() {
  try {
    await saveProfile(form)
    go('settings')
  } catch (error) {
    showError(error)
  }
}
</script>

<template>
  <section class="screen no-nav">
    <AppHeader title="Профиль" back @back="go('settings')" />
    <div class="profile-hero">
      <div class="profile-avatar">{{ initials }}</div>
      <strong>{{ form.name || 'Как вас зовут?' }}</strong>
      <span>{{ state.user?.email }}</span>
    </div>
    <form @submit.prevent="submit">
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Основное</span><strong>Личные данные</strong></div>
        <label class="field-label">Имя</label>
        <input v-model.trim="form.name" class="detail-field" placeholder="Ваше имя">
        <label class="field-label">Почта</label>
        <input class="detail-field" :value="state.user?.email" readonly>
        <p class="field-hint">Изменить почту нельзя</p>
        <label class="field-label">Дата рождения</label>
        <input v-model="form.birthDate" class="detail-field" type="date">
      </div>
      <div class="form-section">
        <div class="form-section-heading"><span class="section-kicker">Настройки</span><strong>Часовой пояс</strong></div>
        <label class="field-label">Часовой пояс</label>
        <select v-model="form.timezone" class="detail-field">
          <option value="Europe/Moscow">Москва</option>
          <option value="Europe/Kaliningrad">Калининград</option>
          <option value="Asia/Yekaterinburg">Екатеринбург</option>
          <option value="Asia/Omsk">Омск</option>
          <option value="Asia/Krasnoyarsk">Красноярск</option>
          <option value="Asia/Irkutsk">Иркутск</option>
          <option value="Asia/Yakutsk">Якутск</option>
          <option value="Asia/Vladivostok">Владивосток</option>
        </select>
      </div>
      <button class="primary-button form-submit" type="submit">Сохранить</button>
    </form>
  </section>
</template>
