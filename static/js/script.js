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
  const container = document.getElementById('popup-container');
  let currentIndex = 0;

  function showPopup(index) {
    if (index >= popups.length) return;

    const popup = popups[index];
    container.classList.remove('pointer-events-none', 'opacity-0');
    popup.classList.remove('pointer-events-none', 'opacity-0', 'scale-95');
    popup.classList.add('opacity-100', 'scale-100');
    popup.focus();

    // Trap focus
    trapFocus(popup);

    // ESC close
    const escListener = (e) => {
      if (e.key === 'Escape') closePopup(index);
    };
    document.addEventListener('keydown', escListener);
    popup._escListener = escListener;

    // Outside click close
    container.addEventListener('click', function outsideClickHandler(e) {
      if (!popup.contains(e.target)) {
        closePopup(index);
        container.removeEventListener('click', outsideClickHandler);
      }
    });
  }

  window.closePopup = function(index) {
    const popup = popups[index];
    if (!popup) return;

    popup.classList.add('pointer-events-none', 'opacity-0', 'scale-95');
    popup.classList.remove('opacity-100', 'scale-100');

    if (popup._escListener) {
      document.removeEventListener('keydown', popup._escListener);
      delete popup._escListener;
    }

    currentIndex++;
    if (currentIndex < popups.length) {
      setTimeout(() => showPopup(currentIndex), 300);
    } else {
      container.classList.add('pointer-events-none', 'opacity-0');
    }
  };

  function trapFocus(element) {
    const focusable = element.querySelectorAll('a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])');
    const first = focusable[0], last = focusable[focusable.length - 1];
    element.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    });
  }

  if (popups.length > 0) showPopup(currentIndex);
});

  