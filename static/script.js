document.getElementById('nameForm').addEventListener('submit', function(event) {
    // event.preventDefault();
    // Store the names in session storage
    sessionStorage.setItem('firstName', document.getElementById('firstName').value);
    sessionStorage.setItem('lastName', document.getElementById('lastName').value);
    // Redirect to the upload form
    // window.location.href = 'uploadForm.html';
});


