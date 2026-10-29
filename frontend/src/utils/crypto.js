import { argon2id } from 'hash-wasm'

const encoder = new TextEncoder()
const decoder = new TextDecoder()
const databaseName = 'my-meds-device'
const storeName = 'keys'

function toBase64(value) {
  let binary = ''
  for (const byte of new Uint8Array(value)) binary += String.fromCharCode(byte)
  return btoa(binary)
}

function fromBase64(value) {
  const binary = atob(value)
  return Uint8Array.from(binary, character => character.charCodeAt(0))
}

function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(databaseName, 1)
    request.onupgradeneeded = () => request.result.createObjectStore(storeName)
    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error)
  })
}

async function deriveKey(password, salt, options) {
  const raw = await argon2id({
    password,
    salt,
    parallelism: options.parallelism,
    iterations: options.iterations,
    memorySize: options.memory,
    hashLength: 32,
    outputType: 'binary',
  })
  return crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['encrypt', 'decrypt'])
}

export async function createEncryptionKey(password) {
  const rawKey = crypto.getRandomValues(new Uint8Array(32))
  const key = await crypto.subtle.importKey('raw', rawKey, 'AES-GCM', false, ['encrypt', 'decrypt'])
  const encrypted = await wrapEncryptionKey(rawKey, password)
  return { key, encrypted }
}

export async function wrapEncryptionKey(rawKey, password) {
  const options = { memory: 65536, iterations: 3, parallelism: 1 }
  const salt = crypto.getRandomValues(new Uint8Array(16))
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const key = await deriveKey(password, salt, options)
  const data = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, rawKey)
  return JSON.stringify({
    v: 1,
    kdf: 'Argon2id',
    ...options,
    salt: toBase64(salt),
    alg: 'AES-256-GCM',
    iv: toBase64(iv),
    data: toBase64(data),
  })
}

export async function unwrapEncryptionKey(encrypted, password) {
  try {
    const envelope = JSON.parse(encrypted)
    const salt = fromBase64(envelope.salt)
    const iv = fromBase64(envelope.iv)
    const key = await deriveKey(password, salt, envelope)
    const rawKey = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, fromBase64(envelope.data))
    const deviceKey = await crypto.subtle.importKey('raw', rawKey, 'AES-GCM', false, ['encrypt', 'decrypt'])
    return { key: deviceKey, rawKey: new Uint8Array(rawKey) }
  } catch {
    throw new Error('Неверный пароль шифрования')
  }
}

export async function encryptData(key, value) {
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const data = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, encoder.encode(JSON.stringify(value)))
  return JSON.stringify({ v: 1, alg: 'AES-256-GCM', iv: toBase64(iv), data: toBase64(data) })
}

export async function decryptData(key, encrypted) {
  const envelope = JSON.parse(encrypted)
  const data = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: fromBase64(envelope.iv) },
    key,
    fromBase64(envelope.data),
  )
  return JSON.parse(decoder.decode(data))
}

export async function saveDeviceKey(userId, key) {
  const database = await openDatabase()
  await new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readwrite')
    transaction.objectStore(storeName).put(key, userId)
    transaction.oncomplete = resolve
    transaction.onerror = () => reject(transaction.error)
  })
  database.close()
}

export async function getDeviceKey(userId) {
  const database = await openDatabase()
  const key = await new Promise((resolve, reject) => {
    const request = database.transaction(storeName).objectStore(storeName).get(userId)
    request.onsuccess = () => resolve(request.result || null)
    request.onerror = () => reject(request.error)
  })
  database.close()
  return key
}

export async function removeDeviceKey(userId) {
  const database = await openDatabase()
  await new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readwrite')
    transaction.objectStore(storeName).delete(userId)
    transaction.oncomplete = resolve
    transaction.onerror = () => reject(transaction.error)
  })
  database.close()
}
