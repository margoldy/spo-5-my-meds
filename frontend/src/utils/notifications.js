let timers = []

export function scheduleReminders(courses, preferences) {
  timers.forEach(clearTimeout)
  timers = []
  if (!preferences.notifications || !('Notification' in window) || Notification.permission !== 'granted') return
  const now = new Date()
  for (let offset = 0; offset < 7; offset += 1) {
    const day = new Date(now.getFullYear(), now.getMonth(), now.getDate() + offset)
    const weekday = day.getDay() || 7
    const date = `${day.getFullYear()}-${String(day.getMonth() + 1).padStart(2, '0')}-${String(day.getDate()).padStart(2, '0')}`
    courses.filter(course => course.is_active && course.start_date <= date && (!course.end_date || course.end_date >= date)).forEach(course => {
      course.schedules.filter(item => item.days_of_week.includes(weekday)).forEach(item => {
        const [hours, minutes] = item.time.split(':').map(Number)
        const planned = new Date(day.getFullYear(), day.getMonth(), day.getDate(), hours, minutes)
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
