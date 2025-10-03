document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('uploadForm');

    // Show selected filename
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = `Selected: ${e.target.files[0].name}`;
            submitBtn.disabled = false;
        }
    });

    // Form submission with loading state
    form.addEventListener('submit', () => {
        submitBtn.textContent = 'Processing...';
        submitBtn.disabled = true;
    });
});
