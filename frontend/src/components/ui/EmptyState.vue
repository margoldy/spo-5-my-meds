<script setup>
import emptyIcon from '../../assets/icons/flower.svg'

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
      <img :src="emptyIcon" alt="">
    </span>
    <strong>{{ title }}</strong>
    <p>{{ text }}</p>
    <button v-if="action" type="button" @click="$emit('action')">{{ action }}</button>
  </div>
</template>