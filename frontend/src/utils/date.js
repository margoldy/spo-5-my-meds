const monthFormatter = new Intl.DateTimeFormat('ru-RU', { month: 'long', year: 'numeric' })
const dateFormatter = new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })

export function isoDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function dateInTimeZone(date, timeZone) {
  const parts = new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    timeZone,
  }).formatToParts(date)
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]))
  return `${values.year}-${values.month}-${values.day}`
}

export function dateTimeInTimeZone(date, timeZone) {
  const parts = new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
    timeZone,
  }).formatToParts(date)
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]))
  return `${values.year}-${values.month}-${values.day}T${values.hour}:${values.minute}`
}

function timeZoneOffset(date, timeZone) {
  const parts = new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hourCycle: 'h23',
    timeZone,
  }).formatToParts(date)
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]))
  const displayedAsUtc = Date.UTC(values.year, Number(values.month) - 1, values.day, values.hour, values.minute, values.second)
  const wholeSecond = Math.floor(date.getTime() / 1000) * 1000
  return displayedAsUtc - wholeSecond
}

export function zonedDateTimeToIso(value, timeZone) {
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,3}))?)?$/)
  if (!match) throw new Error('Неверные дата и время')
  const [, year, month, day, hour, minute, second = '0', fraction = ''] = match
  const milliseconds = Number(fraction.padEnd(3, '0'))
  const localAsUtc = Date.UTC(year, Number(month) - 1, day, hour, minute, second, milliseconds)
  let result = localAsUtc - timeZoneOffset(new Date(localAsUtc), timeZone)
  result = localAsUtc - timeZoneOffset(new Date(result), timeZone)
  return new Date(result).toISOString()
}

export function monthTitle(date) {
  const title = monthFormatter.format(date)
  return title.charAt(0).toUpperCase() + title.slice(1)
}

export function formatDate(value) {
  if (!value) return 'Не указано'
  return dateFormatter.format(new Date(`${value}T12:00:00`))
}

export function formatDateTime(value, timeZone) {
  if (!value) return ''
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
    timeZone,
  }).format(new Date(value))
}

export function formatTime(value, timeZone) {
  if (!value) return ''
  return new Intl.DateTimeFormat('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
    timeZone,
  }).format(new Date(value))
}

export function calendarDays(month) {
  const first = new Date(month.getFullYear(), month.getMonth(), 1)
  const offset = (first.getDay() + 6) % 7
  const start = new Date(first)
  start.setDate(first.getDate() - offset)
  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(start)
    date.setDate(start.getDate() + index)
    return { date, value: isoDate(date), current: date.getMonth() === month.getMonth() }
  })
}

export function daysText(days = []) {
  if (days.length === 7) return 'Ежедневно'
  const names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
  return days.map(day => names[day - 1]).join(', ')
}
