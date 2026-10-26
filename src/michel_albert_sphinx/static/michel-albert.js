// Michel Albert design system: make preformatted blocks that overflow horizontally reachable by keyboard.
// sphinx-immaterial already does this for code blocks; this covers any other <pre>.
(function () {
  function mark() {
    document.querySelectorAll("pre, pre > code").forEach(function (el) {
      var scrolls = el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX !== "visible";
      if (scrolls && !el.hasAttribute("tabindex")) {
        el.setAttribute("tabindex", "0");
        el.setAttribute("data-ma-scroll", "");
        if (!el.hasAttribute("aria-label")) el.setAttribute("aria-label", "Code, scrolls horizontally");
      } else if (!scrolls && el.hasAttribute("data-ma-scroll")) {
        el.removeAttribute("tabindex"); el.removeAttribute("data-ma-scroll"); el.removeAttribute("aria-label");
      }
    });
  }
  var t; function later() { clearTimeout(t); t = setTimeout(mark, 150); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mark); else mark();
  window.addEventListener("load", mark); window.addEventListener("resize", later);
})();
