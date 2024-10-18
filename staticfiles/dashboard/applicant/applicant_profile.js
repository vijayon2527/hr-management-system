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
            firstName: {
                empty: "Please enter your first name",
                invalid: "First name must contain at least one letter."
            },
            lastName: "Please enter your last name",
            dob: { 
                empty: "Please enter your date of birth",
                invalid: "You must be at least 20 years old",
            },
            address: "Please enter your address",
            city: "Please enter a valid city name (not a number)",
            state: "Please select your state",
            country: "Please select your country",
            postalCode: {
                empty: "Please enter your postal code",
                invalid: "Postal code must be exactly 6 digits"
            },
            bio: "Please limit your input to fewer than 500 characters.",
            username: "Please enter your mobile number", // Username validation message
            password: "Please provide a password" ,// Password validation message
            salary: "Please enter positive number only" // salary validation message
        };

        // Validation for first name
        var firstNameField = document.getElementById("id_first_name");
        if (!firstNameField.value) {
            isValid = showError(firstNameField, validationMessages.firstName.empty);
            if (!firstInvalidField) firstInvalidField = firstNameField; // Set first invalid field
        } else if (!/[A-Za-z]/.test(firstNameField.value)) {
            isValid = showError(firstNameField, validationMessages.firstName.invalid);
            if (!firstInvalidField) firstInvalidField = firstNameField; // Set first invalid field
        } 


        // Validation for last name
        var lastNameField = document.getElementById("id_last_name");
        if (!lastNameField.value) {
            isValid = showError(lastNameField, validationMessages.lastName);
            if (!firstInvalidField) firstInvalidField = lastNameField;
        }

        // Validation for date of birth (at least 20 years old)
        let dobField = document.getElementById("id_date_of_birth");
        if (!dobField.value) {
            isValid = showError(dobField, validationMessages.dob.empty);
            if (!firstInvalidField) firstInvalidField = dobField;
        } else {
            let today = new Date();
            let dob = new Date(dobField.value);
            let age = today.getFullYear() - dob.getFullYear();
            let monthDifference = today.getMonth() - dob.getMonth();

            // Adjust if the birthday hasn't happened yet this year
            if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dob.getDate())) {
                age--;
            }
            // Check if age is less than 20
            if (age < 20) {
                isValid = showError(dobField, validationMessages.dob.invalid);
                if (!firstInvalidField) firstInvalidField = dobField;
            }
        }

        // Validation for address
        var addressField1 = document.getElementById("id_address_line_1");
        if (!addressField1.value) {
            isValid = showError(addressField1, validationMessages.address);
            if (!firstInvalidField) firstInvalidField = addressField1;
        }

        // Validation for city
        var cityField = document.getElementById("id_city");
        if (!cityField.value) {
            isValid = showError(cityField, validationMessages.city);
            if (!firstInvalidField) firstInvalidField = cityField;
        } else if (!/^[a-zA-Z\s]+$/.test(cityField.value)) {
            isValid = showError(cityField, validationMessages.city);
            if (!firstInvalidField) firstInvalidField = cityField; // Track the first invalid city field
        }

        // Validation for state
        var stateField = document.getElementById("id_state");
        if (stateField.value === "") {
            isValid = showError(stateField, validationMessages.state);
            if (!firstInvalidField) firstInvalidField = stateField;
        }

        // Validation for country
        var countryField = document.getElementById("id_country");
        if (countryField.value === "") {
            isValid = showError(countryField, validationMessages.country);
            if (!firstInvalidField) firstInvalidField = countryField;
        }

        // Validation for postal code
        var postalCodeField = document.getElementById("id_postal_code");
        if (!postalCodeField.value) {
            isValid = showError(postalCodeField, validationMessages.postalCode.empty);
            if (!firstInvalidField) firstInvalidField = postalCodeField;
        } else if (!/^\d{6}$/.test(postalCodeField.value)) {
            isValid = showError(postalCodeField, validationMessages.postalCode.invalid);
            if (!firstInvalidField) firstInvalidField = postalCodeField;
        }

        // // Validation for bio
        // var bioField = document.getElementById("id_bio");
        // if (bioField.value.length > 500) {
        //     isValid = showError(bioField, validationMessages.bio);
        //     if (!firstInvalidField) firstInvalidField = bioField;
        // }

        // // Validation for salary
        // var salaryField = document.getElementById("id_desired_salary");

        // // Check if the salary field has been entered
        // if (salaryField.value) {
        //     // If a salary is entered, check if it's a valid number and greater than 0
        //     if (isNaN(salaryField.value) || Number(salaryField.value) <= 0) {
        //         // Show error if the salary is not a valid number or less than or equal to 0
        //         isValid = showError(salaryField, validationMessages.salary);
        //         if (!firstInvalidField) firstInvalidField = salaryField;
        //     }
        // }


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
