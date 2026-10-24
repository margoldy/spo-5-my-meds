import { request } from './http'

export function getMedications(filters = {}) {
  const params = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) params.set(key, value)
  })
  const query = params.toString()
  return request(`/api/v1/medications${query ? `?${query}` : ''}`)
}

export const getMedication = id => request(`/api/v1/medications/${id}`)

export const createMedication = body => request('/api/v1/medications', { method: 'POST', body })

export const updateMedication = (id, body) => request(`/api/v1/medications/${id}`, {
  method: 'PATCH',
  body,
})
