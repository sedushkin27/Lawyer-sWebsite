document.addEventListener('DOMContentLoaded', () => {
  initCalendar()
});

function initCalendar() {
  const containerCalendar = document.querySelector('.container-calendar');
  const containerInputInfo = document.querySelector('.container-input-info');
  const datetimeInput = document.querySelector('#datetime_refistration');

  if (!containerCalendar || !containerInputInfo || !datetimeInput) return;

  const availableDates = [
    new Date(2025, 3, 1),
    new Date(2025, 3, 5),
    new Date(2025, 5, 10),
    new Date(2025, 5, 15)
  ];

  const availableTimes = {
    "2025-04-01": ["11:20", "12:30"],
    "2025-04-05": ["14:00", "15:30"],
    "2025-06-10": ["09:00", "10:30"],
    "2025-06-15": ["13:00", "16:00"]
  };

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

const header = document.querySelector('header');
let lastScrollTop = 0;

window.addEventListener('scroll', () => {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  header.classList.toggle('scrolled', currentScrollTop > 0);
  header.classList.toggle('hidden', currentScrollTop > lastScrollTop && currentScrollTop > 0);
  lastScrollTop = Math.max(0, currentScrollTop);
});