document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' || event.key === 'F5') {
            event.preventDefault();
            sessionStorage.removeItem('pageWasVisited');
            window.location.href = '../index.html';
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('file-upload');
    const imagesButton = document.getElementById('images-tab-btn');
    const dropzone = document.querySelector('.upload__dropzone');
    const currentUploadInput = document.querySelector('.upload__input');
    const copyButton = document.querySelector('.upload__copy');

    const backendURL = window.location.origin; // автоматично підхопить http://localhost:8080

    const updateTabStyles = () => {
        const uploadTab = document.getElementById('upload-tab-btn');
        const imagesTab = document.getElementById('images-tab-btn');
        const isImagesPage = window.location.pathname.includes('images.html');

        uploadTab.classList.remove('upload__tab--active');
        imagesTab.classList.remove('upload__tab--active');

        if (isImagesPage) {
            imagesTab.classList.add('upload__tab--active');
        } else {
            uploadTab.classList.add('upload__tab--active');
        }
    };

    const uploadFileToServer = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${backendURL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const data = await response.json();

            // універсально для будь-якого типу відповіді
            const finalUrl = data.url.startsWith('http')
                ? data.url
                : `${backendURL}${data.url}`;

            return finalUrl;
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file!');
            return null;
        }
    };


    const handleAndStoreFiles = async (files) => {
        if (!files || files.length === 0) return;

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        const MAX_SIZE_MB = 5;
        const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
        let storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || [];
        let lastUploadedUrl = '';

        for (const file of files) {
            if (!allowedTypes.includes(file.type)) {
                alert(`${file.name} — unsupported type`);
                continue;
            }
            if (file.size > MAX_SIZE_BYTES) {
                alert(`${file.name} — file too large (>5MB)`);
                continue;
            }

            const uploadedUrl = await uploadFileToServer(file);
            if (uploadedUrl) {
                storedFiles.push({ name: file.name, url: uploadedUrl });
                lastUploadedUrl = uploadedUrl;
            }
        }

        if (storedFiles.length > 0) {
            localStorage.setItem('uploadedImages', JSON.stringify(storedFiles));

            if (currentUploadInput && lastUploadedUrl) {
                currentUploadInput.value = lastUploadedUrl;
            }

            alert('✅ Files uploaded successfully! Go to the "Images" tab to view them.');
        }
    };

    // COPY BUTTON
    if (copyButton && currentUploadInput) {
        copyButton.addEventListener('click', () => {
            const textToCopy = currentUploadInput.value;
            if (textToCopy && textToCopy.startsWith('http')) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    copyButton.textContent = 'COPIED!';
                    setTimeout(() => (copyButton.textContent = 'COPY'), 2000);
                });
            }
        });
    }

    // NAVIGATION BUTTON
    if (imagesButton) {
        imagesButton.addEventListener('click', () => {
            window.location.href = 'images.html';
        });
    }

    // FILE INPUT
    fileUpload.addEventListener('change', async (event) => {
        await handleAndStoreFiles(event.target.files);
        event.target.value = '';
    });

    // DRAG&DROP
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    dropzone.addEventListener('drop', async (event) => {
        await handleAndStoreFiles(event.dataTransfer.files);
    });

    updateTabStyles();
});
