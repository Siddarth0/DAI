document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("nav ul li.relative.group").forEach(function(menuItem) {
    let timeout;
    const dropdown = menuItem.querySelector("ul");

    if (!dropdown) return;

    // Initially hide dropdown, remove group-hover block from CSS to avoid conflict
    dropdown.classList.add("hidden");
    dropdown.classList.remove("block");

    menuItem.addEventListener("mouseenter", function () {
      clearTimeout(timeout);
      dropdown.classList.remove("hidden");
      dropdown.classList.add("block");
    });

    menuItem.addEventListener("mouseleave", function () {
      timeout = setTimeout(function () {
        dropdown.classList.add("hidden");
        dropdown.classList.remove("block");
      }, 300); // 300ms delay before hiding dropdown
    });

    // Also keep dropdown visible if mouse enters submenu itself
    dropdown.addEventListener("mouseenter", function () {
      clearTimeout(timeout);
      dropdown.classList.remove("hidden");
      dropdown.classList.add("block");
    });

    dropdown.addEventListener("mouseleave", function () {
      timeout = setTimeout(function () {
        dropdown.classList.add("hidden");
        dropdown.classList.remove("block");
      }, 300);
    });
  });
});