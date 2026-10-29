import { reactive } from 'vue'
import { getPreferences } from '../utils/storage'

export const state = reactive({
  phase: 'loading',
  page: 'calendar',
  previousPage: 'calendar',
  busy: false,
  toast: '',
  error: '',
  user: null,
  encryptionExists: false,
  key: null,
  catalog: [],
  catalogTotal: 0,
  courses: [],
  dayItems: [],
  intakes: [],
  courseIntakes: [],
  selectedCourseId: null,
  selectedMedicationId: null,
  selectedIntakeId: null,
  coursePreset: null,
  preferences: getPreferences(),
})
