<script setup>
defineProps({ title: String })
defineEmits(['close'])
</script>

<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-card">
      <h2 class="title">{{ title }}</h2>
      <slot />
    </div>
  </div>
</template>
