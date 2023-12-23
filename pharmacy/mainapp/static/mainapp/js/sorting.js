// Блок сортировки таблиц

let block = document.getElementById('sorting');


// Кнопка вызова окна сортировки
function show_sort() {
    block.classList.toggle("active");
    block.style.top = block.style.top === "50px" ? -block.clientHeight + "px" : "50px";
}

// Простановка порядка сортировки
function updateInputNumbers() {
  const inputs = document.querySelectorAll('.sorting-number'); // Нельзя выносить из функции, т.к. нужно состояние на момент вызова функции
  inputs.forEach(function(input, inputIndex) {
      input.value = inputIndex;
  });
}

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
      updateInputNumbers();
  }
}



block.style.top = -block.clientHeight + "px";
updateInputNumbers(); // Изначальная сортировка (пригодится для сброса сортировки по умолчанию)

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

