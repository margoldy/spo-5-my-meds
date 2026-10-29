<script setup>
import { computed, ref } from 'vue'
import AppHeader from '../components/ui/AppHeader.vue'
import { go, showToast } from '../store/store'
import { state } from '../store/state'
import { getEmergencyCard, saveEmergencyCard } from '../utils/storage'
import { formatDate } from '../utils/date'

const stored = getEmergencyCard(state.user?.id)
const allergies = ref([...stored.allergies])
const allergy = ref('')
const activeCourses = computed(() => state.courses.filter(item => item.is_active))

function addAllergy() {
  const value = allergy.value.trim()
  if (!value || allergies.value.some(item => item.toLowerCase() === value.toLowerCase())) return
  allergies.value.push(value)
  allergy.value = ''
  save()
}

function removeAllergy(index) {
  allergies.value.splice(index, 1)
  save()
}

function save() {
  saveEmergencyCard(state.user?.id, { allergies: allergies.value })
  showToast('Карточка сохранена на устройстве')
}
</script>

<template>
  <section class="screen no-nav emergency-screen">
    <AppHeader title="Медицинская карточка" back @back="go('settings')" />
    <div class="emergency-hero">
      <div class="emergency-mark">✚</div>
      <div><span>Для экстренной ситуации</span><strong>{{ state.user?.name || 'Владелец карточки' }}</strong><small>{{ state.user?.birth_date ? formatDate(state.user.birth_date) : 'Дата рождения не указана' }}</small></div>
    </div>

    <section class="emergency-section">
      <div class="emergency-heading"><span>Аллергии</span><small>Заполняются вручную</small></div>
      <form class="allergy-form" @submit.prevent="addAllergy">
        <input v-model="allergy" placeholder="Например, пенициллин">
        <button type="submit" aria-label="Добавить аллергию">+</button>
      </form>
      <div v-if="allergies.length" class="allergy-list">
        <span v-for="(item, index) in allergies" :key="item">{{ item }}<button type="button" :aria-label="`Удалить ${item}`" @click="removeAllergy(index)">×</button></span>
      </div>
      <div v-else class="emergency-empty">Аллергии пока не указаны</div>
    </section>

    <section class="emergency-section">
      <div class="emergency-heading"><span>Принимаемые лекарства</span><small>Из активных курсов</small></div>
      <div v-if="activeCourses.length" class="emergency-medications">
        <article v-for="course in activeCourses" :key="course.id">
          <i>{{ course.name.slice(0, 1).toUpperCase() }}</i>
          <div><strong>{{ course.name }}</strong><small v-if="course.schedules.length">{{ course.schedules.map(item => `${item.amount} ${item.unit} в ${item.time}`).join(' · ') }}</small><small v-else>По необходимости</small></div>
        </article>
      </div>
      <div v-else class="emergency-empty">Активных курсов нет</div>
    </section>

    <div class="local-card-note">
      <svg viewBox="0 0 24 24" fill="none"><path d="M7 10V7a5 5 0 0 1 10 0v3M6 10h12v10H6zM12 14v2"/></svg>
      <p><strong>Аллергии остаются на этом устройстве.</strong> Они не отправляются на сервер и исчезнут после очистки данных браузера.</p>
    </div>
  </section>
</template>
