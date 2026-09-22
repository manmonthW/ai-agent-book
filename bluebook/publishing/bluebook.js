document.addEventListener("DOMContentLoaded", () => {
  const cards = [...document.querySelectorAll(".experiment-card")];
  const groups = [...document.querySelectorAll(".experiment-group")];
  const buttons = [...document.querySelectorAll(".experiment-filters button")];
  const input = document.querySelector("#experiment-search");
  const count = document.querySelector("#experiment-count");
  if (!cards.length) return;
  let activeFilter = "all";

  const apply = () => {
    const query = (input?.value || "").trim().toLocaleLowerCase("zh-CN");
    let visible = 0;
    cards.forEach((card) => {
      const haystack = (card.dataset.search || card.textContent).toLocaleLowerCase("zh-CN");
      const matchesFilter = activeFilter === "all" || haystack.includes(activeFilter.toLocaleLowerCase("zh-CN"));
      const matchesQuery = !query || haystack.includes(query);
      const show = matchesFilter && matchesQuery;
      card.dataset.hidden = String(!show);
      if (show) visible += 1;
    });
    groups.forEach((group) => {
      group.dataset.hidden = String(!group.querySelector('.experiment-card[data-hidden="false"]'));
    });
    if (count) count.textContent = `${visible}项`;
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter || "all";
      buttons.forEach((item) => item.classList.toggle("active", item === button));
      apply();
    });
  });
  input?.addEventListener("input", apply);
  apply();
});
