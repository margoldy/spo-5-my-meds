<script setup>
defineProps({ title: String, back: Boolean })
defineEmits(['back'])
</script>

<template>
  <div class="topbar">
    <button v-if="back" class="back-button" type="button" aria-label="Назад" @click="$emit('back')">‹</button>
    <h1 class="title">{{ title }}</h1>
  </div>
</template>
