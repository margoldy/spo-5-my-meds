<script setup>
import { ref } from 'vue'
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
    <div class="brand-mark"><span></span></div>
    <h1 class="title">Моя аптечка</h1>
    <p class="auth-text">Лекарства, расписание и история приёмов в одном месте</p>
    <form v-if="step === 'email'" @submit.prevent="sendCode">
      <label class="field-label">Электронная почта</label>
      <input v-model.trim="email" class="detail-field" type="email" autocomplete="email" required placeholder="name@example.com">
      <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Отправляем...' : 'Получить код' }}</button>
    </form>
    <form v-else @submit.prevent="signIn">
      <p class="auth-text">Код отправлен на {{ email }}</p>
      <input v-model="code" class="code-input" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="\d{6}" required aria-label="Код из письма">
      <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Проверяем...' : 'Войти' }}</button>
      <button class="text-button" type="button" @click="step = 'email'; code = ''">Изменить почту</button>
    </form>
  </section>
</template>
