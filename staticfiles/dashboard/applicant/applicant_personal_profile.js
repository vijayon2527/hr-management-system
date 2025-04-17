document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('.needs-validation');
    var errorMessagesContainer = document.getElementById('error-messages');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default submission

        // Clear previous error messages
        errorMessagesContainer.innerHTML = '';
        errorMessagesContainer.style.display = 'none';

        // Remove all existing invalid feedback messages
        var existingErrorMessages = document.querySelectorAll(".invalid-feedback");
        existingErrorMessages.forEach(function(message) {
            message.remove();
        });

        var invalidFields = document.querySelectorAll(".is-invalid");
        invalidFields.forEach(function (field) {
            field.classList.remove("is-invalid");
        });

        var isValid = true;
        var firstInvalidField = null;

        // Validation messages
        const validationMessages = {
            firstName: { empty: "Please enter your first name", invalid: "First name must contain at least one letter." },
            lastName: "Please enter your last name",
            dob: { empty: "Please enter your date of birth", invalid: "You must be at least 18 years old" },
            address: "Please enter your address",
            city: { empty: "Please enter a valid city name (not a number)", invalid: "City must not contain numbers" },
            state: "Please select your state",
            country: "Please select your country",
            postalCode: { empty: "Please enter your postal code", invalid: "Postal code must be exactly 6 digits" },
        };

        // First name validation
        var firstNameField = document.getElementById("id_first_name");
        if (!firstNameField.value) {
            isValid = showError(firstNameField, validationMessages.firstName.empty);
            if (!firstInvalidField) firstInvalidField = firstNameField;
        } else if (!/[A-Za-z]/.test(firstNameField.value)) {
            isValid = showError(firstNameField, validationMessages.firstName.invalid);
            if (!firstInvalidField) firstInvalidField = firstNameField;
        }

        // Last name validation
        var lastNameField = document.getElementById("id_last_name");
        if (!lastNameField.value) {
            isValid = showError(lastNameField, validationMessages.lastName);
            if (!firstInvalidField) firstInvalidField = lastNameField;
        }

        // DOB validation
        let dobField = document.getElementById("id_date_of_birth");
        if (!dobField.value) {
            isValid = showError(dobField, validationMessages.dob.empty);
            if (!firstInvalidField) firstInvalidField = dobField;
        } else {
            let today = new Date();
            let dob = new Date(dobField.value);
        
            // Strip the time part
            dob.setHours(0, 0, 0, 0);
            today.setHours(0, 0, 0, 0);
        
            if (dob > today) {
                isValid = showError(dobField, "Date of birth cannot be in the future.");
                if (!firstInvalidField) firstInvalidField = dobField;
            } else {
                // Calculate age
                let age = today.getFullYear() - dob.getFullYear();
                let monthDiff = today.getMonth() - dob.getMonth();
                if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
                    age--;
                }
        
                if (age < 18) {
                    isValid = showError(dobField, "You must be at least 18 years old.");
                    if (!firstInvalidField) firstInvalidField = dobField;
                }
            }
        }    

        // Address validation
        var addressField1 = document.getElementById("id_address_line_1");
        if (!addressField1.value) {
            isValid = showError(addressField1, validationMessages.address);
            if (!firstInvalidField) firstInvalidField = addressField1;
        }

        // City validation
        var cityField = document.getElementById("id_city");
        if (!cityField.value) {
            isValid = showError(cityField, validationMessages.city.empty);
            if (!firstInvalidField) firstInvalidField = cityField;
        } else if (!/^[a-zA-Z\s]+$/.test(cityField.value)) {
            isValid = showError(cityField, validationMessages.city.invalid);
            if (!firstInvalidField) firstInvalidField = cityField;
        }

        // State validation
        var stateField = document.getElementById("id_state");
        if (stateField.value === "") {
            isValid = showError(stateField, validationMessages.state);
            if (!firstInvalidField) firstInvalidField = stateField;
        }

        // Country validation
        var countryField = document.getElementById("id_country");
        if (countryField.value === "") {
            isValid = showError(countryField, validationMessages.country);
            if (!firstInvalidField) firstInvalidField = countryField;
        }

        // Postal code validation
        var postalCodeField = document.getElementById("id_postal_code");
        if (!postalCodeField.value) {
            isValid = showError(postalCodeField, validationMessages.postalCode.empty);
            if (!firstInvalidField) firstInvalidField = postalCodeField;
        } else if (!/^\d{6}$/.test(postalCodeField.value)) {
            isValid = showError(postalCodeField, validationMessages.postalCode.invalid);
            if (!firstInvalidField) firstInvalidField = postalCodeField;
        }

        // If valid, submit the form
        if (isValid) {
            form.submit();
        } else {
            // Scroll to the first invalid field
            if (firstInvalidField) {
                firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    // Show error function
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
