<script setup>
import { computed, ref } from 'vue'
import temporaryLogo from '../assets/temporary-logo.png'
import { logout, setupEncryption, showError, unlockEncryption } from '../store/store'
import { state } from '../store/state'

const password = ref('')
const confirmation = ref('')
const title = computed(() => state.encryptionExists ? 'Введите пароль' : 'Создайте пароль')

async function submit() {
  try {
    if (!state.encryptionExists && password.value !== confirmation.value) throw new Error('Пароли не совпадают')
    if (password.value.length < 8) throw new Error('Пароль должен содержать не меньше 8 символов')
    if (state.encryptionExists) await unlockEncryption(password.value)
    else await setupEncryption(password.value)
  } catch (error) {
    showError(error)
  }
}
</script>

<template>
  <section class="auth-screen">
    <img class="brand-logo" :src="temporaryLogo" alt="Логотип приложения">
    <h1 class="title">{{ title }}</h1>
    <div class="auth-card encryption-card">
      <div class="security-note"><span>◇</span><p>{{ state.encryptionExists ? 'Пароль не отправляется на сервер' : 'Не забудьте пароль — восстановить его нельзя' }}</p></div>
      <form @submit.prevent="submit">
        <label class="field-label">Пароль шифрования</label>
        <input v-model="password" class="detail-field" type="password" autocomplete="current-password" required placeholder="Не меньше 8 символов">
        <template v-if="!state.encryptionExists">
          <label class="field-label">Повторите пароль</label>
          <input v-model="confirmation" class="detail-field" type="password" autocomplete="new-password" required placeholder="Повторите пароль">
        </template>
        <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Подождите...' : state.encryptionExists ? 'Открыть данные' : 'Сохранить пароль' }}</button>
        <button class="text-button" type="button" @click="logout">Выйти из аккаунта</button>
      </form>
    </div>
  </section>
</template>
