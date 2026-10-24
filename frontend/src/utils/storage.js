const ACCESS_TOKEN = 'my-meds-access-token'
const REFRESH_TOKEN = 'my-meds-refresh-token'
const PREFERENCES = 'my-meds-preferences'

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
