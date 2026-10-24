import { dateInTimeZone, zonedDateTimeToIso } from './date'

let timers = []

function addDays(value, amount) {
  const date = new Date(`${value}T12:00:00Z`)
  date.setUTCDate(date.getUTCDate() + amount)
  return date.toISOString().slice(0, 10)
}

export function scheduleReminders(courses, preferences, timeZone) {
  timers.forEach(clearTimeout)
  timers = []
  if (!preferences.notifications || !('Notification' in window) || Notification.permission !== 'granted') return
  const now = new Date()
  const startDate = dateInTimeZone(now, timeZone)
  for (let offset = 0; offset < 7; offset += 1) {
    const date = addDays(startDate, offset)
    const weekday = new Date(`${date}T12:00:00Z`).getUTCDay() || 7
    courses.filter(course => course.is_active && course.start_date <= date && (!course.end_date || course.end_date >= date)).forEach(course => {
      course.schedules.filter(item => item.days_of_week.includes(weekday)).forEach(item => {
        const planned = new Date(zonedDateTimeToIso(`${date}T${item.time}`, timeZone))
        const reminder = planned.getTime() - preferences.reminderMinutes * 60000
        const delay = reminder - Date.now()
        if (delay <= 0 || delay > 2147483647) return
        timers.push(setTimeout(() => {
          new Notification(course.name, {
            body: `Через ${preferences.reminderMinutes} мин.: ${item.amount} ${item.unit}`,
            tag: `schedule-${item.id}-${planned.toISOString()}`,
          })
        }, delay))
      })
    })
  }
}

export async function requestNotifications() {
  if (!('Notification' in window)) return false
  return (await Notification.requestPermission()) === 'granted'
}
