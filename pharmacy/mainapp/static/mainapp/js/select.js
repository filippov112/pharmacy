let PO = document.getElementById("page-overlay");
let active_button = null;

// Обработчик нажатия на линк
function refrashHandlerLinks() {
    let links = document.querySelectorAll("button[select]");
    for (let l = 0; l < links.length; l++) {
        links[l].addEventListener("click", function(e) {
            e.preventDefault();
            let vib = document.querySelector('.table-wrap[select-name="'+this.getAttribute("select-name")+'"]');
            active_button = this;
            PO.classList.add("active");
            vib.classList.add("active");
        });
    }
}
refrashHandlerLinks();


let selects = document.querySelectorAll(".table-wrap[select]");
// Обработчик нажатия на запись выборки
for (let v = 0; v < selects.length; v++) {
    selects[v].addEventListener('click', (e)=>{
        if (e.target.tagName === "TD") {
            const record = e.target.parentElement.getAttribute('record');
            const text = e.target.innerHTML;
            active_button.children[0].value = Number(record);
            active_button.children[1].innerHTML = text;

                    // td ->     tr ->        tbody ->      table ->     table-wrap
            let t = e.target.parentElement.parentElement.parentElement.parentElement;
            t.classList.remove("active");
            PO.classList.remove("active");
            active_button = null;
            resetSearch(t);
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