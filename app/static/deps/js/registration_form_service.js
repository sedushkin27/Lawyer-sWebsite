document.addEventListener('DOMContentLoaded', () => {
  initCalendar();
  phoneInput();
  characterCounter();
  validateForm();
});

function initCalendar() {
  const containerCalendar = document.querySelector('.container-calendar');
  const containerInputInfo = document.querySelector('.container-input-info');
  const datetimeInput = document.querySelector('#datetime_refistration');

  if (!containerCalendar || !containerInputInfo || !datetimeInput) return;

  const availableDates = JSON.parse(document.getElementById('available-dates').textContent).map(date => new Date(date));
  const availableTimes = JSON.parse(document.getElementById('available-times').textContent);

  const minDate = new Date(Math.min(...availableDates.map(d => d.getTime())));
  const maxDate = new Date(Math.max(...availableDates.map(d => d.getTime())));
  let currentDate = new Date(minDate);

  const formatDate = date => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  const isDateAvailable = date => availableDates.some(d => formatDate(d) === formatDate(date));

  const generateCalendar = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const months = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"];

    containerCalendar.innerHTML = '<h2>Оберіть дату та час консультації</h2>';

    const calendarHeader = document.createElement('div');
    calendarHeader.className = 'calendar-header';
    calendarHeader.innerHTML = `
      <button type="button" class="nav-button prev-month">&lt;</button>
      <h2>${months[month]} ${year}</h2>
      <button type="button" class="nav-button next-month">&gt;</button>
    `;
    containerCalendar.appendChild(calendarHeader);

    const daysOfWeek = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'НД'];
    const daysHeader = document.createElement('div');
    daysHeader.className = 'days-of-week';
    daysOfWeek.forEach(day => {
      const dayElement = document.createElement('span');
      dayElement.textContent = day;
      daysHeader.appendChild(dayElement);
    });
    containerCalendar.appendChild(daysHeader);

    const daysContainer = document.createElement('div');
    daysContainer.className = 'days-container';
    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;

    for (let i = 0; i < startDay; i++) {
      const emptyDay = document.createElement('div');
      emptyDay.className = 'day empty';
      daysContainer.appendChild(emptyDay);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const dayElement = document.createElement('div');
      dayElement.className = 'day';
      dayElement.textContent = String(day).padStart(2, '0');

      if (isDateAvailable(date)) {
        dayElement.classList.add('available');
        dayElement.addEventListener('click', () => selectDate(date, dayElement));
      } else {
        dayElement.classList.add('unavailable');
      }

      daysContainer.appendChild(dayElement);
    }

    containerCalendar.appendChild(daysContainer);

    const prevButton = containerCalendar.querySelector('.prev-month');
    const nextButton = containerCalendar.querySelector('.next-month');
    prevButton.disabled = year === minDate.getFullYear() && month === minDate.getMonth();
    nextButton.disabled = year === maxDate.getFullYear() && month === maxDate.getMonth();

    prevButton.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      generateCalendar();
    });

    nextButton.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      generateCalendar();
    });
  };

  const selectDate = (date, dayElement) => {
    const allDays = containerCalendar.querySelectorAll('.day');
    allDays.forEach(day => day.classList.remove('selected'));
    dayElement.classList.add('selected');

    const dateStr = formatDate(date);
    const times = availableTimes[dateStr] || [];
    let timeContainer = containerCalendar.querySelector('.time-container');
    if (!timeContainer) {
      timeContainer = document.createElement('div');
      timeContainer.className = 'time-container';
      const line = document.createElement('hr');
      line.className = 'dividing-line';
      containerCalendar.appendChild(line);
      containerCalendar.appendChild(timeContainer);
    }

    timeContainer.innerHTML = '';
    times.forEach(time => {
      const timeButton = document.createElement('button');
      timeButton.className = 'time-button';
      timeButton.type = 'button';
      timeButton.textContent = time;
      timeButton.addEventListener('click', () => {
        const datetime = `${dateStr} ${time}`;
        datetimeInput.value = datetime;

        const allTimeButtons = containerCalendar.querySelectorAll('.time-button');
        allTimeButtons.forEach(btn => btn.classList.remove('selected'));
        timeButton.classList.add('selected');

        containerCalendar.classList.add('hidden');
        containerInputInfo.classList.remove('hidden');
      });
      timeContainer.appendChild(timeButton);
    });
  };

  generateCalendar();
}

function phoneInput() {
  const telInput = document.getElementById('userstel');
  if (!telInput) return;
  telInput.addEventListener('input', () => {
    let value = telInput.value.replace(/\D/g, '');
    if (value.length > 9) value = value.slice(0, 9);

    let formattedValue = '';
    if (value.length > 0) formattedValue += value.slice(0, 2);
    if (value.length > 2) formattedValue += '-' + value.slice(2, 5);
    if (value.length > 5) formattedValue += '-' + value.slice(5, 7);
    if (value.length > 7) formattedValue += '-' + value.slice(7, 9);

    telInput.value = formattedValue;
    telInput.classList.toggle('invalid', value.length !== 9);
  });
}

function characterCounter() {
  const commentInput = document.querySelector('.input-comment');
  const counter = document.querySelector('.character-counter');

  if (!commentInput || !counter) return;

  commentInput.addEventListener('input', () => {
    const length = commentInput.value.length;
    counter.textContent = `${length}/3000`;
    if (length < 3000) {
      counter.classList.remove('full');
    }
    if (length >= 3000) {
      commentInput.value = commentInput.value.slice(0, 3000);
      counter.textContent = '3000/3000';
      counter.classList.add('full');
    }
  });
};

function validateForm() {
  const form = document.querySelector('.registration-form');
  const errorContainer = document.querySelector('.container-error');
  const errorTitle = errorContainer.querySelector('.error-message h4');
  const errorText = errorContainer.querySelector('.error-message p');

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('name').value.trim();
    const surname = document.getElementById('surname').value.trim();
    const tel = document.getElementById('userstel').value.replace(/\D/g, '');
    const email = document.getElementById('email').value.trim();

    errorContainer.classList.add('hidden');

    if (!name || !surname || !tel) {
      showError('Помилка заповнення форми', 'Будь ласка, заповніть всі обов\'язкові поля. Такі як ім\'я, прізвище, телефон.');
      return;
    } else if (name.length <= 2 || surname.length <= 2) {
      showError('Помилка заповнення форми', 'Ім\'я та прізвище повинні містити не менше 2 символів.');
      return;
    } else if (email != '' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showError('Помилка заповнення форми', 'Будь ласка, введіть коректну електронну адресу.');
      return;
    } else if (tel.length < 9 || !/^\d+$/.test(tel)) {
      showError('Помилка заповнення форми', 'Будь ласка, введіть коректний номер телефону (не менше 10 цифр).');
      return;
    };

    document.getElementById('userstel').value = tel;
    
    form.submit();
  })

  function showError(title, text) {
    errorTitle.textContent = title;
    errorText.textContent = text;
    errorContainer.classList.remove('hidden');
  }
}

const header = document.querySelector('header');
let lastScrollTop = 0;

window.addEventListener('scroll', () => {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  header.classList.toggle('scrolled', currentScrollTop > 0);
  header.classList.toggle('hidden', currentScrollTop > lastScrollTop && currentScrollTop > 0);
  lastScrollTop = Math.max(0, currentScrollTop);
});