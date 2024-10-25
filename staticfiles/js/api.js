async function apiRequest(endpoint, method = 'GET', body = null, customHeaders = {}) {
    // Validate endpoint URL
    if (typeof endpoint !== 'string' || !/^(https?:\/\/|\/)/.test(endpoint)) {
        throw new Error("Invalid endpoint URL");
    }

    const csrfToken = getCookie('csrftoken'); // Retrieve CSRF token

    const options = {
        method: method.toUpperCase(), // Ensure the method is uppercase
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...customHeaders, // Merge custom headers if provided
        },
        credentials: 'same-origin',
    };

    if (body && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(body); // Convert body to JSON if it's a POST/PUT request
    }

    try {
        const response = await fetch(endpoint, options);

        if (!response.ok) {
            const errorText = await response.text(); // Get error message if any
            throw new Error(`Error: ${response.status} ${response.statusText} - ${errorText}`);
        }

        // Handle different response types if needed
        const contentType = response.headers.get('Content-Type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json(); // Return parsed JSON response
        } else {
            return await response.text(); // Fallback to plain text if not JSON
        }
    } catch (error) {
        console.error("API request failed:", error);
        return { error: error.message }; // Return error message
    }
}

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))?.split('=')[1];

    return cookieValue ? decodeURIComponent(cookieValue) : null; // Decode the cookie value
}

