/**
 * !
 * Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2023 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 *
 * @format
 */
document.addEventListener("DOMContentLoaded", function () {
  var navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      // Remove 'active' class from all links
      navLinks.forEach(function (nav) {
        nav.classList.remove("active");
      });
      // Add 'active' class to the clicked link
      this.classList.add("active");
    });
  });
});

// This file is intentionally blank
// Use this file to add JavaScript to your project
