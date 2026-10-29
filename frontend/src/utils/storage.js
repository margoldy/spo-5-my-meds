const ACCESS_TOKEN = 'my-meds-access-token'
const REFRESH_TOKEN = 'my-meds-refresh-token'
const PREFERENCES = 'my-meds-preferences'
const EMERGENCY_CARD = 'my-meds-emergency-card'
const INVENTORY = 'my-meds-inventory'

export function getAccessToken() {
  return sessionStorage.getItem(ACCESS_TOKEN)
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN)
}

export function saveTokens(accessToken, refreshToken) {
  sessionStorage.setItem(ACCESS_TOKEN, accessToken)
  if (refreshToken) localStorage.setItem(REFRESH_TOKEN, refreshToken)
}

export function clearTokens() {
  sessionStorage.removeItem(ACCESS_TOKEN)
  localStorage.removeItem(REFRESH_TOKEN)
}

export function getPreferences() {
  const defaults = { notifications: true, reminderMinutes: 15 }
  try {
    return { ...defaults, ...JSON.parse(localStorage.getItem(PREFERENCES)) }
  } catch {
    return defaults
  }
}

export function savePreferences(value) {
  localStorage.setItem(PREFERENCES, JSON.stringify(value))
}

export function getEmergencyCard(userId) {
  if (!userId) return { allergies: [] }
  try {
    return { allergies: [], ...JSON.parse(localStorage.getItem(`${EMERGENCY_CARD}-${userId}`)) }
  } catch {
    return { allergies: [] }
  }
}

export function saveEmergencyCard(userId, value) {
  if (!userId) return
  localStorage.setItem(`${EMERGENCY_CARD}-${userId}`, JSON.stringify(value))
}

export function getCourseInventory(userId, courseId) {
  if (!userId || !courseId) return null
  try {
    return JSON.parse(localStorage.getItem(`${INVENTORY}-${userId}-${courseId}`))
  } catch {
    return null
  }
}

export function saveCourseInventory(userId, courseId, value) {
  if (!userId || !courseId) return
  localStorage.setItem(`${INVENTORY}-${userId}-${courseId}`, JSON.stringify(value))
}

export function removeCourseInventory(userId, courseId) {
  if (!userId || !courseId) return
  localStorage.removeItem(`${INVENTORY}-${userId}-${courseId}`)
}
