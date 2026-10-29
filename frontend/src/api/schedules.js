import { request } from './http'

export const getSchedulesForDay = date => request(`/api/v1/schedules?date=${date}`)

export const createSchedule = (courseId, body) => request(`/api/v1/courses/${courseId}/schedules`, {
  method: 'POST',
  body,
})

export const updateSchedule = (id, body) => request(`/api/v1/schedules/${id}`, {
  method: 'PATCH',
  body,
})

export const deleteSchedule = id => request(`/api/v1/schedules/${id}`, { method: 'DELETE' })
