// static/theme.js
function toggleTheme(mode) {
  document.documentElement.setAttribute('data-theme', mode);
  localStorage.setItem('theme', mode);
}

window.onload = () => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  const selector = document.getElementById("theme-toggle");
  if (selector) selector.value = savedTheme;
}
