
// Восстановление текущего состояния вкл/выкл фильтра
function setFilterSize() {
    let myVariable = localStorage.getItem("filtersize");
    
    if (myVariable !== null) {
        document.documentElement.style.setProperty('--filter-size', myVariable + "px");
    }
}

setFilterSize();
let filter = document.getElementById("filter-pane");
let filterButton = document.getElementById("filter-b");


// Кнопка вызова фильтра
filterButton.addEventListener('click', function() {
    let myVariable = localStorage.getItem("filtersize");
    if (!myVariable) {
        // Если значение отсутствует, берем значение из CSS-переменной
        myVariable = getComputedStyle(document.documentElement).getPropertyValue('--filter-size');
        console.log(myVariable);
    }

    myVariable = parseInt(myVariable) === 0 ? 450 : 0;
    if (myVariable === 0) {
        filter.style.display = "none";
    } else {
        filter.style.display = "block";
    }
    
    localStorage.setItem("filtersize", myVariable);
    setFilterSize();
});


// Кнопка сброса фильтров
document.getElementById("drop-filters").addEventListener('click', function(e) {
    e.preventDefault();
    const form = document.getElementById("filter-table"); // Замените "myForm" на ID своей формы

    // Получаем все элементы формы, включая все типы полей ввода
    const formElements = form.querySelectorAll("input, select, textarea");

    formElements.forEach(element => {
        const elementType = element.type.toLowerCase();

        // Сбрасываем значение в зависимости от типа элемента
        switch (elementType) {
        case "text":
        case "number":
        case "date":
        case "checkbox":
            element.value = "";
            break;
        case "select-one":
        case "select-multiple":
            element.selectedIndex = -1;
            break;
        case "radio":
            element.checked = false;
            break;
        default:
            break;
        }
    });
})