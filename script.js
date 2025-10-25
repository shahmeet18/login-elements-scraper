// DOM elements
const form = document.getElementById('scrapeForm');
const urlInput = document.getElementById('url');
const submitBtn = document.getElementById('submitBtn');
const urlError = document.getElementById('urlError');
const resultsSection = document.getElementById('resultsSection');
const resultCount = document.getElementById('resultCount');
const jsonOutput = document.getElementById('jsonOutput');
const copyBtn = document.getElementById('copyBtn');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');

// Form validation
function validateURL(url) {
    try {
        const parsedURL = new URL(url);
        return parsedURL.protocol === 'http:' || parsedURL.protocol === 'https:';
    } catch {
        return false;
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
}

function hideError() {
    errorSection.style.display = 'none';
}

function showLoading() {
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    hideError();
}

function hideLoading() {
    loadingSection.style.display = 'none';
}

function showResults(data) {
    resultCount.textContent = `Found ${data.count} login element${data.count !== 1 ? 's' : ''}`;
    jsonOutput.textContent = JSON.stringify(data, null, 2);
    resultsSection.style.display = 'block';
    hideLoading();
    hideError();
}

// API call
async function scrapeLoginElements(url) {
    const response = await fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: url
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An error occurred while scraping');
    }

    return await response.json();
}

// Copy to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = '#17a2b8';
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    } catch (err) {
        console.error('Failed to copy: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }
}

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = urlInput.value.trim();

    // Clear previous error
    urlError.textContent = '';

    // Validate URL
    if (!validateURL(url)) {
        urlError.textContent = 'Please enter a valid HTTP or HTTPS URL.';
        urlInput.focus();
        return;
    }

    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Scraping...';

    showLoading();

    try {
        const data = await scrapeLoginElements(url);
        showResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Scrape Login Elements';
    }
});

// Copy button event listener
copyBtn.addEventListener('click', () => {
    const jsonText = jsonOutput.textContent;
    copyToClipboard(jsonText);
});

// URL input validation on blur
urlInput.addEventListener('blur', () => {
    const url = urlInput.value.trim();
    if (url && !validateURL(url)) {
        urlError.textContent = 'Please enter a valid HTTP or HTTPS URL.';
    } else {
        urlError.textContent = '';
    }
});

// Clear error on input
urlInput.addEventListener('input', () => {
    if (urlError.textContent) {
        urlError.textContent = '';
    }
});

// Example tags functionality
document.querySelectorAll('.tag').forEach(tag => {
    tag.addEventListener('click', () => {
        const url = tag.getAttribute('data-url');
        urlInput.value = url;
        urlInput.focus();
        // Clear any existing error
        urlError.textContent = '';
    });
});