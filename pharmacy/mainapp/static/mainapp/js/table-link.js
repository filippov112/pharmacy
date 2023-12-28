// Ищем все не-чекбокс-ячейки у таблиц с пометкой "linked" и инициируем переход по ссылке в поле "link" при нажатии на запись в такой таблице.

let linked_row = document.querySelectorAll('table tr[link] td:not(.delete-col)');

for(i = 0; i < linked_row.length; i++) {
    linked_row[i].addEventListener('click', function() {
        let link = this.parentElement.getAttribute('link');
        window.location.href = link;
    });
}