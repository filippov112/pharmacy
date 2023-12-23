// Кнопка удаления записей из таблицы
let deleteButton = document.getElementById("delete-record");

deleteButton.addEventListener('click', function() {
    const mes = `Вы подтверждаете удаление записи?`;
    document.getElementById("delete-messedge").textContent = mes;
    document.getElementById("modal-delete").classList.add("active");
    document.getElementById("page-overlay").classList.add("active");
});

// Кнопка отмены удаления
document.getElementById('cancel-delete').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById("page-overlay").classList.remove("active");
    document.getElementById("modal-delete").classList.remove("active");
});