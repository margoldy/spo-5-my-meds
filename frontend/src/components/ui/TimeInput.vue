<script setup>
import { computed } from 'vue'

const props = defineProps({ modelValue: { type: String, default: '09:00' } })
const emit = defineEmits(['update:modelValue'])
const hours = Array.from({ length: 24 }, (_, index) => String(index).padStart(2, '0'))
const minutes = Array.from({ length: 60 }, (_, index) => String(index).padStart(2, '0'))

const hour = computed({
  get: () => props.modelValue.split(':')[0] || '09',
  set: value => emit('update:modelValue', `${value}:${minute.value}`),
})

const minute = computed({
  get: () => props.modelValue.split(':')[1] || '00',
  set: value => emit('update:modelValue', `${hour.value}:${value}`),
})
</script>

<template>
  <div class="time-picker">
    <select v-model="hour" aria-label="Часы">
      <option v-for="item in hours" :key="item" :value="item">{{ item }}</option>
    </select>
    <span>:</span>
    <select v-model="minute" aria-label="Минуты">
      <option v-for="item in minutes" :key="item" :value="item">{{ item }}</option>
    </select>
  </div>
  <div class="time-presets">
    <button v-for="item in ['08:00', '12:00', '15:00', '21:00']" :key="item" type="button" @click="$emit('update:modelValue', item)">{{ item }}</button>
  </div>
</template>
