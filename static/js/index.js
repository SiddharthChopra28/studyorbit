document.addEventListener('DOMContentLoaded', () => {
  // Apply the saved theme on page load
  const savedTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(savedTheme);
});

function applyTheme(theme) {
  const stylesheet = document.getElementById('stylesheet');
  const buttonImg = document.querySelector('.themeImg');

  if (theme === 'dark') {
    stylesheet.setAttribute('href', "{{ url_for('static', filename='css/dark.css') }}");
    buttonImg.setAttribute('src', 'http://simpleicon.com/wp-content/uploads/light.svg');
  } else {
    stylesheet.setAttribute('href', "{{ url_for('static', filename='css/light.css') }}");
    buttonImg.setAttribute('src', 'https://cdn.iconscout.com/icon/free/png-256/night-mode-2-475098.png');
  }

  localStorage.setItem('theme', theme);
}

function toggleTheme() {
  const currentTheme = localStorage.getItem('theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(newTheme);
}
