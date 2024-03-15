document.getElementById('nameForm').addEventListener('submit', function(event) {
    // event.preventDefault();
    // Store the names in session storage
    sessionStorage.setItem('firstName', document.getElementById('firstName').value);
    sessionStorage.setItem('lastName', document.getElementById('lastName').value);
    // Redirect to the upload form
    // window.location.href = 'uploadForm.html';
});

console.log('Script loaded.');
document.getElementById('imageInput').addEventListener('change', function(event) {
    console.log('File selected:', event.target.files[0]);
    var output = document.getElementById('imagePreview');
    output.style.display = 'block';
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        console.log('Image loaded.');
        URL.revokeObjectURL(output.src);
    };
});
