let PO = document.getElementById("page-overlay");
let active_button = null;

// Обработчик нажатия на линк
function refrashHandlerLinks() {
    let links = document.querySelectorAll("button[select]");
    for (let l = 0; l < links.length; l++) {
        links[l].addEventListener("click", function(e) {
            e.preventDefault();
            let vib = document.querySelector('.table-wrap[select-name="'+this.getAttribute("select-name")+'"]');
            let multi = this.getAttribute("multi");
            if (multi === null) {
                vib.setAttribute("not-multi", true);
            }

            let inp_val = this.querySelector('input').value

            MSArray = inp_val !== '' ? inp_val.split(',') : [];
            vib.querySelectorAll('.multi-select-record').forEach( msr => {
                let this_r = msr.parentElement.parentElement.parentElement.getAttribute('record');
                msr.checked = MSArray.indexOf(this_r) > -1
            });

            let all_rec = vib.querySelectorAll('tbody .select-record')
            all_rec.forEach( el => {
                let this_r = el.parentElement.getAttribute('record');
                if (MSArray.indexOf(this_r) > -1) {
                    MSNArray.push(el.innerHTML);
                }
            });

            vib.querySelector('th .multi-select-record').checked = (all_rec.length === MSArray.length && MSArray.length > 0)
            active_button = this;
            PO.classList.add("active");
            vib.classList.add("active");
        });
    }
}
refrashHandlerLinks();


let selects = document.querySelectorAll(".table-wrap[select] td:not(.delete-col)");
// Обработчик нажатия на запись выборки
for (let v = 0; v < selects.length; v++) {
    selects[v].addEventListener('click', (e)=>{
        if (e.target.tagName === "TD") {
            const record = e.target.parentElement.getAttribute('record');
            const text = e.target.innerHTML;
            active_button.children[0].value = record;
            active_button.children[1].innerHTML = text;

                    // td ->     tr ->        tbody ->      table ->     table-wrap
            let t = e.target.parentElement.parentElement.parentElement.parentElement;
            closeSelectWindow(t);
        }
    });
}



// Поиск записей по ходу ввода текста в поле
let searches = document.querySelectorAll(".table-wrap[select] .select-search");
for( let i = 0; i < searches.length; i++) {
    searches[i].addEventListener('keyup', (e)=>{
        let v = e.target.parentElement.parentElement;
        let tds = v.getElementsByClassName("select-record");
        for (let j = 0; j < tds.length; j++) {
            if (!tds[j].innerHTML.match(e.target.value)) {
                tds[j].parentElement.style.display = "none";
            } else {
                tds[j].parentElement.style.display = "table-row";
            }
        }
    })
}

// Сброс поиска
function resetSearch(v) {
    let tds = v.getElementsByClassName("select-record");
    v.getElementsByClassName("select-search")[0].value = "";
    for (let j = 0; j < tds.length; j++) {
        tds[j].parentElement.style.display = "table-row";
    }
}



let MSArray = []; // Список записей таблицы
let MSNArray = []; // Список записей ИМЕН таблицы

// Функция работы со списком записей
function handlerMSArray(elem) {
    let value = elem.value;
    if (elem.checked) {
        if (!MSArray.includes(value)) {
            MSArray.push(value);
        }
    } else {
        let index = MSArray.indexOf(value);
        if (index > -1) {
            MSArray.splice(index, 1);
        }
    }
}
// Функция работы со списком ИМЕН записей
function handlerMSNArray(elem, name) {
    if (elem.checked) {
        if (!MSNArray.includes(name)) {
            MSNArray.push(name);
        }
    } else {
        let index = MSNArray.indexOf(name);
        if (index > -1) {
            MSNArray.splice(index, 1);
        }
    }
}

// Локальные чекбоксы
document.querySelectorAll('tbody .multi-select-record').forEach(function (checkbox) {
    checkbox.addEventListener('change', function() {
        let table = this.parentElement.parentElement.parentElement.parentElement.parentElement;
        let name = this.parentElement.parentElement.parentElement.querySelector('.select-record').innerHTML;
        handlerMSArray(this);
        handlerMSNArray(this, name);
        const count_rec_false =  Array.from(table.querySelectorAll('tbody .multi-select-record:not(:checked)')).length;
        table.querySelector('thead .multi-select-record').checked = count_rec_false === 0;
    } );
});
// Обработка клика по ячейке чекбокса
document.querySelectorAll('.delete-col').forEach(el => el.addEventListener('mousedown', function(e) {
    if (e.target.tagName.toLowerCase() !== 'input') {
        let chb = e.target.querySelector('.multi-select-record');
        chb.click();
    }
}));

// Общий чекбокс
document.querySelectorAll('thead .multi-select-record').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        let tbody = this.parentElement.parentElement.parentElement.parentElement.nextElementSibling;
        tbody.querySelectorAll('.multi-select-record').forEach( checkB =>  {
            checkB.checked = this.checked
            let name = checkB.parentElement.parentElement.parentElement.querySelector('.select-record').innerHTML;
            handlerMSArray(checkB);
            handlerMSNArray(checkB, name);
        });
    });
});

// Подтверждение выбора
document.querySelectorAll('.confirm-select').forEach( butt => {
    butt.addEventListener('click', (e) => {
        active_button.children[0].value = MSArray.join(',');
        let str = MSNArray.join(',');
        active_button.children[1].innerHTML = (str.length > 50) ? str.slice(0, 50) + "..." : str;
        t = e.target.parentElement.parentElement;
        closeSelectWindow(t);
    })
})

// Закрытие окна выборки
function closeSelectWindow(table) {
    table.classList.remove("active");
    PO.classList.remove("active");
    active_button = null;
    MSArray = [];
    MSNArray = [];
    document.querySelectorAll('.multi-select-record').forEach(inp => {
        inp.checked = false;
    })
    resetSearch(table);
}