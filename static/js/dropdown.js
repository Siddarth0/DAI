document.addEventListener("DOMContentLoaded", function () {
  function handleDropdown(menuItem) {
    let timeout;
    const dropdown = menuItem.querySelector(":scope > ul");

    if (!dropdown) return;

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
      }, 300);
    });

    dropdown.addEventListener("mouseenter", function () {
      clearTimeout(timeout);
    });

    dropdown.addEventListener("mouseleave", function () {
      timeout = setTimeout(function () {
        dropdown.classList.add("hidden");
        dropdown.classList.remove("block");
      }, 300);
    });

    // Recurse for children
    dropdown.querySelectorAll(":scope > li.relative.group").forEach(handleDropdown);
  }

  document.querySelectorAll("nav ul li.relative.group").forEach(handleDropdown);
});
