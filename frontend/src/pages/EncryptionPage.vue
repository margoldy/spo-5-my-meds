<script setup>
import { computed, ref } from 'vue'
import { logout, setupEncryption, showError, unlockEncryption } from '../store/store'
import { state } from '../store/state'

const password = ref('')
const confirmation = ref('')
const title = computed(() => state.encryptionExists ? 'Открыть данные' : 'Защитить данные')

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
    <div class="brand-mark"><span></span></div>
    <h1 class="title">{{ title }}</h1>
    <p class="auth-text" v-if="state.encryptionExists">Введите пароль шифрования, чтобы открыть медицинские записи на этом устройстве.</p>
    <p class="auth-text" v-else>Создайте отдельный пароль шифрования. Он потребуется при входе с нового устройства.</p>
    <form @submit.prevent="submit">
      <label class="field-label">Пароль шифрования</label>
      <input v-model="password" class="detail-field" type="password" autocomplete="current-password" required>
      <template v-if="!state.encryptionExists">
        <label class="field-label">Повторите пароль</label>
        <input v-model="confirmation" class="detail-field" type="password" autocomplete="new-password" required>
      </template>
      <button class="primary-button" :disabled="state.busy">{{ state.busy ? 'Подождите...' : state.encryptionExists ? 'Открыть' : 'Сохранить пароль' }}</button>
      <button class="text-button" type="button" @click="logout">Выйти из аккаунта</button>
    </form>
  </section>
</template>
