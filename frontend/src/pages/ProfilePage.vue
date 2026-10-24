<script setup>
import { computed, reactive } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import { go, saveProfile, showError } from '../store/store'
import { state } from '../store/state'

const form = reactive({
  name: state.user?.name || '',
  birthDate: state.user?.birth_date || '',
  avatarUrl: state.user?.avatar_url || '',
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
    <img v-if="form.avatarUrl" class="profile-avatar image-avatar" :src="form.avatarUrl" alt="">
    <div v-else class="profile-avatar">{{ initials }}</div>
    <form @submit.prevent="submit">
      <label class="field-label">Имя</label>
      <input v-model.trim="form.name" class="detail-field">
      <label class="field-label">Почта</label>
      <input class="detail-field" :value="state.user?.email" readonly>
      <label class="field-label">Дата рождения</label>
      <input v-model="form.birthDate" class="detail-field" type="date">
      <label class="field-label">Ссылка на аватар</label>
      <input v-model.trim="form.avatarUrl" class="detail-field" type="url">
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
      <button class="primary-button form-submit" type="submit">Сохранить</button>
    </form>
  </section>
</template>
