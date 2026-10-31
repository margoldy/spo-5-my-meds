<script setup>
defineProps({ active: String })
defineEmits(['change'])

import scheduleRed from '../../assets/icons/nav/calendar-red.svg'
import scheduleWhite from '../../assets/icons/nav/calendar-white.svg'
import medsRed from '../../assets/icons/nav/meds-red.svg'
import medsWhite from '../../assets/icons/nav/meds-white.svg'
import historyRed from '../../assets/icons/nav/history-red.svg'
import historyWhite from '../../assets/icons/nav/history-white.svg'
import settingsRed from '../../assets/icons/nav/settings-red.svg'
import settingsWhite from '../../assets/icons/nav/settings-white.svg'

const icons = {
  calendar: { red: scheduleRed, white: scheduleWhite },
  courses:  { red: medsRed,     white: medsWhite },
  history:  { red: historyRed,  white: historyWhite },
  settings: { red: settingsRed, white: settingsWhite },
}

function icon(tab, isActive) {
  return isActive ? icons[tab].white : icons[tab].red
}
</script>

<template>
  <nav class="bottom-nav">
    <button class="nav-button schedule-tab" :class="{ active: active === 'calendar' }" type="button" aria-label="Расписание" @click="$emit('change', 'calendar')">
      <img class="nav-icon nav-icon--calendar" :src="icon('calendar', active === 'calendar')" alt="">
    </button>

    <button class="nav-button" :class="{ active: active === 'courses' }" type="button" aria-label="Мои лекарства" @click="$emit('change', 'courses')">
      <img class="nav-icon nav-icon--meds"     :src="icon('courses',  active === 'courses')"  alt="">
    </button>

    <button class="nav-button history-tab" :class="{ active: active === 'history' }" type="button" aria-label="История" @click="$emit('change', 'history')">
      <img class="nav-icon nav-icon--history"  :src="icon('history',  active === 'history')"  alt="">
    </button>

    <button class="nav-button" :class="{ active: active === 'settings' }" type="button" aria-label="Настройки" @click="$emit('change', 'settings')">
      <img class="nav-icon nav-icon--settings" :src="icon('settings', active === 'settings')" alt="">
    </button>
  </nav>
</template>