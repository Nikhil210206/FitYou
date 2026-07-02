/* FitYou — theme toggle + mobile nav. Single source of truth for all pages. */
(function () {
  "use strict";

  var STORAGE_KEY = "fityou-theme";

  function getStoredTheme() {
    return localStorage.getItem(STORAGE_KEY);
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  // Apply as early as possible (default: dark).
  applyTheme(getStoredTheme() || "dark");

  document.addEventListener("DOMContentLoaded", function () {
    // Theme toggle (any element with [data-theme-toggle] or #theme-toggle)
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-theme-toggle], #theme-toggle")) {
        e.preventDefault();
        var current = document.documentElement.getAttribute("data-theme");
        applyTheme(current === "dark" ? "light" : "dark");
      }
      // Mobile nav toggle
      if (e.target.closest("[data-nav-toggle], #nav-toggle")) {
        var links = document.getElementById("nav-links");
        if (links) links.classList.toggle("open");
      }
    });

    // Close mobile menu after clicking a link
    var links = document.getElementById("nav-links");
    if (links) {
      links.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () { links.classList.remove("open"); });
      });
    }
  });
})();
