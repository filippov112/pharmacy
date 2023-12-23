// Кнопка отмены удаления
document.getElementById('cancel-delete').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById("page-overlay").classList.remove("active");
    document.getElementById("modal-delete").classList.remove("active");
});



let valuesArray = []; // Список записей таблицы к удалению


// Функция работы со списком записей к удалению
function handlerValuesArray(elem) {
    let value = elem.value;
    if (elem.checked) {
        if (!valuesArray.includes(value)) {
            valuesArray.push(value);
        }
    } else {
        let index = valuesArray.indexOf(value);
        if (index > -1) {
            valuesArray.splice(index, 1);
        }
    }
    if (valuesArray.length > 0)
        deleteButton.classList.add('active');
    else
        deleteButton.classList.remove('active');
}

// Локальные чекбоксы
document.querySelectorAll('tbody .delete-record').forEach(function (checkbox) {
    checkbox.addEventListener('change', function() {
        handlerValuesArray(this);
        let table = this.parentElement.parentElement.parentElement.parentElement;
        const count_rec_false =  Array.from(table.querySelectorAll('tbody .delete-record:not(:checked)')).length;
        table.querySelector('thead .delete-record').checked = count_rec_false === 0;
    } );
});
// Обработка клика по ячейке чекбокса
document.querySelectorAll('.delete-col').forEach(el => el.addEventListener('mousedown', function(e) {
    if (e.target.tagName.toLowerCase() !== 'input') {
        let chb = e.target.querySelector('.delete-record');
        chb.click();
    } 
}));


// Общий чекбокс
document.querySelectorAll('thead .delete-record').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        let tbody = this.parentElement.parentElement.parentElement.nextElementSibling;
        tbody.querySelectorAll('.delete-record').forEach( checkB =>  {
            checkB.checked = this.checked
            handlerValuesArray(checkB, 0);
        });
    });
});



// Кнопка удаления записей из таблицы
let deleteButton = document.getElementById("delete-elements");

deleteButton.addEventListener('click', function() {
    if (valuesArray.length > 0) {
      document.getElementById('delete-list').value = valuesArray.join(', ');
      const mes = `Вы подтверждаете удаление ${valuesArray.length} записи(-ей)?`;
      document.getElementById("delete-messedge").textContent = mes;
      document.getElementById("modal-delete").classList.add("active");
      document.getElementById("page-overlay").classList.add("active");
    }  
});