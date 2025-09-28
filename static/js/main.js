document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');

    // Drag and drop functionality
    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateUploadArea(files[0].name);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            updateUploadArea(e.target.files[0].name);
        }
    });

    function updateUploadArea(filename) {
        uploadArea.innerHTML = `<p>Selected: ${filename}</p>`;
        submitBtn.disabled = false;
    }

    // Form submission with loading state
    const form = document.getElementById('uploadForm');
    form.addEventListener('submit', () => {
        submitBtn.textContent = 'Processing...';
        submitBtn.disabled = true;
    });
});
