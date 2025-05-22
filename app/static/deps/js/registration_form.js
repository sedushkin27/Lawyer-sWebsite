function initCalendar() {
    // Имитация данных с бэкенда
    const availableDates = [
        new Date(2025, 3, 1),  // 1 апреля 2025
        new Date(2025, 3, 5),  // 5 апреля 2025
        new Date(2025, 5, 10), // 10 июня 2025
        new Date(2025, 5, 15)  // 15 июня 2025
    ];
  
    const availableTimes = {
        "2025-04-01": ["11:20", "12:30"],
        "2025-04-05": ["14:00", "15:30"],
        "2025-06-10": ["09:00", "10:30"],
        "2025-06-15": ["13:00", "16:00"]
    };
  
    const containerCalendar = document.querySelector('.container-calendar');
    const containerInputInfo = document.querySelector('.container-input-info');
    const datetimeInput = document.querySelector('#datetime_refistration');
  
    // Определяем минимальный и максимальный месяцы
    const minDate = new Date(Math.min(...availableDates.map(d => d.getTime())));
    const maxDate = new Date(Math.max(...availableDates.map(d => d.getTime())));
    let currentDate = new Date(minDate);
  
    // Функция форматирования даты в строку YYYY-MM-DD
    const formatDate = (date) => {
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    };
  
    // Функция для проверки, является ли день доступным
    const isDateAvailable = (date) => {
        return availableDates.some(d => formatDate(d) === formatDate(date));
    };
  
    // Генерация календаря
    const generateCalendar = () => {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        
        // Названия месяцев на украинском
        const months = [
            "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
            "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
        ];
  
        // Очистка контейнера
        containerCalendar.innerHTML = '<h2>Оберіть дату та час консультації</h2>';
  
        // Заголовок календаря
        const calendarHeader = document.createElement('div');
        calendarHeader.className = 'calendar-header';
        calendarHeader.innerHTML = `
            <button type="button" class="nav-button prev-month">&lt;</button>
            <h2>${months[month]} ${year}</h2>
            <button type="button" class="nav-button next-month">&gt;</button>
        `;
        containerCalendar.appendChild(calendarHeader);
  
        // Дни недели
        const daysOfWeek = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'НД'];
        const daysHeader = document.createElement('div');
        daysHeader.className = 'days-of-week';
        daysOfWeek.forEach(day => {
            const dayElement = document.createElement('span');
            dayElement.textContent = day;
            daysHeader.appendChild(dayElement);
        });
        containerCalendar.appendChild(daysHeader);
  
        // Дни месяца
        const daysContainer = document.createElement('div');
        daysContainer.className = 'days-container';
        
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const startDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
  
        // Добавляем пустые ячейки до первого дня
        for (let i = 0; i < startDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'day empty';
            daysContainer.appendChild(emptyDay);
        }
  
        // Добавляем дни месяца
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
  
        // Навигация по месяцам
        const prevButton = containerCalendar.querySelector('.prev-month');
        const nextButton = containerCalendar.querySelector('.next-month');
  
        prevButton.disabled = currentDate.getFullYear() === minDate.getFullYear() && currentDate.getMonth() === minDate.getMonth();
        nextButton.disabled = currentDate.getFullYear() === maxDate.getFullYear() && currentDate.getMonth() === maxDate.getMonth();
  
        prevButton.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            generateCalendar();
        });
  
        nextButton.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            generateCalendar();
        });
    };
  
    // Выбор даты и отображение времени
    const selectDate = (date, dayElement) => {
        // Удаляем выделение с других дней
        const allDays = containerCalendar.querySelectorAll('.day');
        allDays.forEach(day => day.classList.remove('selected'));
  
        // Выделяем выбранный день
        dayElement.classList.add('selected');
  
        // Формируем дату в формате YYYY-MM-DD
        const dateStr = formatDate(date);
  
        // Показываем доступное время
        const times = availableTimes[dateStr] || [];
        let timeContainer = containerCalendar.querySelector('.time-container');
        if (!timeContainer) {
            timeContainer = document.createElement('div');
            timeContainer.className = 'time-container';
            line = document.createElement('hr')
            line.className = 'dividing-line';
            containerCalendar.appendChild(line)
            containerCalendar.appendChild(timeContainer);
        }
  
        timeContainer.innerHTML = '';
        times.forEach(time => {
            const timeButton = document.createElement('button');
            timeButton.className = 'time-button';
            timeButton.type = 'button';
            timeButton.textContent = time;
            timeButton.addEventListener('click', () => {
                // Сохраняем выбранную дату и время
                const datetime = `${dateStr} ${time}`;
                datetimeInput.value = datetime;
  
                // Удаляем выделение с других кнопок времени
                const allTimeButtons = containerCalendar.querySelectorAll('.time-button');
                allTimeButtons.forEach(btn => btn.classList.remove('selected'));
  
                // Выделяем выбранное время
                timeButton.classList.add('selected');
  
                // Показываем форму для ввода информации
                containerCalendar.classList.add('hidden')
                containerInputInfo.classList.remove('hidden');
            });
            timeContainer.appendChild(timeButton);
        });
    };
  
    // Инициализация календаря
    generateCalendar();
  }
// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initCalendar();
});