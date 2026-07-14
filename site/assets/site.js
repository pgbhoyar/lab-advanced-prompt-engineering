// Advanced Prompt Engineering Workshop — shared site behavior.
// 1) Theme toggle (persisted). 2) Language tabs across Python / C# / Java (persisted).
(function () {
  var toggle = document.getElementById('themeToggle');
  var html = document.documentElement;
  var stored = localStorage.getItem('theme');
  if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    html.setAttribute('data-theme', 'dark');
    if (toggle) toggle.textContent = '🎨';
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var isDark = html.getAttribute('data-theme') === 'dark';
      html.setAttribute('data-theme', isDark ? 'light' : 'dark');
      toggle.textContent = isDark ? '🌙' : '🎨';
      localStorage.setItem('theme', isDark ? 'light' : 'dark');
    });
  }
})();

(function () {
  var KEY = 'workshopLang';
  var LANGS = ['python', 'csharp', 'java'];
  function setLang(lang) {
    if (LANGS.indexOf(lang) === -1) lang = 'python';
    document.querySelectorAll('.code-tabs').forEach(function (group) {
      group.querySelectorAll('.code-tab-btn').forEach(function (btn) {
        var active = btn.getAttribute('data-lang') === lang;
        btn.setAttribute('aria-selected', active ? 'true' : 'false');
        btn.tabIndex = active ? 0 : -1;
      });
      group.querySelectorAll('.code-tab-panel').forEach(function (panel) {
        panel.hidden = panel.getAttribute('data-lang') !== lang;
      });
    });
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }
  document.querySelectorAll('.code-tab-btn').forEach(function (btn) {
    btn.addEventListener('click', function () { setLang(btn.getAttribute('data-lang')); });
  });
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  setLang(stored || 'python');
})();
