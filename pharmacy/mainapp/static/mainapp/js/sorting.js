// Блок сортировки таблиц
let block = document.getElementById('sorting');
let button = document.getElementById("submit-filter");
let psevdo_button = document.getElementById("submit-sorting");
let input = document.getElementById("parameter_sorting");


// Кнопка вызова окна сортировки
function show_sort() {
    block.classList.toggle("active");
    block.style.top = block.style.top === "50px" ? -block.clientHeight + "px" : "50px";
}
block.style.top = -block.clientHeight + "px";


// Перестановка группы
function moveGroup(group, direction) {
  const groups = document.querySelectorAll('.group');
  const index = Array.from(groups).indexOf(group);
  const targetIndex = direction === 'up' ? index - 1 : index + 1;

  if ((targetIndex < groups.length && direction === 'down') || (targetIndex >= 0 && direction === 'up')) {
      if (direction === 'down') {
          groups[targetIndex].insertAdjacentElement('afterend', group);
      } else {
          groups[targetIndex].insertAdjacentElement('beforebegin', group);
      }
  }
}
// Рычаги поднятия группы
document.querySelectorAll('.up').forEach(function(button) {
  button.addEventListener('click', function(event) {
    event.preventDefault();
    moveGroup(this.parentElement, 'up');
  });
});
// Рычаги опускания группы
document.querySelectorAll('.down').forEach(function(button) {
  button.addEventListener('click', function(event) {
    event.preventDefault();
    moveGroup(this.parentElement, 'down');
  });
});


// Формирование строки параметров сортировки при нажатии отправки формы
psevdo_button.addEventListener('click', function(e) {
  let fields = Array.from(document.getElementsByClassName("group")).map( (x)=>{ return x.getAttribute("name") });
  let checks = Array.from(document.getElementsByClassName("sort-check")).map( (x)=> { return x.checked });
  let dirs = Array.from(document.getElementsByClassName("sort-dir")).map( (x)=> { return x.checked });

  let rez = "";

  for(i = 0; i < checks.length; i++){
    if (checks[i]) {
      if (rez !== "") {
        rez += ",";
      }
      if (dirs[i]) {
        rez += "-"+fields[i];
      } else {
        rez += fields[i];
      }
    }
  }

  input.value = rez;
  button.click();
});