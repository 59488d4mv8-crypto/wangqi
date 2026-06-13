(function () {
  "use strict";

  function setCurrentYear() {
    var els = document.querySelectorAll("[data-current-year]");
    var year = new Date().getFullYear();
    for (var i = 0; i < els.length; i += 1) {
      els[i].textContent = String(year);
    }
  }

  function highlightActiveNav() {
    var path = window.location.pathname.replace(/\/+$/, "") || "/";
    var fileName = path.substring(path.lastIndexOf("/") + 1) || "index.html";
    if (!/\.html$/.test(fileName)) {
      fileName = "index.html";
    }

    var menu = document.querySelector(".site-nav .menu");
    if (!menu) return;

    var links = menu.querySelectorAll("a[data-nav]");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var href = link.getAttribute("href") || "";
      var clean = href.replace(/^.*?([^/]+\.html)(#.*)?$/, "$1");
      if (!clean) continue;

      if (clean === fileName) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    }
  }

  function ensureToastContainer() {
    var container = document.querySelector(".toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      document.body.appendChild(container);
    }
    return container;
  }

  function showToast(msg, level) {
    if (!msg) return;
    var levelValue = level || "info";
    var container = ensureToastContainer();
    var toast = document.createElement("div");
    toast.className = "toast " + levelValue;
    toast.textContent = String(msg);
    container.appendChild(toast);

    window.requestAnimationFrame(function () {
      toast.classList.add("show");
    });

    window.setTimeout(function () {
      toast.classList.remove("show");
      window.setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 2800);
  }

  window.showToast = showToast;

  window.addEventListener("learn:badgeUnlocked", function (ev) {
    if (!showToast) return;
    var detail = (ev && ev.detail) || {};
    var title = detail.title || "新徽章";
    var points = detail.points ? "（+" + detail.points + " 分）" : "";
    showToast("🎉 获得徽章：" + title + points, "success");
  });

  document.addEventListener("DOMContentLoaded", function () {
    setCurrentYear();
    highlightActiveNav();
  });
})();
