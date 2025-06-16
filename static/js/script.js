document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper (Assuming Swiper.js is loaded and functional)
    const swiper = new Swiper('.swiper', {
        direction: 'horizontal',
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        scrollbar: {
            el: '.swiper-scrollbar',
            draggable: true,
        },
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true,
        },
    });

    const popups = document.querySelectorAll('#popup-container > div');
  let currentIndex = 0;

  function showPopup(index) {
    if (index >= popups.length) return;

    const popup = popups[index];
    popup.parentElement.classList.remove('pointer-events-none', 'opacity-0');
    popup.classList.remove('pointer-events-none', 'opacity-0');
    popup.classList.add('opacity-100');  

    popup.focus();

    trapFocus(popup);

    function escListener(e) {
      if (e.key === 'Escape' || e.key === 'Esc') {
        closePopup(index);
      }
    }
    document.addEventListener('keydown', escListener);
    popup._escListener = escListener;
  }

  window.closePopup = function(index) {
    const popup = popups[index];
    if (!popup) return;

    popup.classList.add('pointer-events-none', 'opacity-0');
    popup.classList.remove('opacity-100'); 

    // Hide overlay if last popup
    if (index === popups.length -1) {
      popup.parentElement.classList.add('pointer-events-none', 'opacity-0');
    }

    if (popup._escListener) {
      document.removeEventListener('keydown', popup._escListener);
      delete popup._escListener;
    }

    currentIndex++;
    if (currentIndex < popups.length) {
      setTimeout(() => showPopup(currentIndex), 350);
    }
  }

  function trapFocus(element) {
    const focusableSelectors = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';
    const focusableEls = element.querySelectorAll(focusableSelectors);
    if (!focusableEls.length) return;

    const firstFocusable = focusableEls[0];
    const lastFocusable = focusableEls[focusableEls.length - 1];

    element.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      }
    });
  }

  if (popups.length > 0) {
    showPopup(currentIndex);
  }
});