<script setup>
defineProps({
  title: { type: String, default: 'Пока пусто' },
  text: String,
  action: String,
})

defineEmits(['action'])
</script>

<template>
  <div class="empty-state">
    <span class="empty-state-icon" aria-hidden="true">
      <svg viewBox="0 0 32 32" fill="none">
        <circle cx="16" cy="16" r="13" />
        <path d="M16 9v14M10 12.5l12 7M22 12.5l-12 7" />
      </svg>
    </span>
    <strong>{{ title }}</strong>
    <p>{{ text }}</p>
    <button v-if="action" type="button" @click="$emit('action')">{{ action }}</button>
  </div>
</template>
