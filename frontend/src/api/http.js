import { clearTokens, getAccessToken, getRefreshToken, saveTokens } from '../utils/storage'

const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
let refreshRequest = null

function errorMessage(data, status) {
  if (typeof data?.detail === 'string') return data.detail
  if (Array.isArray(data?.detail)) return data.detail.map(item => item.msg).join('. ')
  return `Ошибка запроса: ${status}`
}

async function refreshAccessToken() {
  const refreshToken = getRefreshToken()
  if (!refreshToken) throw new Error('Сессия завершена')
  const response = await fetch(`${apiUrl}/api/v1/auth/token/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
  if (!response.ok) {
    clearTokens()
    throw new Error('Сессия завершена')
  }
  const data = await response.json()
  saveTokens(data.access_token)
  return data.access_token
}

export async function request(path, options = {}, retry = true) {
  const headers = { ...options.headers }
  if (options.body !== undefined) headers['Content-Type'] = 'application/json'
  const accessToken = getAccessToken()
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`
  const response = await fetch(`${apiUrl}${path}`, {
    ...options,
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  })
  if (response.status === 401 && retry && getRefreshToken()) {
    refreshRequest ||= refreshAccessToken().finally(() => { refreshRequest = null })
    await refreshRequest
    return request(path, options, false)
  }
  if (response.status === 204) return null
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const error = new Error(errorMessage(data, response.status))
    error.status = response.status
    throw error
  }
  return data
}
