import { request } from './http'

export const requestCode = email => request('/api/v1/auth/code/request', {
  method: 'POST',
  body: { email },
})

export const verifyCode = (email, code) => request('/api/v1/auth/code/verify', {
  method: 'POST',
  body: { email, code },
})
