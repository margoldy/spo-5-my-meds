<script setup>
import { ref } from 'vue'
import temporaryLogo from '../assets/temporary-logo.png'
import { openGuestCatalog, requestAuthCode, showError, verifyAuthCode } from '../store/store'
import { state } from '../store/state'

const step = ref('email')
const email = ref('')
const code = ref('')

async function sendCode() {
  try {
    await requestAuthCode(email.value)
    step.value = 'code'
  } catch (error) {
    showError(error)
  }
}

async function signIn() {
  try {
    await verifyAuthCode(email.value, code.value)
  } catch (error) {
    showError(error)
  }
}

async function continueAsGuest() {
  try {
    await openGuestCatalog()
  } catch (error) {
    showError(error)
  }
}
</script>

<template>
  <section class="auth-screen">
    <button class="guest-login" type="button" @click="continueAsGuest">Справочник без входа</button>
    <div class="auth-brand">
      <img class="brand-logo" :src="temporaryLogo" alt="Логотип приложения">
      <h1 class="title">Моя аптечка</h1>
    </div>
    <div class="auth-card">
      <form v-if="step === 'email'" @submit.prevent="sendCode">
        <div class="auth-card-heading">
          <span class="auth-step">Вход</span>
        </div>
        <label class="auth-field-label" for="auth-email">Электронная почта</label>
        <div class="auth-input">
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>
          <input id="auth-email" v-model.trim="email" type="email" autocomplete="email" required placeholder="name@example.com">
        </div>
        <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Отправляем...' : 'Получить код' }}</button>
      </form>
      <form v-else @submit.prevent="signIn">
        <div class="auth-card-heading">
          <span class="auth-step">Введите код</span>
          <p>Код отправлен на <strong>{{ email }}</strong></p>
        </div>
        <input v-model="code" class="code-input" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="\d{6}" required aria-label="Код из письма" placeholder="000000">
        <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Проверяем...' : 'Войти' }}</button>
        <button class="text-button" type="button" @click="step = 'email'; code = ''">Указать другую почту</button>
      </form>
    </div>
  </section>
</template>
