document.getElementById('nameForm').addEventListener('submit', function(event) {
    //event.preventDefault();
    // Store the names in session storage
    sessionStorage.setItem('firstName', document.getElementById('firstName').value);
    sessionStorage.setItem('lastName', document.getElementById('lastName').value);
    // Redirect to the upload form
    // window.location.href = 'uploadForm.html';
});

document.getElementById('imageInput').addEventListener('change', function(event) {
    var output = document.getElementById('imagePreview');
    output.style.display = 'block'; // Show the image container
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // Free memory when the image is loaded
    }
});