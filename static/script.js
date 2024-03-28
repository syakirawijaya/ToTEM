// script.js

var loadFile = function(event) {
    var output = document.getElementById('imagePreview');
    output.style.display = 'block'; 
    if (output.src) {
        URL.revokeObjectURL(output.src);
    }
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src); 
    };
};
