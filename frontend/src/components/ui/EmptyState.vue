<script setup>
defineProps({ text: String })
</script>

<template>
  <div class="empty-state">{{ text }}</div>
</template>
