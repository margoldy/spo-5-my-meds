import { request } from './http'

export const getMe = () => request('/api/v1/users/me')

export const updateMe = body => request('/api/v1/users/me', { method: 'PATCH', body })

export const getEncryptionKey = () => request('/api/v1/users/me/encryption-key')

export const saveEncryptionKey = encryptedDek => request('/api/v1/users/me/encryption-key', {
  method: 'PUT',
  body: { encrypted_dek: encryptedDek },
})
