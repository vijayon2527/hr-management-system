document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('.needs-validation');

    form.addEventListener('submit', function (event) {
        // Prevent default submission
        event.preventDefault();

        // Remove all existing invalid feedback messages
        var existingErrorMessages = document.querySelectorAll(".invalid-feedback");
        existingErrorMessages.forEach(function (message) {
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
            companyName: "Please enter the company name.",
            companyWebsite: {
                empty: "Please enter your company website.",
                invalid: "Please enter a valid URL."
            },
            companyLogo: "Please upload a company logo.",
            contactPersonName: {
                empty: "Please enter the contact person's name.",
                invalid: "Contact person's name must not contain numbers."
            },
            contactNumber: {
                empty: "Please enter your contact number.",
                invalid: "Contact number must be a 10-digit number."
            },
            additionalContactNumber: "Additional contact number must be a 10-digit number.",
            companyAddress: "Please enter the company address.",
            city: "Please enter the city.",
            state: "Please select a state.",
            country: "Please enter the country.",
            zipCode: {
                empty: "Please enter the zip code.",
                invalid: "Zip code must be exactly 6 digits."
            },
            industry: "Please enter the industry.",
            companySize: "Please select the company size.",
            linkedinUrl: "Please enter a valid LinkedIn URL.",
            facebookUrl: "Please enter a valid Facebook URL.",
            twitterUrl: "Please enter a valid Twitter URL.",
            instagramUrl: "Please enter a valid Instagram URL."
        };

        // Validation functions
        function showError(field, message) {
            var error = document.createElement('div');
            error.classList.add('invalid-feedback');
            error.textContent = message;
            field.parentNode.appendChild(error);
            field.classList.add('is-invalid');
            return false;
        }

        // Validate each field
        function validateField(field, message, regex = null, rejectOnlyNumbers = false) {
            if (!field.value) {
                isValid = showError(field, message.empty || message);
                if (!firstInvalidField) firstInvalidField = field;
            } else if (rejectOnlyNumbers && /^\d+$/.test(field.value)) {
                // Reject if the field consists only of numbers
                isValid = showError(field, message.invalid || "This field cannot contain only numbers.");
                if (!firstInvalidField) firstInvalidField = field;
            } else if (regex && !regex.test(field.value)) {
                isValid = showError(field, message.invalid || message);
                if (!firstInvalidField) firstInvalidField = field;
            }
        }

        // Validate Company Name (should not be only numbers)
        validateField(document.getElementById('id_company_name'), validationMessages.companyName, null, true);

        // Validate Company Website
        validateField(document.getElementById('id_company_website'), validationMessages.companyWebsite, /^(https?:\/\/[^\s]+$)/);

        // Validate Contact Person Name (should not contain numbers)
        validateField(document.getElementById('id_contact_person_name'), validationMessages.contactPersonName, null, true);

        // Validate Contact Number
        validateField(document.getElementById('id_contact_number'), validationMessages.contactNumber, /^\d{10}$/);

        // Validate Additional Contact Number (if filled)
        var additionalContactNumberField = document.getElementById('id_additional_contact_number');
        if (additionalContactNumberField.value) {
            validateField(additionalContactNumberField, validationMessages.additionalContactNumber, /^\d{10}$/);
        }

        // Validate Company Address (should not be only numbers)
        validateField(document.getElementById('id_company_address'), validationMessages.companyAddress, null, true);

        // Validate City (should not be only numbers)
        validateField(document.getElementById('id_city'), validationMessages.city, null, true);

        // Validate State
        validateField(document.getElementById('id_state'), validationMessages.state);

        // Validate Country
        validateField(document.getElementById('id_country'), validationMessages.country);

        // Validate Zip Code (must be exactly 6 digits)
        validateField(document.getElementById('id_zip_code'), validationMessages.zipCode, /^\d{6}$/);

        // Validate Industry (should not be only numbers)
        validateField(document.getElementById('id_industry'), validationMessages.industry, null, true);

        // Validate Company Size
        validateField(document.getElementById('id_company_size'), validationMessages.companySize);

        // Validate URLs
        validateField(document.getElementById('id_linkedin_url'), validationMessages.linkedinUrl, /^(https?:\/\/[^\s]+$)/);
        validateField(document.getElementById('id_facebook_url'), validationMessages.facebookUrl, /^(https?:\/\/[^\s]+$)/);
        validateField(document.getElementById('id_twitter_url'), validationMessages.twitterUrl, /^(https?:\/\/[^\s]+$)/);
        validateField(document.getElementById('id_instagram_url'), validationMessages.instagramUrl, /^(https?:\/\/[^\s]+$)/);

        // If the form is valid, submit the form
        if (isValid) {
            form.submit();
        } else {
            firstInvalidField.focus(); // Focus on the first invalid field
        }
    });
});
