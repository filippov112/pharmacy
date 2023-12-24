// Сообщение об ошибке
document.addEventListener("DOMContentLoaded", function() {
  var hiddenBlock = document.getElementById("servMesBlock");
  
  if (hiddenBlock.innerText.trim() !== "") {
    hiddenBlock.style.display = "block";
    setTimeout(function() {
      hiddenBlock.style.transform = "translateY(-500px)";
      setTimeout(function() {
        hiddenBlock.remove();
      }, 500);
    }, 5000);
  }
});


function refrashHandlerInputFiles() {
  Array.from(document.querySelectorAll('label:not(:has(img)) input[type=file]')).forEach(inp => inp.addEventListener('change', (e)=>{

    if (e.target.files) {
      if (e.target.files[0]) {
        let file = e.target.files[0];
        e.target.previousElementSibling.innerText = file.name;
      }
    }

  }));
}
refrashHandlerInputFiles();

const fileTypes = [
  "image/apng",
  "image/bmp",
  "image/gif",
  "image/jpeg",
  "image/pjpeg",
  "image/png",
  "image/svg+xml",
  "image/tiff",
  "image/webp",
  "image/x-icon"
];

function validFileType(file) {
  return fileTypes.includes(file.type);
}

Array.from(document.querySelectorAll('.edit-input-block:has(img) input[type=file]')).forEach(el => {
  el.addEventListener("change", showPreview);
});
function showPreview(e) {
  let files = e.target.files;

  if (files.length !== 0) {
    let f = files[0];
    if (validFileType(f)) {
        this.nextElementSibling.setAttribute("src", URL.createObjectURL(f));
    }
  }
}