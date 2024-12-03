// Function to get the CSRF token from the cookie
export function getCsrfToken() {
    const csrfToken = document.cookie
      .split(';')
      .find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}

export const api = axios.create({
    baseURL: `${window.location.origin}`,  // Your API base URL
    withCredentials: true,  // Ensure session cookies are sent with the request
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),  // Include the CSRF token for security
    },
});

// Function to make a GET request to a protected endpoint
export function getData(endpoint) {
    return api.get(endpoint)
      .then(response => response.data)
      .catch(error => {
        console.error('Error:', error);
        throw error;
      });
}

// Function to make a POST request to a protected endpoint
export function postData(endpoint, data) {
    return api.post(endpoint, data)
      .then(response => response.data)
      .catch(error => {
        console.error('Error:', error);
        throw error;
      });
}

// Function to make a PUT request to a protected endpoint
export function putData(endpoint, data) {
    return api.put(endpoint, data)
      .then(response => response.data)
      .catch(error => {
        console.error('Error:', error);
        throw error;
      });
}

// Function to make a PATCH request to a protected endpoint
export function patchData(endpoint, data) {
    return api.patch(endpoint, data)
      .then(response => response.data)
      .catch(error => {
        console.error('Error:', error);
        throw error;
      });
}

// Function to make a DELETE request to a protected endpoint
export function deleteData(endpoint) {
    return api.delete(endpoint)
      .then(response => response.data)
      .catch(error => {
        console.error('Error:', error);
        throw error;
      });
}
