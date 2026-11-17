const select = (selector) => document.querySelector(selector);
const selectAll = (selector) => [...document.querySelectorAll(selector)];

const theme = select(".theme");
function updateThemeLabel() {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  select('meta[name="theme-color"]').content = next === "light" ? "#0f1216" : "#ffffff";
  theme.setAttribute("aria-label", `Switch to ${next} theme`);
  theme.title = theme.getAttribute("aria-label");
}
theme.addEventListener("click", () => {
  const root = document.documentElement;
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  try {
    localStorage.setItem("docs-theme", root.dataset.theme);
  } catch {
    // The current page can still switch themes when storage is unavailable.
  }
  updateThemeLabel();
});
updateThemeLabel();

const sidebar = select(".sidebar");
const menu = select(".menu");
const narrow = matchMedia("(max-width: 800px)");
function setMenu(open, restoreFocus = false) {
  sidebar.classList.toggle("open", open);
  menu.setAttribute("aria-expanded", String(open));
  menu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  if (restoreFocus) menu.focus();
}
menu.addEventListener("click", () => {
  const open = !sidebar.classList.contains("open");
  setMenu(open);
  if (open) sidebar.querySelector("a").focus();
});
document.addEventListener("click", (event) => {
  if (!sidebar.classList.contains("open") || menu.contains(event.target)) return;
  if (event.target.closest("a") || !sidebar.contains(event.target)) setMenu(false);
});
document.addEventListener("focusin", (event) => {
  if (!sidebar.contains(event.target) && event.target !== menu) setMenu(false);
});
narrow.addEventListener("change", () => setMenu(false));

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const field = document.createElement("textarea");
    const previous = document.activeElement;
    field.value = text;
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.append(field);
    field.select();
    const copied = document.execCommand("copy");
    field.remove();
    previous?.focus({ preventScroll: true });
    if (!copied) throw new Error("Clipboard unavailable");
  }
}
selectAll(".copy").forEach((button) => {
  let timer;
  const label = button.querySelector("span");
  label.setAttribute("aria-live", "polite");
  button.addEventListener("click", async () => {
    clearTimeout(timer);
    try {
      await copyText(button.closest(".code-block").querySelector("pre code").textContent);
      label.textContent = "Copied";
    } catch {
      label.textContent = "Select code to copy";
    }
    timer = setTimeout(() => { label.textContent = "Copy"; }, 2000);
  });
});

const tabs = select(".os-tabs");
if (tabs) {
  const panels = selectAll(".os-panel");
  tabs.setAttribute("role", "tablist");
  function activate(index, updateUrl = false) {
    panels.forEach((panel, i) => {
      panel.hidden = index !== i;
      tabs.children[i].tabIndex = index === i ? 0 : -1;
      tabs.children[i].setAttribute("aria-selected", String(index === i));
    });
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set("os", panels[index].id.slice(3));
      history.replaceState(history.state, "", url);
    }
  }
  panels.forEach((panel, i) => {
    const tab = document.createElement("button");
    tab.type = "button";
    tab.id = `tab-${panel.id}`;
    tab.textContent = panel.querySelector("h3").textContent;
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", panel.id);
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
    tab.addEventListener("click", () => activate(i, true));
    tab.addEventListener("keydown", (event) => {
      const next = { ArrowLeft: (i + panels.length - 1) % panels.length, ArrowRight: (i + 1) % panels.length, Home: 0, End: panels.length - 1 }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      activate(next, true);
      tabs.children[next].focus();
    });
    tabs.append(tab);
  });
  const os = new URLSearchParams(location.search).get("os");
  activate(Math.max(0, panels.findIndex((panel) => panel.id === `os-${os}`)));
}

function followFragment() {
  const target = document.getElementById(location.hash.slice(1));
  if (target?.matches("details")) {
    target.open = true;
    target.scrollIntoView({ block: "start" });
  }
  const page = location.pathname.split("/").pop() || "index.html";
  const links = selectAll(".sidebar nav a");
  const current = links.find((link) => link.getAttribute("href") === page + location.hash)
    || links.find((link) => link.getAttribute("href") === page)
    || (page === "guide.html" && !location.hash ? links.find((link) => link.hash === "#pipeline") : null);
  links.forEach((link) => link.removeAttribute("aria-current"));
  if (current) current.setAttribute("aria-current", current.hash ? "location" : "page");
  const section = target?.closest(".doc-section");
  for (const link of selectAll(".page-outline a")) {
    if (section && link.hash === `#${section.id}`) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}
window.addEventListener("hashchange", followFragment);
followFragment();

const dialog = select(".search-dialog");
const input = dialog.querySelector("input");
const results = dialog.querySelector(".results");
const status = dialog.querySelector(".search-status");
function renderResults() {
  const query = input.value.trim().toLowerCase();
  const terms = query.split(/\s+/);
  const matches = documentationIndex.filter(([name, , category, description]) => {
    if (!query) return true;
    const haystack = [name, category, description].join(" ").toLowerCase().replaceAll("_", " ");
    return terms.every((term) => haystack.includes(term.replaceAll("_", " ")));
  });
  if (query) matches.sort((a, b) => Number(b[0].toLowerCase().includes(query)) - Number(a[0].toLowerCase().includes(query)));
  const visible = query ? matches : matches.slice(0, 8);
  status.textContent = query ? (matches.length ? `${matches.length} result${matches.length === 1 ? "" : "s"}` : "No results. Try a function name or a different term.") : "Documentation";
  results.replaceChildren();
  visible.forEach(([name, href, category]) => {
    const link = document.createElement("a");
    link.href = href;
    const group = document.createElement("small");
    group.textContent = category;
    link.append(group, document.createTextNode(name));
    link.addEventListener("click", () => {
      dialog.close();
      if (link.pathname === location.pathname && link.hash === location.hash) followFragment();
    });
    results.append(link);
  });
}
function openSearch() {
  setMenu(false);
  if (!dialog.open) dialog.showModal();
  input.value = "";
  renderResults();
  input.focus();
}
const openButton = select(".search-open");
if (/Mac|iPhone|iPad/.test(navigator.platform)) openButton.querySelector("kbd").textContent = "⌘ K";
openButton.addEventListener("click", openSearch);
select(".close-search").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target !== dialog) return;
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});
input.addEventListener("input", renderResults);
input.addEventListener("keydown", (event) => {
  if (event.key === "ArrowDown") {
    event.preventDefault();
    results.querySelector("a")?.focus();
  }
  if (event.key === "Enter" && !event.isComposing) results.querySelector("a")?.click();
});
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    openSearch();
  }
  if (event.key === "Escape" && sidebar.classList.contains("open")) setMenu(false, true);
});
