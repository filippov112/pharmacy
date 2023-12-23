// Получаем все заголовки и ссылки
const headers = document.querySelectorAll('#menu-title h2');
const links = document.querySelectorAll('#menu-block a');

// Функция для отображения соответствующего заголовка при наведении на ссылку
function showHeader(event) {
    if (event.target.tagName.toLowerCase() === 'a' && !event.target.classList.contains('disable')) {
        // Получаем порядковый номер ссылки, на которую наведен курсор
        const index = Array.from(links).indexOf(event.target);
        // Скрываем все заголовки
        headers.forEach(header => header.style.display = 'none');
        // Отображаем соответствующий заголовок
        headers[index].style.display = 'block';
    }
}

// Привязываем функцию к событию наведения курсора на ссылку
links.forEach(link => {
  link.addEventListener('mouseover', showHeader);
});