document.addEventListener('DOMContentLoaded', function () {
    // Initialize Swiper
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

    const container = document.getElementById("popup-container");
    const templates = document.querySelectorAll(".popup-notice");
    let currentIndex = 0;

    function showPopup(index) {
        if (index >= templates.length) return;

        const data = templates[index].dataset;

        // Create popup box
        const popup = document.createElement("div");
        popup.className = "relative bg-white rounded-xl shadow-2xl transform transition-all duration-300 scale-95 opacity-100 max-h-[90vh] w-full overflow-auto mx-4 " +
            (data.pdf ? "max-w-5xl" : "max-w-xl");

        popup.innerHTML = `
            <button onclick="closePopup()" class="absolute top-4 right-4 bg-gray-100 hover:bg-red-400 text-gray-700 hover:text-white p-2 rounded-full shadow transition duration-200" aria-label="Close popup">
                <img src="/static/images/icons/close.svg" alt="Close" class="h-5 w-5">
            </button>
            <div class="p-6">
                <h3 class="text-2xl font-bold mb-4 text-gray-800">${data.title}</h3>
                <div class="mb-4 text-gray-700 whitespace-pre-wrap">${data.content}</div>
                ${data.image ? `<img src="${data.image}" class="mb-4 max-h-96 w-auto mx-auto object-contain rounded border border-gray-300">` : ""}
                ${data.pdf ? `<iframe src="${data.pdf}" width="100%" height="600" class="mb-4 rounded border border-gray-300"></iframe>` : ""}
                ${data.url ? `<a href="${data.url}" target="_blank" rel="noopener noreferrer" class="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Go to Post</a>` : ""}
            </div>
        `;

        // Display popup
        container.innerHTML = "";
        container.appendChild(popup);
        container.style.display = "flex";
        requestAnimationFrame(() => {
            container.classList.remove("opacity-0", "pointer-events-none");
        });

        // Add Escape key listener
        const escListener = (e) => {
            if (e.key === "Escape") {
                closePopup();
                document.removeEventListener("keydown", escListener);
            }
        };
        document.addEventListener("keydown", escListener);
    }

    window.closePopup = function () {
        container.classList.add("opacity-0", "pointer-events-none");
        setTimeout(() => {
            container.style.display = "none";
            container.innerHTML = "";
            currentIndex++;
            showPopup(currentIndex);
        }, 300);
    };

    // Close when clicking outside the popup box
    container.addEventListener("click", (e) => {
        if (e.target === container) {
            closePopup();
        }
    });

    // Start first popup if available
    if (templates.length > 0) {
        showPopup(currentIndex);
    }
});

//news hover scroll
let scrollInterval;

  function startScroll(direction) {
    const wrapper = document.getElementById('services-wrapper');
    scrollInterval = setInterval(() => {
      wrapper.scrollLeft += direction === 'right' ? 10 : -10;
    }, 15);
  }

  function stopScroll() {
    clearInterval(scrollInterval);
  }