// Кнопка открытия сайдбара
document.getElementById("show-sidebar").addEventListener('click', function() {
    document.getElementById("sidebar").classList.add("active");
    document.getElementById("page-overlay").classList.add("active");
});