// style/js/everywhere.js
barba.init({
  transitions: [{
    name: 'parallelogram-transition',
    async leave(data) {
      // Получаем элементы
      const overlay = document.querySelector('.transition-overlay');
      const logoContainer = document.querySelector('.container-logo');
      const transitionLogo = document.querySelector('.transition-logo');
      const menuHamburger = document.querySelector('.menu-hamburger');
      const dropMenu = document.querySelector('.drop-menu');
      const formContainer = document.querySelector('.container-form-call-us');

      // Проверяем, что overlay существует
      if (!overlay) {
        console.error('Overlay не найден!');
        return;
      }

      if (formContainer && formContainer.classList.contains('active')) {
        await gsap.to(formContainer, {
          opacity: 0,
          duration: 0.3,
          ease: 'power2.in',
          onComplete: () => {
            formContainer.classList.remove('active');
            gsap.set(formContainer, { visibility: 'hidden' });
          }
        });
      }

      if (menuHamburger && dropMenu && dropMenu.classList.contains('active')) {
        await gsap.to(dropMenu, {
          opacity: 0,
          y: '-100%',
          duration: 0.3,
          ease: 'power2.in',
          onComplete: () => {
            menuHamburger.classList.remove('active');
            dropMenu.classList.remove('active');
            gsap.set(dropMenu, { visibility: 'hidden' });
          }
        });
      }

      overlay.style.height = `${window.innerHeight}px`;

      // Копируем логотип в overlay и скрываем его изначально
      transitionLogo.innerHTML = logoContainer.innerHTML;
      gsap.set(transitionLogo, { opacity: 0 });

      // Анимация появления overlay
      if (window.innerWidth > 850) {
        await gsap.fromTo(overlay, 
          { x: '-200%' }, 
          { x: '150%', duration: 0.8, ease: 'power2.inOut' }
        );
      } else {
        await gsap.fromTo(overlay, 
          { x: '-100%' }, 
          { x: '125%', duration: 0.8, ease: 'power2.inOut' }
        );
      }

      // Плавное появление логотипа
      gsap.to(transitionLogo, { opacity: 1, duration: 0.5 });
    },
    async enter(data) {
      // Удаляем старый специфический CSS
      const allStyles = document.querySelectorAll('link[rel="stylesheet"]:not([href*="everywhere.css"]):not([href*="fonts.googleapis.com"])');
      allStyles.forEach(style => style.remove());

      // Удаляем старый main.js, если он есть
      const existingMainScript = document.querySelector('script[src="style/js/main.js"]');
      if (existingMainScript) {
        existingMainScript.remove();
      }

      // Определяем новый CSS-файл
      let cssFile;
      switch (data.next.namespace) {
        case 'home': cssFile = 'style/css/main.css'; break;
        case 'services': cssFile = 'style/css/services.css'; break;
        case 'about': cssFile = 'style/css/about_me.css'; break;
        case 'consultation': cssFile = 'style/css/consultation.css'; break;
        case 'policy': cssFile = 'style/css/conditioning_policy.css'; break;
        case 'registration': cssFile = 'style/css/registration-form-consultation.css'; break;
        default: cssFile = 'style/css/main.css';
      }

      // Добавляем новый CSS-файл
      const link = document.createElement('link');
      link.id = 'page-specific-styles';
      link.rel = 'stylesheet';
      link.href = cssFile;
      document.head.appendChild(link);

      // Ждём загрузки стилей
      await new Promise(resolve => {
        link.onload = resolve;
        link.onerror = resolve;
      });

      // Добавляем main.js только для главной страницы
      if (data.next.namespace === 'home') {
        const mainScript = document.createElement('script');
        mainScript.src = 'style/js/main.js';
        mainScript.id = 'main-script';
        document.body.appendChild(mainScript);

        // Ждём загрузки скрипта
        await new Promise(resolve => {
          mainScript.onload = resolve;
          mainScript.onerror = resolve;
        });
      }
    },
    async after(data) {
      const overlay = document.querySelector('.transition-overlay');
      const transitionLogo = document.querySelector('.transition-logo');

      if (!overlay) {
        console.error('Overlay не найден в after!');
        return;
      }

      // Минимальная задержка 1 секунда перед уходом overlay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Анимация ухода overlay в зависимости от ширины экрана
      if (window.innerWidth > 450) {
        console.log('Десктопная анимация ухода: x от 150% к -200%');
        await Promise.all([
          gsap.to(transitionLogo, { opacity: 0, duration: 0.5 }),
          gsap.to(overlay, {
            x: '-200%',
            duration: 0.8,
            ease: 'power2.inOut',
            delay: 0.5,
            onComplete: () => {
              transitionLogo.innerHTML = '';
            }
          })
        ]);
      } else {
        console.log('Мобильная анимация ухода: x от 125% к -100%');
        await Promise.all([
          gsap.to(transitionLogo, { opacity: 0, duration: 0.5 }),
          gsap.to(overlay, {
            x: '-100%',
            duration: 0.8,
            ease: 'power2.inOut',
            delay: 0.5,
            onComplete: () => {
              transitionLogo.innerHTML = '';
            }
          })
        ]);
      }
    },
    afterEnter(data) {
      // Повторная инициализация динамического контента
      initMenuHamburger();
      initCallUsForm();
      if (data.next.namespace === 'services') {
        initServicesAccordion();
      }
      if (data.next.namespace === 'registration') {
        initCalendar();
      }
    }
  }]
});

// Инициализация меню-гамбургера
function initMenuHamburger() {
  const menuHamburger = document.querySelector('.menu-hamburger');
  const dropMenu = document.querySelector('.drop-menu');
  const formContainer = document.querySelector('.container-form-call-us');

  if (menuHamburger && dropMenu) {
    menuHamburger.replaceWith(menuHamburger.cloneNode(true));
    const newMenuHamburger = document.querySelector('.menu-hamburger');

    newMenuHamburger.addEventListener('click', () => {
      const isActive = newMenuHamburger.classList.contains('active');

      if (isActive) {
        // Закрываем меню с анимацией
        gsap.to(dropMenu, {
          opacity: 0,
          y: '-100%',
          duration: 0.3,
          ease: 'power2.in',
          onComplete: () => {
            newMenuHamburger.classList.remove('active');
            dropMenu.classList.remove('active');
            gsap.set(dropMenu, { visibility: 'hidden' });
          }
        });
      } else {
        // Закрываем форму, если она открыта
        if (formContainer && formContainer.classList.contains('active')) {
          gsap.to(formContainer, {
            opacity: 0,
            duration: 0.3,
            ease: 'power2.in',
            onComplete: () => {
              formContainer.classList.remove('active');
              gsap.set(formContainer, { visibility: 'hidden' });
            }
          });
        }

        // Открываем меню с анимацией
        newMenuHamburger.classList.add('active');
        dropMenu.classList.add('active');
        gsap.fromTo(dropMenu, 
          { opacity: 0, y: '-100%', visibility: 'visible' },
          { opacity: 1, y: '0%', duration: 0.3, ease: 'power2.out' }
        );
      }
    });
  }
}

// Инициализация аккордеона для services.html
function initServicesAccordion() {
  const buttons = document.querySelectorAll('.button-service');
  buttons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const container = button.nextElementSibling;
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
      container.classList.toggle('hidden');
    });
  });
}

function initCallUsForm() {
  const callUsButtons = document.querySelectorAll('.button-call-us');
  const formContainer = document.querySelector('.container-form-call-us');
  const closeButton = document.querySelector('.close-form');
  const menuHamburger = document.querySelector('.menu-hamburger');
  const dropMenu = document.querySelector('.drop-menu');
  const telInput = document.querySelector('#users-tel');
  const form = document.querySelector('.form-call-us');
  const submitButton = document.querySelector('#enter-tel');

  if (callUsButtons.length > 0 && formContainer) {
    // Добавляем обработчик для каждой кнопки .button-call-us
    callUsButtons.forEach(button => {
      button.removeEventListener('click', openForm);
      button.addEventListener('click', openForm);
    });

    function openForm() {
      // Закрываем меню, если оно открыто
      if (menuHamburger && dropMenu && dropMenu.classList.contains('active')) {
        gsap.to(dropMenu, {
          opacity: 0,
          y: '-100%',
          duration: 0.3,
          ease: 'power2.in',
          onComplete: () => {
            menuHamburger.classList.remove('active');
            dropMenu.classList.remove('active');
            gsap.set(dropMenu, { visibility: 'hidden' });
          }
        });
      }

      formContainer.classList.add('active');
      gsap.fromTo(formContainer, 
        { opacity: 0, visibility: 'visible' },
        { opacity: 1, duration: 0.3, ease: 'power2.out' }
      );
      gsap.fromTo(formContainer.querySelector('.form-call-us'), 
        { scale: 0.8 },
        { scale: 1, duration: 0.3, ease: 'power2.out' }
      );
    }

    // Закрытие формы при клике на кнопку закрытия
    if (closeButton) {
      closeButton.removeEventListener('click', closeForm);
      closeButton.addEventListener('click', closeForm);
    }

    // Закрытие формы при клике на фон
    formContainer.removeEventListener('click', closeFormOnBackdrop);
    formContainer.addEventListener('click', closeFormOnBackdrop);

    function closeForm() {
      gsap.to(formContainer, {
        opacity: 0,
        duration: 0.3,
        ease: 'power2.in',
        onComplete: () => {
          formContainer.classList.remove('active');
          gsap.set(formContainer, { visibility: 'hidden' });
          if (telInput) {
            telInput.value = '';
            telInput.classList.remove('invalid');
          }
        }
      });
      gsap.to(formContainer.querySelector('.form-call-us'), {
        scale: 0.8,
        duration: 0.3,
        ease: 'power2.in'
      });
    }

    function closeFormOnBackdrop(event) {
      if (event.target === formContainer) {
        formContainer.classList.remove('active');
      }
    }

    // Форматирование номера телефона
    if (telInput) {
      telInput.addEventListener('input', () => {
        // Удаляем все нечисловые символы
        let value = telInput.value.replace(/\D/g, '');

        // Ограничиваем длину до 9 цифр (для украинского номера после +380)
        if (value.length > 9) {
          value = value.slice(0, 9);
        }

        // Форматируем отображаемое значение
        let formattedValue = '';
        if (value.length > 0) {
          formattedValue += value.slice(0, 2);
        }
        if (value.length > 2) {
          formattedValue += '-' + value.slice(2, 5);
        }
        if (value.length > 5) {
          formattedValue += '-' + value.slice(5, 7);
        }
        if (value.length > 7) {
          formattedValue += '-' + value.slice(7, 9);
        }

        // Устанавливаем отформатированное значение для отображения
        telInput.value = formattedValue;

        // Проверяем валидность (должно быть ровно 9 цифр)
        if (value.length === 9) {
          telInput.classList.remove('invalid');
        } else {
          telInput.classList.add('invalid');
        }
      });

      // При отправке формы убираем дефисы
      if (form && submitButton) {
        form.addEventListener('submit', (e) => {
          e.preventDefault(); // Предотвращаем отправку для тестирования

          const rawValue = telInput.value.replace(/\D/g, '');
          if (rawValue.length !== 9) {
            telInput.classList.add('invalid');
            alert('Будь ласка, введіть коректний номер телефону (9 цифр після +380).');
            return;
          }

          // Для отправки на сервер используем только цифры
          const phoneNumber = '+380' + rawValue;
          console.log('Отправляемый номер:', phoneNumber);

          // Здесь можно добавить реальную отправку формы, например:
          // form.submit();
        });
      }
    }
  }
}

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

// Управление хедером при скролле
const header = document.querySelector('header');
let lastScrollTop = 0;

window.addEventListener('scroll', () => {
  let currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  if (currentScrollTop <= 0) {
    header.classList.remove('scrolled');
  } else {
    header.classList.add('scrolled');
  }
  if (currentScrollTop > lastScrollTop) {
    header.classList.add('hidden');
  } else {
    header.classList.remove('hidden');
  }
  lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
});

// Инициализация при первой загрузке
initMenuHamburger();
initCallUsForm();