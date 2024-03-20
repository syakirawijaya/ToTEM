// script.js

var loadFile = function(event) {
    var output = document.getElementById('imagePreview');
    output.style.display = 'block'; // Show the image container
    if (output.src) {
        URL.revokeObjectURL(output.src); // Revoke the previous object URL
    }
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src); // Free memory when the image is loaded
    };
};
