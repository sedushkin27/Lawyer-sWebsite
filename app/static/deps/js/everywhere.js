document.addEventListener('DOMContentLoaded', () => {
  initScrollHeder();
  initMenuHamburger();
  initCallUsForm();
  initServicesAccordion();
});

function initScrollHeder() {
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
}

function initMenuHamburger() {
  const menuHamburger = document.querySelector('.menu-hamburger');
  const dropMenu = document.querySelector('.drop-menu');
  const formContainer = document.querySelector('.container-form-call-us');

  if (!menuHamburger || !dropMenu) return;

  const newMenuHamburger = menuHamburger.cloneNode(true);
  menuHamburger.replaceWith(newMenuHamburger);

  function resetMenuState() {
    if (window.innerWidth > 1306) {
      newMenuHamburger.classList.remove('active');
      dropMenu.classList.remove('active');
      gsap.set(dropMenu, {
        visibility: 'visible',
        opacity: 1,
        y: '0%',
        clearProps: 'all' 
      });
    } else {
      if (!dropMenu.classList.contains('active')) {
        gsap.set(dropMenu, { visibility: 'hidden', opacity: 0, y: '-100%' });
      }
    }
  }

  newMenuHamburger.addEventListener('click', () => {
    const isActive = newMenuHamburger.classList.contains('active');

    if (isActive) {
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
      if (formContainer?.classList.contains('active')) {
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

      newMenuHamburger.classList.add('active');
      dropMenu.classList.add('active');
      gsap.fromTo(dropMenu, 
        { opacity: 0, y: '-100%', visibility: 'visible' },
        { opacity: 1, y: '0%', duration: 0.3, ease: 'power2.out' }
      );
    }
  });

  resetMenuState();

  window.addEventListener('resize', resetMenuState);
}

function initServicesAccordion() {
  const buttons = document.querySelectorAll('.button-service');
  buttons.forEach(button => {
    button.removeEventListener('click', toggleAccordion);
    button.addEventListener('click', toggleAccordion);
  });

  function toggleAccordion(e) {
    e.preventDefault();
    const button = e.currentTarget;
    const container = button.nextElementSibling;
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', !isExpanded);
    container.classList.toggle('hidden');
  }
}

function initCallUsForm() {
  const callUsButtons = document.querySelectorAll('.button-call-us');
  const formContainer = document.querySelector('.container-form-call-us');
  const closeButton = document.querySelector('.close-form');
  const menuHamburger = document.querySelector('.menu-hamburger');
  const dropMenu = document.querySelector('.drop-menu');
  const telInput = document.querySelector('#phone');
  const form = document.querySelector('.form-call-us');

  if (!callUsButtons.length || !formContainer) return;

  callUsButtons.forEach(button => {
    button.removeEventListener('click', openForm);
    button.addEventListener('click', openForm);
  });

  function openForm() {
    if (menuHamburger?.classList.contains('active') && dropMenu?.classList.contains('active')) {
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

  if (closeButton) {
    closeButton.removeEventListener('click', closeForm);
    closeButton.addEventListener('click', closeForm);
  }

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
      closeForm();
    }
  }

  if (telInput && form) {
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

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const rawValue = telInput.value.replace(/\D/g, '');
      if (rawValue.length !== 9) {
        telInput.classList.add('invalid');
        alert('Будь ласка, введіть коректний номер телефону (9 цифр після +380).');
        return;
      }
      telInput.value = telInput.value.replace(/\D/g, '');
      telInput.classList.remove('invalid');

      form.submit();
      closeForm();
    });
  }
}