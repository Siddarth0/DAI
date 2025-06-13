// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper
    const swiper = new Swiper('.swiper', {
        // Optional parameters
        direction: 'horizontal',
        loop: true,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true, // Make pagination dots clickable
        },

        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

        // And if we need scrollbar
        scrollbar: {
            el: '.swiper-scrollbar',
            draggable: true,
        },

        // Autoplay (optional)
        autoplay: {
            delay: 5000, // 5 seconds
            disableOnInteraction: false, // Continue autoplay after user interaction
        },

        effect: 'fade', // Optional: Add a fade effect between slides
                fadeEffect: {
                    crossFade: true,
                },

        // Add any other Swiper options here
    });
});