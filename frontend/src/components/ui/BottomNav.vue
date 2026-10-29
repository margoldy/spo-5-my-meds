<script setup>
defineProps({ active: String })
defineEmits(['change'])
</script>

<template>
  <nav class="bottom-nav">
    <button class="nav-button schedule-tab" :class="{ active: active === 'calendar' }" type="button" aria-label="Расписание" @click="$emit('change', 'calendar')">
      <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></svg>
      <span>Расписание</span>
    </button>
    <button class="nav-button" :class="{ active: active === 'courses' }" type="button" aria-label="Мои лекарства" @click="$emit('change', 'courses')">
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8"/><path d="M7.5 16.5l9-9"/></svg>
      <span>Лекарства</span>
    </button>
    <button class="nav-button history-tab" :class="{ active: active === 'history' }" type="button" aria-label="История" @click="$emit('change', 'history')">
      <svg viewBox="0 0 24 24" fill="none"><path d="M4 12a8 8 0 1 0 2.3-5.7L4 8.6M4 4v4.6h4.6M12 7.5V12l3 2"/></svg>
      <span>История</span>
    </button>
    <button class="nav-button" :class="{ active: active === 'settings' }" type="button" aria-label="Настройки" @click="$emit('change', 'settings')">
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3"/><path d="M19 13.8l1.2 1-.9 2.2-1.6-.1-1.2 1.2.1 1.6-2.2.9-1-1.2h-1.7l-1 1.2-2.2-.9.1-1.6-1.2-1.2-1.6.1-.9-2.2 1.2-1v-1.7l-1.2-1L6 9l1.6.1 1.2-1.2-.1-1.6 2.2-.9 1 1.2h1.7l1-1.2 2.2.9-.1 1.6L18 9.1l1.6-.1.9 2.2-1.2 1z"/></svg>
      <span>Настройки</span>
    </button>
  </nav>
</template>
