document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".publications");
  const buttons = document.querySelectorAll("[data-pub-sort]");
  if (!container || buttons.length === 0) return;

  const originalHTML = container.innerHTML;

  const getRow = (li) => li.querySelector(".row");

  const sorters = {
    alphabetical: (a, b) => (getRow(a)?.dataset.title || "").localeCompare(getRow(b)?.dataset.title || ""),
    "author-position": (a, b) => parseInt(getRow(a)?.dataset.authorPosition || "999", 10) - parseInt(getRow(b)?.dataset.authorPosition || "999", 10),
  };

  const flattenAndSort = (compareFn) => {
    const entries = Array.from(container.querySelectorAll("ol.bibliography > li"));
    entries.sort(compareFn);

    const firstOl = container.querySelector("ol.bibliography");
    if (!firstOl) return;

    container.querySelectorAll("h2.bibliography").forEach((el) => el.remove());
    container.querySelectorAll("ol.bibliography").forEach((ol, idx) => {
      if (idx > 0) ol.remove();
    });

    entries.forEach((li) => firstOl.appendChild(li));
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("btn-primary", "active"));
      buttons.forEach((b) => b.classList.add("btn-outline-primary"));
      button.classList.remove("btn-outline-primary");
      button.classList.add("btn-primary", "active");

      const mode = button.dataset.pubSort;
      if (mode === "year") {
        container.innerHTML = originalHTML;
      } else {
        flattenAndSort(sorters[mode]);
      }
    });
  });
});
