document.addEventListener('DOMContentLoaded', () => {
  initListReviews()
});

function initListReviews () {
    const listReviews = document.querySelector('.list-reviews');
    const buttonReviewLeft = document.querySelector('.button-review-left');
    const buttonReviewRight = document.querySelector('.button-review-right');
  
    // Сбрасываем позицию карусели
    if (listReviews) {
      listReviews.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
    }
  
    // Функции для прокрутки
    const scrollLeft = () => {
      listReviews.scrollBy({
        left: -375,
        behavior: 'smooth'
      });
    };
  
    const scrollRight = () => {
      listReviews.scrollBy({
        left: 375,
        behavior: 'smooth'
      });
    };
  
    // Удаляем старые обработчики, если они есть (на случай, если элементы остались в DOM)
    if (buttonReviewLeft) {
      buttonReviewLeft.removeEventListener('click', scrollLeft);
      buttonReviewLeft.addEventListener('click', scrollLeft);
    }
  
    if (buttonReviewRight) {
      buttonReviewRight.removeEventListener('click', scrollRight);
      buttonReviewRight.addEventListener('click', scrollRight);
    }
  
    const stars = document.querySelectorAll('.container-stars');
  
    if (stars.length > 0) {
      initStars();
    }
  
    function initStars() {
      let starsActive, starsValue;
      for (let index = 0; index < stars.length; index++) {
        const star = stars[index];
        initStar(star);
      }
  
      function initStar(star) {
        initStarsVars(star);
        setStarsActiveWigth();
      }
  
      function initStarsVars(star) {
        starsActive = star.querySelector('.stars-active');
        starsValue = star.querySelector('.stars-value');
        console.log(starsValue)
        console.log(typeof(starsValue))
      }
  
      function setStarsActiveWigth(index = starsValue.innerHTML) {
        const starsActiveWigth = parseFloat(index.replace(',', '.')) / 0.05;
        starsActive.style.width = `${starsActiveWigth}%`;
      }
    }
};