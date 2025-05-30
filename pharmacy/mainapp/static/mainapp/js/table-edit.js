let list_tbody = Array.from(document.querySelectorAll('.table-wrap:has(tbody[name])')).map(tw => {
    return tw.getElementsByTagName("tbody")[0];
});


// Обновление имен инпутов при добавлении/удалении/инициализации записей
function refrashNamesInputs() {
    list_tbody.forEach(tb => {
        let table_name = tb.getAttribute("name");
        let table_fields = tb.getAttribute("fields").split(";")
        let tf_names = table_fields.map((x) => { return x.split(":")[0]} );
        let t_count = tf_names.length;

        let list_inputs = Array.from(tb.getElementsByTagName("INPUT"));
        for(let i = 0; i < list_inputs.length; i++) {
            list_inputs[i].setAttribute("name", table_name + "-" +tf_names[i % t_count]+"-"+ String(parseInt(i / t_count))  );
        }
    })
}

refrashNamesInputs()

// Список актуальных файловых записей, не подлежащих удалению при сохранении
let FSR = document.getElementById("fsr");
FSR.value = Array.from(document.querySelectorAll("input[type=file][load]")).map(x => x.getAttribute('load')).join(',');


// Удаление элемента из списка по совпадению
function removeFirstElement(array, element) {
  var index = array.indexOf(element);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}


// Обновление обработчиков удаления
function refrashHandlerRemove() {
    Array.from(document.querySelectorAll('tbody[name] .table-edit-delete')).forEach(btn => btn.addEventListener('click', (e)=>{
        let row = e.target.parentElement.parentElement;

        // Проверка на удаление старых файловых записей
        let files_input = row.querySelector("input[type=file][load]");
        if (files_input) {
            let file_rec = parseInt(files_input.getAttribute("load"));
            let mfsr = FSR.value === '' ? [] : FSR.value.split(",").map(x => parseInt(x));
            if (mfsr.length > 0 && file_rec) {
                mfsr = removeFirstElement(mfsr, file_rec);
                FSR.value = mfsr.join(",");
            }
        }

        row.remove();
        refrashNamesInputs();
    }));
}

// Проверка на именение старых файловых записей
Array.from(document.querySelectorAll('input[type=file][load]')).forEach(inp => inp.addEventListener('change', (e)=>{
    let file_rec = e.target.getAttribute('load');
    if (FSR && file_rec) {
        let mfsr = FSR.value.split(",");
        mfsr = removeFirstElement(mfsr, file_rec);
        FSR.value = mfsr.join(",");
    }
}));




// Инициализация обработчиков при редактировании уже имеющейся записи
refrashHandlerRemove();

let tag_td, tag_tr, tag_input, tag_label, tag_p, tag_button, tag_img;

// Прокидка обработчиков добавления
Array.from(document.querySelectorAll(".table-title img")).forEach(add_button => {
    add_button.addEventListener('click', (e)=>{
        let tbody = e.target.parentElement.parentElement.getElementsByTagName("tbody")[0];
        let table_fields = tbody.getAttribute("fields").split(";");
        let svg_url = tbody.getAttribute("svg_url");
        if (table_fields.length > 0) {
            tag_tr = document.createElement("tr");

            table_fields.forEach(field => {
                let f_arr = field.split(":");
                let f_type = f_arr[1];
                let f_select = f_arr[2];

                tag_td = document.createElement("td");
                tag_input = document.createElement("input");
                switch(f_type) {
                    case 'text':
                        tag_input.setAttribute("type", "text");
                        tag_td.append(tag_input);
                        break;
                    case 'number':
                        tag_input.setAttribute("type", "number");
                        tag_td.append(tag_input);
                        break;
                    case 'file':
                        tag_label = document.createElement("label");
                        tag_p = document.createElement("p");
                        tag_input.setAttribute("type", "file");
                        tag_label.append(tag_p);
                        tag_label.append(tag_input);

                        tag_td.append(tag_label);
                        break;
                    case 'link':
                        // <button select select-name="doctor">
                        //     <input type="number" name="" id="">
                        //     <p>5464564564</p>
                        // </button>
                        tag_button = document.createElement("button");
                        tag_button.setAttribute("select", "");
                        tag_button.setAttribute("select-name", f_select);

                        tag_input.setAttribute("type", "number");
                        tag_button.append(tag_input);

                        tag_p = document.createElement("p");
                        tag_button.append(tag_p);

                        tag_td.append(tag_button);
                        break;
                }
                tag_tr.append(tag_td);
            });

            // <img class="table-edit-delete" src="svg/delete.svg">
            tag_td = document.createElement("td");
            tag_img = document.createElement("img");
            tag_img.className = "table-edit-delete";
            tag_img.setAttribute("src", svg_url);
            tag_td.append(tag_img);
            tag_tr.append(tag_td);


            tbody.append(tag_tr);
            try {
                refrashHandlerLinks();
            } catch {}
            refrashHandlerInputFiles();
            refrashHandlerRemove();
            refrashNamesInputs();
        }
    });
});