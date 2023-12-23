// Тап по оверлею
document.getElementById("page-overlay").addEventListener('mousedown', disactive);

// Деактивация модальных элементов
function disactive() {
    ['page-overlay', 'sidebar', 'modal-delete'].forEach(elem => {
        let e = document.getElementById(elem);
        if (e) {
            e.classList.remove("active");
        }
    });

    let vs = document.querySelectorAll(".table-wrap[select]");
    for (let i = 0; i < vs.length; i++) {
        vs[i].classList.remove("active");
        resetSearch(vs[i]);
    }
    try {
        active_button = null;
    } catch {}
}