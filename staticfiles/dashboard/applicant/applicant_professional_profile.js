document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('.needs-validation');
    var errorMessagesContainer = document.getElementById('error-messages');

    form.addEventListener('submit', function (event) {
        // Prevent default submission
        event.preventDefault();

        // Clear previous error messages
        errorMessagesContainer.innerHTML = '';
        errorMessagesContainer.style.display = 'none';

        // Remove all existing invalid feedback messages
        var existingErrorMessages = document.querySelectorAll(".invalid-feedback");
        existingErrorMessages.forEach(function(message) {
            message.remove(); // Remove all previously added error messages
        });

        var invalidFields = document.querySelectorAll(".is-invalid");
        invalidFields.forEach(function (field) {
            field.classList.remove("is-invalid");
        });

        // Initialize a flag to track if the form is valid
        var isValid = true;
        var firstInvalidField = null; // Track the first invalid field

        // Validation messages
        const validationMessages = {
            bio: "Please limit your input to fewer than 500 characters.",
            salary: "Please enter positive number only" // salary validation message
        };

        // Validation for bio
        var bioField = document.getElementById("id_bio");

        if (bioField.value.length > 500) {
            isValid = showError(bioField, validationMessages.bio);
            if (!firstInvalidField) firstInvalidField = bioField;
        }

        // Validation for salary
        var salaryField = document.getElementById("id_desired_salary");
        // Check if the salary field has been entered
        if (!salaryField.value){
            isValid = showError(salaryField, validationMessages.salary);
                if (!firstInvalidField) firstInvalidField = salaryField;
            }
        
        if (salaryField.value) {
            // If a salary is entered, check if it's a valid number and greater than 0
            if (isNaN(salaryField.value) || Number(salaryField.value) <= 0) {
                // Show error if the salary is not a valid number or less than or equal to 0
            isValid = showError(salaryField, validationMessages.salary);
                if (!firstInvalidField) firstInvalidField = salaryField;
            }
        }

        // If the form is valid, submit the form
        if (isValid) {
            form.submit();
        } else {
            // Scroll to the first invalid field or error messages
            if (firstInvalidField) {
                firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                errorMessagesContainer.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });

    // Function to handle showing errors
    function showError(field, message) {

        field.classList.add("is-invalid");
        var errorMessage = document.createElement('div');
        errorMessage.classList.add("invalid-feedback");
        errorMessage.innerText = message;
        field.insertAdjacentElement('afterend', errorMessage);
        errorMessagesContainer.innerHTML += `<p>${message}</p>`;
        return false; // Form is invalid
    }
});
