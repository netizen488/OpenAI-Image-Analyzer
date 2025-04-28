const form = document.getElementById('upload-form');
const imageFileInput = document.getElementById('image-file');
const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const file = imageFileInput.files[0];
    if (!file) {
        resultDiv.innerHTML = '<p style="color: red;">Please select an image file first.</p>';
        return;
    }

    // Basic client-side size check (optional, but good practice)
    // OpenAI has a 20MB limit, but you might want smaller limits
    if (file.size > 20 * 1024 * 1024) {
         resultDiv.innerHTML = '<p style="color: red;">File is too large (max 20MB).</p>';
         return;
    }

    resultDiv.innerHTML = '<p>Submit an image to see the analysis here.</p>'; // Clear previous result
    loadingDiv.style.display = 'block'; // Show loading indicator

    const formData = new FormData();
    formData.append('file', file);

    try {
        // IMPORTANT: This '/analyze-image/' path must match your Nginx proxy and FastAPI endpoint
        const response = await fetch('/analyze-image/', {
            method: 'POST',
            body: formData,
            // Headers are generally not needed for FormData with fetch,
            // the browser sets Content-Type to multipart/form-data correctly
        });

        loadingDiv.style.display = 'none'; // Hide loading indicator

        if (!response.ok) {
            // Try to get error message from backend response body
            let errorMsg = `Error: ${response.status} ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMsg = `Error: ${errorData.detail || JSON.stringify(errorData)}`;
            } catch (e) { /* Ignore if response is not JSON */ }
             resultDiv.innerHTML = `<p style="color: red;">${errorMsg}</p>`;
             console.error('Analysis request failed:', response);
            return;
        }

        const data = await response.json();

        if (data.analysis) {
            resultDiv.textContent = data.analysis; // Use textContent to prevent HTML injection
        } else {
            resultDiv.innerHTML = '<p style="color: orange;">Received empty analysis from server.</p>';
        }

    } catch (error) {
        loadingDiv.style.display = 'none'; // Hide loading indicator
        resultDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
        console.error('Error submitting form:', error);
    }
});