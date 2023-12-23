// Изменение размера колонок таблицы
// Управляем шириной соседних блоков варьируя соотношение их ширин друг к другу чтобы не задевать таблицу целиком

const tables = Array.from(document.querySelectorAll('.resizable:not(:last-child)'));
let clickedTh = null;
let nextTh = null;
let downX = null;
let all_w_col = null;
let active_el = null;


tables.forEach(table => {
  const handles = Array.from(table.querySelectorAll('.resizable:not(:last-child) .resizable-handle'));
  handles.forEach(handle => {
    handle.addEventListener('mousedown', e => {
      active_el = e.target;
      active_el.classList.add('active');
      clickedTh = active_el.parentElement;
      nextTh = clickedTh.nextElementSibling;
      all_w_col = clickedTh.offsetWidth + nextTh.offsetWidth;
      downX = e.clientX;
      document.addEventListener('mousemove', resizeColumn);
      document.addEventListener('mouseup', stopResize);
    });
  });
});

function resizeColumn(e) {
  let dx = e.clientX - downX;
  downX = e.clientX;
  const widthCol = Math.min(Math.max(clickedTh.offsetWidth + dx, 0), all_w_col);

  if (widthCol >= 0 >= 0) {
    clickedTh.style.width = widthCol + 'px';
    nextTh.style.width = (all_w_col - widthCol) + 'px';
  }
}

function stopResize() {
  active_el.classList.remove('active');
  document.removeEventListener('mousemove', resizeColumn);
  document.removeEventListener('mouseup', stopResize);
  active_el = null;
}
