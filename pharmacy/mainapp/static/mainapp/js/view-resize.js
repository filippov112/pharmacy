// Изменение размера областей окна записи
// Управляем шириной соседних блоков варьируя соотношение их ширин друг к другу
let size_block = document.getElementById('resize-block');
let rb = document.getElementById('right-block');
let lb = document.getElementById('left-block');
let x0_region = null;
let all_w_reg = null;


size_block.addEventListener('mousedown', e => {
    e.target.classList.add('active');
    x0_region = e.clientX;
    all_w_reg = lb.offsetWidth + rb.offsetWidth
    document.addEventListener('mousemove', resizeRegion);
    document.addEventListener('mouseup', stopResizeRegion);
  });


function resizeRegion(e) {
  const dx = e.clientX - x0_region;
  x0_region = e.clientX;
  const widthCol = Math.min(Math.max(lb.offsetWidth + dx, 0), all_w_reg);

  if (widthCol >= 0) {
    lb.style.width = widthCol + 'px';
    rb.style.width = (all_w_reg - widthCol)+ 'px';
  }
}

function stopResizeRegion(e) {
  e.target.classList.remove('active');
  document.removeEventListener('mousemove', resizeRegion);
  document.removeEventListener('mouseup', stopResizeRegion);
}


window.addEventListener('resize', function() {
    rb.style.removeProperty('width');
    lb.style.removeProperty('width');
});