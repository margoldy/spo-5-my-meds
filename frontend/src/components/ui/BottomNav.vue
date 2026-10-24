<script setup>
defineProps({ active: String })
defineEmits(['change'])
</script>

<template>
  <nav class="bottom-nav">
    <button class="nav-button" :class="{ active: active === 'calendar' }" type="button" aria-label="Календарь" @click="$emit('change', 'calendar')">
      <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></svg>
    </button>
    <button class="nav-button" :class="{ active: active === 'courses' }" type="button" aria-label="Мои лекарства" @click="$emit('change', 'courses')">
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8"/><path d="M7.5 16.5l9-9"/></svg>
    </button>
    <button class="nav-button" :class="{ active: active === 'catalog' }" type="button" aria-label="Справочник" @click="$emit('change', 'catalog')">
      <svg viewBox="0 0 24 24" fill="none"><path d="M3 5.5c3.4-.8 6.4 0 9 2.2v12c-2.6-2.2-5.6-3-9-2.2zM21 5.5c-3.4-.8-6.4 0-9 2.2v12c2.6-2.2 5.6-3 9-2.2z"/></svg>
    </button>
    <button class="nav-button" :class="{ active: active === 'settings' }" type="button" aria-label="Настройки" @click="$emit('change', 'settings')">
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3"/><path d="M19 13.8l1.2 1-.9 2.2-1.6-.1-1.2 1.2.1 1.6-2.2.9-1-1.2h-1.7l-1 1.2-2.2-.9.1-1.6-1.2-1.2-1.6.1-.9-2.2 1.2-1v-1.7l-1.2-1L6 9l1.6.1 1.2-1.2-.1-1.6 2.2-.9 1 1.2h1.7l1-1.2 2.2.9-.1 1.6L18 9.1l1.6-.1.9 2.2-1.2 1z"/></svg>
    </button>
  </nav>
</template>
