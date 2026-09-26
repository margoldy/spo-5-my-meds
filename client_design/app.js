const icons = {
  calendar: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></svg>',
  pills: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><circle cx="12" cy="12" r="8"/><path d="M7.5 16.5l9-9"/></svg>',
  book: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><path d="M3 5.5c3.4-.8 6.4 0 9 2.2v12c-2.6-2.2-5.6-3-9-2.2zM21 5.5c-3.4-.8-6.4 0-9 2.2v12c2.6-2.2 5.6-3 9-2.2z"/></svg>',
  settings: '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M19 13.8l1.2 1-.9 2.2-1.6-.1-1.2 1.2.1 1.6-2.2.9-1-1.2h-1.7l-1 1.2-2.2-.9.1-1.6-1.2-1.2-1.6.1-.9-2.2 1.2-1v-1.7l-1.2-1L6 9l1.6.1 1.2-1.2-.1-1.6 2.2-.9 1 1.2h1.7l1-1.2 2.2.9-.1 1.6L18 9.1l1.6-.1.9 2.2-1.2 1z"/></svg>',
  taken: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><path d="M12 5v14M5.9 8.5l12.2 7M18.1 8.5l-12.2 7"/></svg>'
};

const catalogSeed = [
  [1, 'Маалокс®', 'Maalox®', 'Санофи', 'Пищеварительная система', 'Суспензия', '15 мл'],
  [2, 'Маверекс', 'Maverex', 'Медикал Юнион', 'Противовирусные', 'Таблетки', '100 мг'],
  [3, 'Мавирет', 'Mavireth', 'AbbVie', 'Противовирусные', 'Таблетки', '100 мг + 40 мг'],
  [4, 'Магалюмон®', 'Magalumon', 'Фармстандарт', 'Минералы', 'Таблетки', '500 мг'],
  [5, 'Магнатол', 'Magnatol', 'VitaLab', 'Минералы', 'Таблетки', '400 мг'],
  [6, 'Магне B6®', 'Magne B6®', 'Opella', 'Минералы', 'Таблетки', '48 мг + 5 мг'],
  [7, 'Магневист®', 'Magnevist®', 'Bayer', 'Диагностические средства', 'Раствор', '0,5 ммоль/мл'],
  [8, 'Магнезия карбоника', 'Magnesia carbonica', 'Boiron', 'Минералы', 'Гранулы', 'C30'],
  [9, 'Магнелисит', 'Magnelicit', 'Фармгрупп', 'Минералы', 'Таблетки', '470 мг'],
  [10, 'Магнерот®', 'Magnerot®', 'Wörwag Pharma', 'Минералы', 'Таблетки', '500 мг'],
  [11, 'Магника®', 'Magnica', 'Киевский витаминный завод', 'Минералы', 'Таблетки', '48 мг'],
  [12, 'Магний плюс', 'Magnesium plus', 'Внешторг Фарма', 'Минералы', 'Таблетки', '500 мг'],
  [13, 'Мазепин', 'Mazepine', 'HealthCare', 'Нервная система', 'Таблетки', '200 мг'],
  [14, 'Витрум', 'Vitrum', 'Unipharm', 'Витамины', 'Таблетки', '1 таблетка'],
  [15, 'Эсциталопрам', 'Escitalopram', 'Канонфарма', 'Нервная система', 'Таблетки', '10 мг']
];

const state = {
  page: 'calendar',
  loggedIn: true,
  guest: false,
  authStep: 'email',
  email: 'user@example.com',
  role: 'user',
  selectedDay: 19,
  selectedCourseId: 'c2',
  selectedMedicationId: 1,
  selectedIntakeId: null,
  editingScheduleId: null,
  courseDraftSchedules: [],
  editingDraftScheduleId: null,
  catalogQuery: '',
  courseQuery: '',
  categoryFilter: '',
  formFilter: '',
  adminQuery: '',
  historyCourseId: '',
  toast: '',
  notifications: true,
  reminderMinutes: 15,
  profile: { name: 'Макан', email: 'user@example.com', birthDate: '2006-04-15', avatar: '' },
  catalog: catalogSeed.map(([id, name, international, manufacturer, category, form, strength]) => ({
    id, name, international, manufacturer, category, form, strength,
    instruction: `Инструкция для препарата «${name}»`,
    active: true
  })),
  courses: [
    { id: 'c1', medicationId: null, name: 'Анальгин', mode: 'as_needed', start: '2021-08-20', end: '', active: true, notes: 'Принимать при боли', schedules: [] },
    { id: 'c2', medicationId: 14, name: 'Витрум', mode: 'scheduled', start: '2026-08-15', end: '2026-10-15', active: true, notes: 'После еды', schedules: [
      { id: 's21', time: '15:00', amount: 1, unit: 'таблетка', days: [1, 2, 3, 4, 5, 6, 7] }
    ] },
    { id: 'c3', medicationId: 15, name: 'Эсциталопрам', mode: 'scheduled', start: '2026-09-15', end: '2026-10-15', active: true, notes: '', schedules: [
      { id: 's31', time: '12:00', amount: 5, unit: 'мг', days: [1, 2, 3, 4, 5, 6, 7] },
      { id: 's32', time: '21:00', amount: 5, unit: 'мг', days: [1, 2, 3, 4, 5, 6, 7] }
    ] }
  ],
  intakes: [
    { id: 'i1', courseId: 'c3', scheduleId: 's31', medicationName: 'Эсциталопрам', date: '2026-09-19', time: '12:03', amount: 5, unit: 'мг' },
    { id: 'i2', courseId: 'c2', scheduleId: 's21', medicationName: 'Витрум', date: '2026-09-18', time: '15:06', amount: 1, unit: 'таблетка' },
    { id: 'i3', courseId: 'c1', scheduleId: null, medicationName: 'Анальгин', date: '2026-09-17', time: '18:40', amount: 1, unit: 'таблетка' },
    { id: 'i4', courseId: null, scheduleId: null, medicationName: 'Маалокс®', date: '2026-09-16', time: '20:15', amount: 15, unit: 'мл' }
  ]
};

const app = document.querySelector('#app');

function safe(value = '') {
  return String(value).replace(/[&<>"]/g, symbol => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[symbol]);
}

function pad(value) {
  return String(value).padStart(2, '0');
}

function selectedDate() {
  return `2026-09-${pad(state.selectedDay)}`;
}

function formatDate(value) {
  if (!value) return 'Не указано';
  return new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(`${value}T12:00:00`));
}

function dateWeekday(value) {
  const day = new Date(`${value}T12:00:00`).getDay();
  return day === 0 ? 7 : day;
}

function daysText(days) {
  if (days.length === 7) return 'Ежедневно';
  const names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  return days.map(day => names[day - 1]).join(', ');
}

function doseText(amount, unit) {
  return `${amount} ${unit}`;
}

function timePicker(prefix, value = '09:00') {
  const [selectedHour, selectedMinute] = value.split(':');
  const hours = Array.from({ length: 24 }, (_, index) => pad(index));
  const minutes = Array.from({ length: 60 }, (_, index) => pad(index));
  const options = (items, selected) => items.map(item => `<option value="${item}" ${item === selected ? 'selected' : ''}>${item}</option>`).join('');
  return `
    <div class="time-picker" data-time-picker="${prefix}">
      <select name="${prefix}Hour" aria-label="Часы">${options(hours, selectedHour)}</select>
      <span>:</span>
      <select name="${prefix}Minute" aria-label="Минуты">${options(minutes, selectedMinute)}</select>
    </div>
    <div class="time-presets">
      ${['08:00', '12:00', '15:00', '21:00'].map(time => `<button type="button" data-time-prefix="${prefix}" data-quick-time="${time}">${time}</button>`).join('')}
    </div>
  `;
}

function formTime(data, prefix) {
  return `${data.get(`${prefix}Hour`)}:${data.get(`${prefix}Minute`)}`;
}

function nav(active) {
  if (state.guest) return '';
  const items = [
    ['calendar', 'calendar', 'Календарь'],
    ['medicines', 'pills', 'Мои лекарства'],
    ['catalog', 'book', 'Справочник'],
    ['settings', 'settings', 'Настройки']
  ];
  return `<nav class="bottom-nav">${items.map(([page, icon, label]) => `<button class="nav-button ${active === page ? 'active' : ''}" data-page="${page}" aria-label="${label}">${icons[icon]}</button>`).join('')}</nav>`;
}

function header(title, back = '') {
  return `<div class="topbar">${back ? `<button class="back-button" data-back="${back}" aria-label="Назад">‹</button>` : ''}<h1 class="title">${title}</h1></div>`;
}

function toast() {
  return state.toast ? `<div class="toast">${safe(state.toast)}</div>` : '';
}

function showToast(message) {
  state.toast = message;
  render();
  setTimeout(() => {
    if (state.toast === message) {
      state.toast = '';
      render();
    }
  }, 1600);
}

function calendarDays() {
  const days = [31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 1, 2, 3, 4];
  return days.map((day, index) => `<button class="day ${index === 0 || index > 30 ? 'other' : ''} ${day === state.selectedDay && index <= 30 ? 'selected' : ''}" data-day="${day}" ${index === 0 || index > 30 ? 'disabled' : ''}>${day}</button>`).join('');
}

function scheduledItems() {
  const date = selectedDate();
  const weekday = dateWeekday(date);
  const items = [];
  state.courses.filter(course => course.active && course.mode === 'scheduled').forEach(course => {
    course.schedules.filter(schedule => schedule.days.includes(weekday)).forEach(schedule => {
      const intake = state.intakes.find(item => item.date === date && item.scheduleId === schedule.id);
      items.push({ course, schedule, intake });
    });
  });
  return items.sort((a, b) => a.schedule.time.localeCompare(b.schedule.time));
}

function renderCalendar() {
  const groups = scheduledItems().map(({ course, schedule, intake }) => `
    <section class="time-group">
      <h2 class="time-label">${schedule.time}</h2>
      <article class="intake-card">
        <button class="intake-main plain-card-button" data-course="${course.id}">
          <span class="medicine-name">${safe(course.name)}</span>
          <span class="dose">${doseText(intake?.amount ?? schedule.amount, intake?.unit ?? schedule.unit)}</span>
          ${intake ? `<span class="taken-at">Принято в ${intake.time}</span>` : ''}
        </button>
        <button class="check-button ${intake ? 'taken' : ''}" data-toggle-intake="${schedule.id}" aria-label="${intake ? 'Отменить приём' : 'Отметить приём'}">${intake ? icons.taken : ''}</button>
      </article>
    </section>
  `).join('');
  app.innerHTML = `
    <section class="screen">
      <h1 class="title">Сентябрь 2026</h1>
      <div class="calendar">
        <div class="calendar-grid">
          ${['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'].map(day => `<div class="weekday">${day}</div>`).join('')}
          ${calendarDays()}
        </div>
      </div>
      <button class="inline-action" data-page="as-needed">+ Внеплановый приём</button>
      ${groups || '<div class="empty-state">На этот день приёмов нет</div>'}
    </section>
    ${nav('calendar')}
    ${toast()}
  `;
}

function courseSummary(course) {
  const times = course.schedules.map(item => `${item.time} — ${doseText(item.amount, item.unit)}`).join('<br>');
  const scheduleDays = [...new Set(course.schedules.flatMap(item => item.days))];
  return `
    <article class="course-card ${course.active ? '' : 'inactive'}" data-course="${course.id}">
      <div class="card-heading"><h2 class="medicine-name">${safe(course.name)}</h2>${course.active ? '' : '<span class="badge">Завершён</span>'}</div>
      <div class="info-grid">
        <span class="info-label">Частота</span><span>${course.mode === 'as_needed' ? 'По необходимости' : daysText(scheduleDays)}</span>
        ${times ? `<span class="info-label">Время</span><span>${times}</span>` : ''}
        <span class="info-label">Длительность</span><span>Начало: ${formatDate(course.start)}${course.end ? `<br>Конец: ${formatDate(course.end)}` : ''}</span>
      </div>
    </article>
  `;
}

function renderMedicines() {
  const query = state.courseQuery.toLowerCase();
  const courses = state.courses.filter(course => course.name.toLowerCase().includes(query));
  app.innerHTML = `
    <section class="screen">
      <h1 class="title">Мои лекарства</h1>
      <input class="search" id="medicine-search" value="${safe(state.courseQuery)}" placeholder="Найти лекарство...">
      <div class="course-list">${courses.map(courseSummary).join('') || '<div class="empty-state">Ничего не найдено</div>'}</div>
    </section>
    <button class="floating-button" data-page="course-create" aria-label="Добавить лекарство">+</button>
    ${nav('medicines')}
    ${toast()}
  `;
}

function renderCourseDetail() {
  const course = state.courses.find(item => item.id === state.selectedCourseId);
  if (!course) {
    state.page = 'medicines';
    renderMedicines();
    return;
  }
  const scheduleRows = course.schedules.map(schedule => `
    <div class="schedule-row">
      <button class="schedule-main" type="button" data-edit-schedule="${schedule.id}">
        <strong>${schedule.time} — ${doseText(schedule.amount, schedule.unit)}</strong>
        <span>${daysText(schedule.days)}</span>
      </button>
      <button class="mini-button danger" type="button" data-delete-schedule="${schedule.id}" aria-label="Удалить расписание">×</button>
    </div>
  `).join('');
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Информация о лекарстве', 'medicines')}
      <form id="course-edit-form">
        <label class="field-label">Название</label>
        <input class="detail-field" value="${safe(course.name)}" readonly>
        <div class="two-columns">
          <label class="field-label">Начало<input class="detail-field" name="start" type="date" value="${course.start}" required></label>
          <label class="field-label">Конец<input class="detail-field" name="end" type="date" value="${course.end}"></label>
        </div>
        <label class="section-title">Расписание</label>
        <article class="detail-card">
          ${scheduleRows || '<p class="compact-text">Расписание не задано — лекарство принимается по необходимости.</p>'}
          <button class="inline-action" type="button" data-edit-schedule="new">+ Добавить время</button>
        </article>
        <label class="section-title" for="course-notes">Заметки</label>
        <textarea class="notes" id="course-notes" name="notes" placeholder="Напишите что-нибудь...">${safe(course.notes)}</textarea>
        <label class="toggle-row"><span>Курс активен</span><input type="checkbox" name="active" ${course.active ? 'checked' : ''}></label>
        <div class="stack-actions">
          <button class="action-button primary" type="submit">Сохранить изменения</button>
          ${course.mode === 'as_needed' ? '<button class="action-button" type="button" data-page="as-needed">Записать приём</button>' : ''}
          <button class="action-button" type="button" data-history-course="${course.id}">История приёмов</button>
          <button class="action-button danger" type="button" data-delete-course="${course.id}">Удалить курс</button>
        </div>
      </form>
    </section>
    ${toast()}
  `;
}

function daysPicker(selected = [1, 2, 3, 4, 5, 6, 7], name = 'days') {
  const names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  return `<div class="days-picker">${names.map((day, index) => `<label><input type="checkbox" name="${name}" value="${index + 1}" ${selected.includes(index + 1) ? 'checked' : ''}><span>${day}</span></label>`).join('')}</div>`;
}

function draftScheduleRows() {
  return state.courseDraftSchedules.map(schedule => `
    <div class="schedule-row">
      <button class="schedule-main" type="button" data-edit-draft-schedule="${schedule.id}">
        <strong>${schedule.time} — ${doseText(schedule.amount, schedule.unit)}</strong>
        <span>${daysText(schedule.days)}</span>
      </button>
      <button class="mini-button danger" type="button" data-delete-draft-schedule="${schedule.id}" aria-label="Удалить время">×</button>
    </div>
  `).join('') || '<p class="compact-text">Добавьте хотя бы одно время приёма.</p>';
}

function refreshDraftScheduleList() {
  const list = document.querySelector('#draft-schedule-list');
  if (list) list.innerHTML = draftScheduleRows();
}

function fillDraftScheduleEditor(schedule) {
  const hour = document.querySelector('[name="draftTimeHour"]');
  const minute = document.querySelector('[name="draftTimeMinute"]');
  const amount = document.querySelector('[name="draftAmount"]');
  const unit = document.querySelector('[name="draftUnit"]');
  if (!hour || !minute || !amount || !unit) return;
  const [scheduleHour, scheduleMinute] = (schedule?.time || '09:00').split(':');
  hour.value = scheduleHour;
  minute.value = scheduleMinute;
  amount.value = schedule?.amount || 1;
  unit.value = schedule?.unit || 'таблетка';
  document.querySelectorAll('[name="draftDays"]').forEach(input => {
    input.checked = schedule ? schedule.days.includes(Number(input.value)) : true;
  });
  const button = document.querySelector('#save-draft-schedule');
  if (button) button.textContent = schedule ? 'Сохранить время' : 'Добавить это время';
}

function renderCourseCreate() {
  const options = state.catalog.filter(item => item.active).map(item => `<option value="${item.id}">${safe(item.name)} — ${safe(item.strength)}</option>`).join('');
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Новое лекарство', 'medicines')}
      <form id="course-create-form">
        <label class="field-label">Источник</label>
        <select class="detail-field" name="source" id="course-source"><option value="catalog">Из справочника</option><option value="custom">Своё название</option></select>
        <div id="catalog-course-field"><label class="field-label">Лекарство</label><select class="detail-field" name="medicationId">${options}</select></div>
        <div id="custom-course-field" class="hidden"><label class="field-label">Название</label><input class="detail-field" name="customName" placeholder="Название лекарства"></div>
        <div class="two-columns">
          <label class="field-label">Начало<input class="detail-field" name="start" type="date" value="2026-09-25" required></label>
          <label class="field-label">Конец<input class="detail-field" name="end" type="date"></label>
        </div>
        <label class="field-label">Режим приёма</label>
        <select class="detail-field" name="mode" id="course-mode"><option value="scheduled">По расписанию</option><option value="as_needed">По необходимости</option></select>
        <div id="initial-schedule">
          <label class="section-title">Добавленные времена</label>
          <div class="detail-card draft-schedule-list" id="draft-schedule-list">${draftScheduleRows()}</div>
          <div class="schedule-editor">
            <h2 class="section-title">Новое время</h2>
            ${timePicker('draftTime', '09:00')}
            <div class="two-columns">
              <label class="field-label">Доза<input class="detail-field" name="draftAmount" type="number" min="0.1" step="0.1" value="1"></label>
              <label class="field-label">Единица<select class="detail-field" name="draftUnit"><option>таблетка</option><option>мг</option><option>мл</option><option>капсула</option><option>капля</option></select></label>
            </div>
            <label class="section-title">Дни приёма</label>
            ${daysPicker(undefined, 'draftDays')}
            <p class="form-error" id="draft-schedule-error"></p>
            <button class="choice-button" id="save-draft-schedule" type="button">Добавить это время</button>
          </div>
        </div>
        <label class="section-title">Заметки</label>
        <textarea class="notes" name="notes" placeholder="Например: после еды"></textarea>
        <button class="action-button primary wide-button" type="submit">Добавить курс</button>
      </form>
    </section>
  `;
}

function renderScheduleForm() {
  const course = state.courses.find(item => item.id === state.selectedCourseId);
  const schedule = course?.schedules.find(item => item.id === state.editingScheduleId);
  app.innerHTML = `
    <section class="screen no-nav">
      ${header(schedule ? 'Изменить расписание' : 'Новое расписание', 'course-detail')}
      <form id="schedule-form">
        <label class="field-label">Время</label>
        ${timePicker('time', schedule?.time || '09:00')}
        <div class="two-columns">
          <label class="field-label">Доза<input class="detail-field" name="amount" type="number" min="0.1" step="0.1" value="${schedule?.amount || 1}" required></label>
          <label class="field-label">Единица<select class="detail-field" name="unit">${['таблетка', 'мг', 'мл', 'капсула', 'капля'].map(unit => `<option ${schedule?.unit === unit ? 'selected' : ''}>${unit}</option>`).join('')}</select></label>
        </div>
        <label class="section-title">Дни приёма</label>
        ${daysPicker(schedule?.days)}
        <button class="action-button primary wide-button" type="submit">Сохранить</button>
      </form>
    </section>
  `;
}

function renderAsNeeded() {
  const courses = state.courses.filter(course => course.active);
  const medications = state.catalog.filter(item => item.active);
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Внеплановый приём', state.selectedCourseId ? 'course-detail' : 'calendar')}
      <form id="as-needed-form">
        <input id="intake-source" name="source" type="hidden" value="course">
        <div id="existing-intake-course">
          <label class="field-label">Из моих курсов</label>
          <select class="detail-field" name="courseId">${courses.map(course => `<option value="${course.id}" ${course.id === state.selectedCourseId ? 'selected' : ''}>${safe(course.name)}</option>`).join('')}</select>
        </div>
        <div id="other-intake-course" class="hidden">
          <label class="field-label">Лекарство без курса</label>
          <select class="detail-field" id="intake-other-source" name="otherSource">
            <option value="catalog">Из справочника</option>
            <option value="custom">Ввести своё название</option>
          </select>
          <div id="intake-catalog-field">
            <label class="field-label">Лекарство из справочника</label>
            <select class="detail-field" name="medicationId">${medications.map(item => `<option value="${item.id}">${safe(item.name)} — ${safe(item.strength)}</option>`).join('')}</select>
          </div>
          <div id="intake-custom-field" class="hidden">
            <label class="field-label">Название лекарства</label>
            <input class="detail-field" name="customName" placeholder="Введите название">
          </div>
          <p class="form-hint">Курс не создаётся. В историю сохранится только название лекарства, без ID из справочника.</p>
        </div>
        <button class="choice-button" type="button" id="toggle-other-intake">Записать без курса</button>
        <div class="two-columns">
          <label class="field-label">Фактическая доза<input class="detail-field" name="amount" type="number" min="0.1" step="0.1" value="1" required></label>
          <label class="field-label">Единица<select class="detail-field" name="unit"><option>таблетка</option><option>мг</option><option>мл</option><option>капсула</option><option>капля</option></select></label>
        </div>
        <label class="field-label">Дата</label>
        <input class="detail-field" name="date" type="date" value="${selectedDate()}" required>
        <label class="field-label">Время</label>
        ${timePicker('time', '15:30')}
        <button class="action-button primary wide-button" type="submit">Записать приём</button>
      </form>
    </section>
  `;
}

function filteredCatalog() {
  const query = state.catalogQuery.toLowerCase();
  return state.catalog.filter(item => {
    const found = `${item.name} ${item.international}`.toLowerCase().includes(query);
    const category = !state.categoryFilter || item.category === state.categoryFilter;
    const form = !state.formFilter || item.form === state.formFilter;
    return found && category && form && (state.role === 'admin' || item.active);
  });
}

function renderCatalog() {
  const categories = [...new Set(state.catalog.map(item => item.category))];
  const forms = [...new Set(state.catalog.map(item => item.form))];
  const rows = filteredCatalog().map(item => `
    <button class="catalog-row ${item.active ? '' : 'inactive'}" data-catalog-item="${item.id}">
      <span>${safe(item.name)} (${safe(item.international)})</span>
      ${item.active ? '' : '<span class="badge">Скрыто</span>'}
    </button>
  `).join('');
  app.innerHTML = `
    <section class="screen ${state.guest ? 'guest-screen' : ''}">
      <h1 class="title">Справочник</h1>
      ${state.guest ? '<button class="guest-login" data-page="auth">Войти</button>' : ''}
      <input class="search" id="catalog-search" value="${safe(state.catalogQuery)}" placeholder="Найти лекарство...">
      <div class="filter-row">
        <select id="category-filter"><option value="">Все категории</option>${categories.map(item => `<option ${state.categoryFilter === item ? 'selected' : ''}>${safe(item)}</option>`).join('')}</select>
        <select id="form-filter"><option value="">Все формы</option>${forms.map(item => `<option ${state.formFilter === item ? 'selected' : ''}>${safe(item)}</option>`).join('')}</select>
      </div>
      <div class="catalog-list">${rows || '<div class="empty-state">Ничего не найдено</div>'}</div>
    </section>
    ${nav('catalog')}
    ${state.role === 'admin' && !state.guest ? '<button class="floating-button" data-admin-edit="new" aria-label="Добавить препарат">+</button>' : ''}
  `;
}

function renderCatalogDetail() {
  const item = state.catalog.find(medication => medication.id === state.selectedMedicationId);
  if (!item) return renderCatalog();
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('О препарате', 'catalog')}
      <article class="detail-card medication-detail">
        <h2 class="medicine-name">${safe(item.name)}</h2>
        <p class="international-name">${safe(item.international)}</p>
        <div class="info-grid">
          <span class="info-label">Производитель</span><span>${safe(item.manufacturer)}</span>
          <span class="info-label">Категория</span><span>${safe(item.category)}</span>
          <span class="info-label">Форма</span><span>${safe(item.form)}</span>
          <span class="info-label">Дозировка</span><span>${safe(item.strength)}</span>
        </div>
      </article>
      <button class="action-button primary wide-button" data-instruction="${item.id}">Открыть инструкцию</button>
      ${state.loggedIn && !state.guest ? `<button class="action-button wide-button" data-add-from-catalog="${item.id}">Добавить в мои лекарства</button>` : ''}
      ${state.role === 'admin' && !state.guest ? `<button class="action-button wide-button" data-admin-edit="${item.id}">Редактировать</button>` : ''}
    </section>
    ${toast()}
  `;
}

function renderHistory() {
  const items = state.intakes
    .filter(item => !state.historyCourseId || (state.historyCourseId === 'standalone' ? !item.courseId : item.courseId === state.historyCourseId))
    .sort((a, b) => `${b.date}${b.time}`.localeCompare(`${a.date}${a.time}`));
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('История приёмов', state.historyCourseId === 'standalone' ? 'calendar' : state.historyCourseId ? 'course-detail' : 'settings')}
      <label class="field-label">Лекарство</label>
      <select class="detail-field" id="history-filter">
        <option value="">Все лекарства</option>
        <option value="standalone" ${state.historyCourseId === 'standalone' ? 'selected' : ''}>Без курса</option>
        ${state.courses.map(course => `<option value="${course.id}" ${course.id === state.historyCourseId ? 'selected' : ''}>${safe(course.name)}</option>`).join('')}
      </select>
      <div class="history-list">${items.map(item => {
        return `<button class="history-card" data-intake="${item.id}"><strong>${safe(item.medicationName)}</strong><span>${doseText(item.amount, item.unit)}</span><span>${formatDate(item.date)}, ${item.time}</span>${item.courseId ? '' : '<small>Без курса</small>'}</button>`;
      }).join('') || '<div class="empty-state">История пока пуста</div>'}</div>
    </section>
  `;
}

function renderIntakeEdit() {
  const intake = state.intakes.find(item => item.id === state.selectedIntakeId);
  if (!intake) return renderHistory();
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Запись о приёме', 'history')}
      <h2 class="section-title">${safe(intake.medicationName)}</h2>
      <form id="intake-edit-form">
        <div class="two-columns">
          <label class="field-label">Фактическая доза<input class="detail-field" name="amount" type="number" min="0.1" step="0.1" value="${intake.amount}" required></label>
          <label class="field-label">Единица<select class="detail-field" name="unit">${['таблетка', 'мг', 'мл', 'капсула', 'капля'].map(unit => `<option ${intake.unit === unit ? 'selected' : ''}>${unit}</option>`).join('')}</select></label>
        </div>
        <label class="field-label">Дата</label>
        <input class="detail-field" name="date" type="date" value="${intake.date}" required>
        <label class="field-label">Время</label>
        ${timePicker('time', intake.time)}
        <div class="stack-actions">
          <button class="action-button primary" type="submit">Сохранить</button>
          <button class="action-button danger" type="button" data-delete-intake="${intake.id}">Удалить запись</button>
        </div>
      </form>
    </section>
  `;
}

function renderSettings() {
  app.innerHTML = `
    <section class="screen">
      <h1 class="title">Настройки</h1>
      <button class="settings-card" data-page="profile">
        <span class="avatar">${safe(state.profile.name.slice(0, 1))}</span>
        <span><strong>${safe(state.profile.name)}</strong><small>${safe(state.profile.email)}</small></span><b>›</b>
      </button>
      <article class="settings-section">
        <h2 class="section-title">Напоминания</h2>
        <label class="toggle-row"><span>Уведомления о приёме</span><input id="notifications-toggle" type="checkbox" ${state.notifications ? 'checked' : ''}></label>
        <label class="field-label">Напоминать заранее</label>
        <select class="detail-field" id="reminder-minutes">${[5, 10, 15, 30, 60].map(value => `<option value="${value}" ${state.reminderMinutes === value ? 'selected' : ''}>За ${value} минут</option>`).join('')}</select>
      </article>
      <div class="menu-list">
        <button data-page="history"><span>История приёмов</span><b>›</b></button>
        <button id="role-toggle"><span>Демо-роль</span><small>${state.role === 'admin' ? 'Администратор' : 'Пользователь'}</small></button>
        ${state.role === 'admin' ? '<button data-page="admin"><span>Управление справочником</span><b>›</b></button>' : ''}
        <button id="logout"><span>Выйти из аккаунта</span><b>›</b></button>
      </div>
    </section>
    ${nav('settings')}
    ${toast()}
  `;
}

function renderProfile() {
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Профиль', 'settings')}
      <form id="profile-form">
        <div class="profile-avatar">${safe(state.profile.name.slice(0, 1))}</div>
        <label class="field-label">Имя</label><input class="detail-field" name="name" value="${safe(state.profile.name)}" required>
        <label class="field-label">Email</label><input class="detail-field" value="${safe(state.profile.email)}" readonly>
        <label class="field-label">Дата рождения</label><input class="detail-field" name="birthDate" type="date" value="${state.profile.birthDate}">
        <label class="field-label">Ссылка на аватар</label><input class="detail-field" name="avatar" value="${safe(state.profile.avatar)}" placeholder="Не указана">
        <button class="action-button primary wide-button" type="submit">Сохранить</button>
      </form>
    </section>
    ${toast()}
  `;
}

function renderAdmin() {
  const query = state.adminQuery.toLowerCase();
  const rows = state.catalog.filter(item => `${item.name} ${item.international} ${item.manufacturer}`.toLowerCase().includes(query)).map(item => `
    <button class="admin-row" data-admin-edit="${item.id}">
      <span><strong>${safe(item.name)}</strong><small>${safe(item.form)}, ${safe(item.strength)}</small></span>
      <span class="badge">${item.active ? 'Активно' : 'Скрыто'}</span>
    </button>
  `).join('');
  app.innerHTML = `
    <section class="screen no-nav">
      ${header('Управление справочником', 'settings')}
      <input class="search" id="admin-search" value="${safe(state.adminQuery)}" placeholder="Найти препарат...">
      <div class="catalog-list">${rows || '<div class="empty-state">Ничего не найдено</div>'}</div>
    </section>
    <button class="floating-button" data-admin-edit="new" aria-label="Добавить препарат">+</button>
  `;
}

function renderAdminMedication() {
  const item = state.catalog.find(medication => medication.id === state.selectedMedicationId);
  app.innerHTML = `
    <section class="screen no-nav">
      ${header(item ? 'Редактировать препарат' : 'Новый препарат', 'admin')}
      <form id="admin-medication-form">
        <label class="field-label">Название</label><input class="detail-field" name="name" value="${safe(item?.name || '')}" required>
        <label class="field-label">Международное название</label><input class="detail-field" name="international" value="${safe(item?.international || '')}" required>
        <label class="field-label">Производитель</label><input class="detail-field" name="manufacturer" value="${safe(item?.manufacturer || '')}" required>
        <label class="field-label">Категория</label><input class="detail-field" name="category" value="${safe(item?.category || '')}" required>
        <div class="two-columns">
          <label class="field-label">Форма<input class="detail-field" name="form" value="${safe(item?.form || '')}" required></label>
          <label class="field-label">Дозировка<input class="detail-field" name="strength" value="${safe(item?.strength || '')}" required></label>
        </div>
        <label class="section-title">Инструкция</label><textarea class="notes" name="instruction">${safe(item?.instruction || '')}</textarea>
        <label class="toggle-row"><span>Показывать в справочнике</span><input type="checkbox" name="active" ${item?.active !== false ? 'checked' : ''}></label>
        <button class="action-button primary wide-button" type="submit">Сохранить</button>
      </form>
    </section>
  `;
}

function renderAuth() {
  if (state.authStep === 'code') {
    app.innerHTML = `
      <section class="auth-screen">
        <div class="brand-mark">✚</div><h1 class="title">Проверьте почту</h1>
        <p class="auth-text">Мы отправили шестизначный код на<br><strong>${safe(state.email)}</strong></p>
        <form id="code-form"><input class="code-input" name="code" inputmode="numeric" maxlength="6" placeholder="000000" required><button class="action-button primary wide-button" type="submit">Войти</button></form>
        <button class="text-button" id="change-email">Изменить email</button>
      </section>
    `;
    return;
  }
  app.innerHTML = `
    <section class="auth-screen">
      <div class="brand-mark">✚</div><h1 class="title">Моя аптечка</h1>
      <p class="auth-text">Лекарства, расписание и история приёмов в одном месте</p>
      <form id="email-form">
        <label class="field-label">Электронная почта</label>
        <input class="detail-field" name="email" type="email" value="${safe(state.email)}" placeholder="name@example.com" required>
        <button class="action-button primary wide-button" type="submit">Получить код</button>
      </form>
      <button class="text-button" id="guest-mode">Продолжить как гость</button>
    </section>
  `;
}

function render() {
  const renders = {
    auth: renderAuth,
    calendar: renderCalendar,
    medicines: renderMedicines,
    'course-detail': renderCourseDetail,
    'course-create': renderCourseCreate,
    schedule: renderScheduleForm,
    'as-needed': renderAsNeeded,
    catalog: renderCatalog,
    'catalog-detail': renderCatalogDetail,
    history: renderHistory,
    'intake-edit': renderIntakeEdit,
    settings: renderSettings,
    profile: renderProfile,
    admin: renderAdmin,
    'admin-medication': renderAdminMedication
  };
  renders[state.page]();
}

app.addEventListener('click', event => {
  const pageButton = event.target.closest('[data-page]');
  const backButton = event.target.closest('[data-back]');
  const dayButton = event.target.closest('[data-day]');
  const intakeToggle = event.target.closest('[data-toggle-intake]');
  const courseCard = event.target.closest('[data-course]');
  const catalogItem = event.target.closest('[data-catalog-item]');
  const scheduleEdit = event.target.closest('[data-edit-schedule]');
  const scheduleDelete = event.target.closest('[data-delete-schedule]');
  const draftScheduleEdit = event.target.closest('[data-edit-draft-schedule]');
  const draftScheduleDelete = event.target.closest('[data-delete-draft-schedule]');
  const historyCourse = event.target.closest('[data-history-course]');
  const intakeCard = event.target.closest('[data-intake]');
  const adminEdit = event.target.closest('[data-admin-edit]');
  const quickTime = event.target.closest('[data-quick-time]');

  if (quickTime) {
    const [hour, minute] = quickTime.dataset.quickTime.split(':');
    const prefix = quickTime.dataset.timePrefix;
    const picker = document.querySelector(`[data-time-picker="${prefix}"]`);
    picker.querySelector(`[name="${prefix}Hour"]`).value = hour;
    picker.querySelector(`[name="${prefix}Minute"]`).value = minute;
    return;
  }
  if (event.target.closest('#save-draft-schedule')) {
    const amount = Number(document.querySelector('[name="draftAmount"]').value);
    const unit = document.querySelector('[name="draftUnit"]').value;
    const time = `${document.querySelector('[name="draftTimeHour"]').value}:${document.querySelector('[name="draftTimeMinute"]').value}`;
    const days = [...document.querySelectorAll('[name="draftDays"]:checked')].map(input => Number(input.value));
    const error = document.querySelector('#draft-schedule-error');
    if (!amount || !days.length) {
      error.textContent = !days.length ? 'Выберите хотя бы один день.' : 'Укажите дозу.';
      return;
    }
    const schedule = state.courseDraftSchedules.find(item => item.id === state.editingDraftScheduleId);
    if (schedule) Object.assign(schedule, { time, amount, unit, days });
    else state.courseDraftSchedules.push({ id: `draft-${Date.now()}`, time, amount, unit, days });
    state.editingDraftScheduleId = null;
    error.textContent = '';
    refreshDraftScheduleList();
    fillDraftScheduleEditor(null);
    return;
  }
  if (draftScheduleEdit) {
    state.editingDraftScheduleId = draftScheduleEdit.dataset.editDraftSchedule;
    fillDraftScheduleEditor(state.courseDraftSchedules.find(item => item.id === state.editingDraftScheduleId));
    return;
  }
  if (draftScheduleDelete) {
    state.courseDraftSchedules = state.courseDraftSchedules.filter(item => item.id !== draftScheduleDelete.dataset.deleteDraftSchedule);
    if (state.editingDraftScheduleId === draftScheduleDelete.dataset.deleteDraftSchedule) {
      state.editingDraftScheduleId = null;
      fillDraftScheduleEditor(null);
    }
    refreshDraftScheduleList();
    return;
  }
  if (event.target.closest('#toggle-other-intake')) {
    const source = document.querySelector('#intake-source');
    const useOther = source.value !== 'other';
    source.value = useOther ? 'other' : 'course';
    document.querySelector('#existing-intake-course').classList.toggle('hidden', useOther);
    document.querySelector('#other-intake-course').classList.toggle('hidden', !useOther);
    event.target.closest('#toggle-other-intake').textContent = useOther ? 'Выбрать из моих курсов' : 'Записать без курса';
    return;
  }

  if (pageButton) {
    if (pageButton.dataset.page === 'as-needed' && state.page === 'calendar') state.selectedCourseId = '';
    if (pageButton.dataset.page === 'history') state.historyCourseId = '';
    if (pageButton.dataset.page === 'course-create') {
      state.courseDraftSchedules = [];
      state.editingDraftScheduleId = null;
    }
    if (pageButton.dataset.page === 'auth') {
      state.guest = false;
      state.authStep = 'email';
    }
    state.page = pageButton.dataset.page;
    render();
    return;
  }
  if (backButton) {
    state.page = backButton.dataset.back;
    render();
    return;
  }
  if (dayButton) {
    state.selectedDay = Number(dayButton.dataset.day);
    renderCalendar();
    return;
  }
  if (intakeToggle) {
    const scheduleId = intakeToggle.dataset.toggleIntake;
    const date = selectedDate();
    const existing = state.intakes.find(item => item.date === date && item.scheduleId === scheduleId);
    if (existing) {
      state.intakes = state.intakes.filter(item => item.id !== existing.id);
    } else {
      const course = state.courses.find(item => item.schedules.some(schedule => schedule.id === scheduleId));
      const schedule = course.schedules.find(item => item.id === scheduleId);
      state.intakes.push({ id: `i${Date.now()}`, courseId: course.id, scheduleId, medicationName: course.name, date, time: schedule.time, amount: schedule.amount, unit: schedule.unit });
    }
    renderCalendar();
    return;
  }
  if (courseCard) {
    state.selectedCourseId = courseCard.dataset.course;
    state.page = 'course-detail';
    render();
    return;
  }
  if (catalogItem) {
    state.selectedMedicationId = Number(catalogItem.dataset.catalogItem);
    state.page = 'catalog-detail';
    render();
    return;
  }
  if (scheduleEdit) {
    state.editingScheduleId = scheduleEdit.dataset.editSchedule === 'new' ? null : scheduleEdit.dataset.editSchedule;
    state.page = 'schedule';
    render();
    return;
  }
  if (scheduleDelete) {
    const course = state.courses.find(item => item.id === state.selectedCourseId);
    const scheduleId = scheduleDelete.dataset.deleteSchedule;
    course.schedules = course.schedules.filter(item => item.id !== scheduleId);
    course.mode = course.schedules.length ? 'scheduled' : 'as_needed';
    state.intakes.filter(item => item.scheduleId === scheduleId).forEach(item => { item.scheduleId = null; });
    renderCourseDetail();
    return;
  }
  if (historyCourse) {
    state.historyCourseId = historyCourse.dataset.historyCourse;
    state.page = 'history';
    render();
    return;
  }
  if (intakeCard) {
    state.selectedIntakeId = intakeCard.dataset.intake;
    state.page = 'intake-edit';
    render();
    return;
  }
  if (adminEdit) {
    state.selectedMedicationId = adminEdit.dataset.adminEdit === 'new' ? null : Number(adminEdit.dataset.adminEdit);
    state.page = 'admin-medication';
    render();
    return;
  }
  const addFromCatalog = event.target.closest('[data-add-from-catalog]');
  if (addFromCatalog) {
    const medication = state.catalog.find(item => item.id === Number(addFromCatalog.dataset.addFromCatalog));
    const id = `c${Date.now()}`;
    state.courses.unshift({ id, medicationId: medication.id, name: medication.name, mode: 'as_needed', start: '2026-09-25', end: '', active: true, notes: '', schedules: [] });
    state.selectedCourseId = id;
    state.page = 'course-detail';
    render();
    return;
  }
  if (event.target.closest('[data-instruction]')) {
    showToast('Инструкция открыта в режиме макета');
    return;
  }

  const deleteCourse = event.target.closest('[data-delete-course]');
  if (deleteCourse) {
    const id = deleteCourse.dataset.deleteCourse;
    state.courses = state.courses.filter(item => item.id !== id);
    state.intakes.filter(item => item.courseId === id).forEach(item => {
      item.courseId = null;
      item.scheduleId = null;
    });
    state.page = 'medicines';
    render();
    return;
  }

  const deleteIntake = event.target.closest('[data-delete-intake]');
  if (deleteIntake) {
    state.intakes = state.intakes.filter(item => item.id !== deleteIntake.dataset.deleteIntake);
    state.page = 'history';
    render();
    return;
  }
  if (event.target.closest('#role-toggle')) {
    state.role = state.role === 'admin' ? 'user' : 'admin';
    showToast(state.role === 'admin' ? 'Включён режим администратора' : 'Включён режим пользователя');
    return;
  }
  if (event.target.closest('#logout')) {
    state.loggedIn = false;
    state.guest = false;
    state.page = 'auth';
    state.authStep = 'email';
    render();
    return;
  }
  if (event.target.closest('#guest-mode')) {
    state.guest = true;
    state.loggedIn = false;
    state.role = 'user';
    state.page = 'catalog';
    render();
    return;
  }
  if (event.target.closest('#change-email')) {
    state.authStep = 'email';
    renderAuth();
  }
});

app.addEventListener('input', event => {
  if (event.target.id === 'medicine-search') {
    state.courseQuery = event.target.value;
    renderMedicines();
    const search = document.querySelector('#medicine-search');
    search?.focus();
    search?.setSelectionRange(search.value.length, search.value.length);
  }
  if (event.target.id === 'catalog-search') {
    state.catalogQuery = event.target.value;
    renderCatalog();
    const search = document.querySelector('#catalog-search');
    search?.focus();
    search?.setSelectionRange(search.value.length, search.value.length);
  }
  if (event.target.id === 'admin-search') {
    state.adminQuery = event.target.value;
    renderAdmin();
    const search = document.querySelector('#admin-search');
    search?.focus();
    search?.setSelectionRange(search.value.length, search.value.length);
  }
});

app.addEventListener('change', event => {
  if (event.target.id === 'category-filter') {
    state.categoryFilter = event.target.value;
    renderCatalog();
  }
  if (event.target.id === 'form-filter') {
    state.formFilter = event.target.value;
    renderCatalog();
  }
  if (event.target.id === 'history-filter') {
    state.historyCourseId = event.target.value;
    renderHistory();
  }
  if (event.target.id === 'notifications-toggle') {
    state.notifications = event.target.checked;
    showToast(state.notifications ? 'Уведомления включены' : 'Уведомления выключены');
  }
  if (event.target.id === 'reminder-minutes') {
    state.reminderMinutes = Number(event.target.value);
    showToast('Настройка сохранена');
  }
  if (event.target.id === 'course-source') {
    document.querySelector('#catalog-course-field').classList.toggle('hidden', event.target.value !== 'catalog');
    document.querySelector('#custom-course-field').classList.toggle('hidden', event.target.value !== 'custom');
  }
  if (event.target.id === 'course-mode') {
    document.querySelector('#initial-schedule').classList.toggle('hidden', event.target.value === 'as_needed');
  }
  if (event.target.id === 'intake-other-source') {
    document.querySelector('#intake-catalog-field').classList.toggle('hidden', event.target.value !== 'catalog');
    document.querySelector('#intake-custom-field').classList.toggle('hidden', event.target.value !== 'custom');
  }
});

app.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(event.target);

  if (event.target.id === 'email-form') {
    state.email = data.get('email').trim();
    state.authStep = 'code';
    renderAuth();
    return;
  }
  if (event.target.id === 'code-form') {
    state.loggedIn = true;
    state.guest = false;
    state.profile.email = state.email;
    state.page = 'calendar';
    render();
    return;
  }
  if (event.target.id === 'profile-form') {
    state.profile.name = data.get('name').trim();
    state.profile.birthDate = data.get('birthDate');
    state.profile.avatar = data.get('avatar').trim();
    showToast('Профиль сохранён');
    return;
  }
  if (event.target.id === 'course-create-form') {
    const medication = state.catalog.find(item => item.id === Number(data.get('medicationId')));
    const mode = data.get('mode');
    const name = data.get('source') === 'catalog' ? medication.name : data.get('customName').trim();
    if (!name) return;
    const id = `c${Date.now()}`;
    if (mode === 'scheduled' && !state.courseDraftSchedules.length) {
      document.querySelector('#draft-schedule-error').textContent = 'Добавьте хотя бы одно время приёма.';
      return;
    }
    const schedules = mode === 'scheduled'
      ? state.courseDraftSchedules.map((schedule, index) => ({ ...schedule, id: `s${Date.now()}-${index}` }))
      : [];
    state.courses.unshift({ id, medicationId: data.get('source') === 'catalog' ? medication.id : null, name, mode, start: data.get('start'), end: data.get('end'), active: true, notes: data.get('notes').trim(), schedules });
    state.selectedCourseId = id;
    state.courseDraftSchedules = [];
    state.page = 'course-detail';
    render();
    return;
  }
  if (event.target.id === 'course-edit-form') {
    const course = state.courses.find(item => item.id === state.selectedCourseId);
    course.start = data.get('start');
    course.end = data.get('end');
    course.notes = data.get('notes').trim();
    course.active = data.has('active');
    showToast('Курс сохранён');
    return;
  }
  if (event.target.id === 'schedule-form') {
    const course = state.courses.find(item => item.id === state.selectedCourseId);
    const values = { time: formTime(data, 'time'), amount: Number(data.get('amount')), unit: data.get('unit'), days: data.getAll('days').map(Number) };
    if (!values.days.length) return;
    const schedule = course.schedules.find(item => item.id === state.editingScheduleId);
    if (schedule) Object.assign(schedule, values);
    else course.schedules.push({ id: `s${Date.now()}`, ...values });
    course.mode = 'scheduled';
    state.page = 'course-detail';
    render();
    return;
  }
  if (event.target.id === 'as-needed-form') {
    let courseId = data.get('courseId');
    let medicationName;
    if (data.get('source') === 'other') {
      const medication = state.catalog.find(item => item.id === Number(data.get('medicationId')));
      medicationName = data.get('otherSource') === 'catalog' ? medication.name : data.get('customName').trim();
      if (!medicationName) return;
      courseId = null;
    } else {
      const course = state.courses.find(item => item.id === courseId);
      medicationName = course.name;
    }
    state.intakes.push({
      id: `i${Date.now() + 1}`,
      courseId,
      scheduleId: null,
      medicationName,
      date: data.get('date'),
      time: formTime(data, 'time'),
      amount: Number(data.get('amount')),
      unit: data.get('unit')
    });
    state.historyCourseId = courseId || 'standalone';
    state.page = 'history';
    render();
    return;
  }
  if (event.target.id === 'intake-edit-form') {
    const intake = state.intakes.find(item => item.id === state.selectedIntakeId);
    intake.date = data.get('date');
    intake.time = formTime(data, 'time');
    intake.amount = Number(data.get('amount'));
    intake.unit = data.get('unit');
    showToast('Запись сохранена');
    return;
  }
  if (event.target.id === 'admin-medication-form') {
    const values = {
      name: data.get('name').trim(),
      international: data.get('international').trim(),
      manufacturer: data.get('manufacturer').trim(),
      category: data.get('category').trim(),
      form: data.get('form').trim(),
      strength: data.get('strength').trim(),
      instruction: data.get('instruction').trim(),
      active: data.has('active')
    };
    const item = state.catalog.find(medication => medication.id === state.selectedMedicationId);
    if (item) Object.assign(item, values);
    else state.catalog.push({ id: Math.max(...state.catalog.map(medication => medication.id)) + 1, ...values });
    state.page = 'admin';
    render();
  }
});

render();
