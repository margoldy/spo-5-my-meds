import { request } from './http'

export const getCourses = () => request('/api/v1/courses')

export const getCourse = id => request(`/api/v1/courses/${id}`)

export const createCourse = body => request('/api/v1/courses', { method: 'POST', body })

export const updateCourse = (id, body) => request(`/api/v1/courses/${id}`, {
  method: 'PATCH',
  body,
})

export const deleteCourse = id => request(`/api/v1/courses/${id}`, { method: 'DELETE' })
