import { request } from './http'

export const createIntake = body => request('/api/v1/intakes', { method: 'POST', body })

export function getIntakes(filters = {}) {
  const params = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value)
  })
  const query = params.toString()
  return request(`/api/v1/intakes${query ? `?${query}` : ''}`)
}

export const updateIntake = (id, body) => request(`/api/v1/intakes/${id}`, {
  method: 'PATCH',
  body,
})

export const deleteIntake = id => request(`/api/v1/intakes/${id}`, { method: 'DELETE' })
