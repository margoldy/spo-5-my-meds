<script setup>
defineProps({ title: String })
defineEmits(['close'])
</script>

<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-heading">
        <h2 class="title">{{ title }}</h2>
        <button class="modal-close" type="button" aria-label="Закрыть" @click="$emit('close')">×</button>
      </div>
      <slot />
    </div>
  </div>
</template>
