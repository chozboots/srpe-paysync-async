document.addEventListener("DOMContentLoaded", function() {
    let phoneField = document.getElementById("phone");
    let phoneError = document.getElementById('phoneError');

    // Phone InputMask Initialization
    $(phoneField).inputmask({"mask": "(999) 999-9999"});

    phoneField.addEventListener("blur", function() {
        // Check the format of the phone number
        validatePhoneDetailed(phoneField, phoneError);

        // If there's no error-input class, then we check if the phone number is taken.
        if (phoneField.value && !phoneField.classList.contains('error-input')) {
            checkPhoneTaken(phoneField, phoneError);
        }
    });
});

function validatePhoneDetailed(phoneField, errorMessageElement) {
    // Clear previous states
    phoneField.setCustomValidity('');
    phoneField.classList.remove('error-input');
    errorMessageElement.textContent = '';

    const phoneRegex = /^\(\d{3}\) \d{3}-\d{4}$/;
    
    if (phoneField.value === '') {
        return;  // Exit early if the field is empty
    }

    if (!phoneRegex.test(phoneField.value)) {
        phoneField.setCustomValidity('Invalid phone number format.');
        phoneField.classList.add('error-input');
        errorMessageElement.textContent = 'Invalid phone number format.';
    }
}

// The checkPhoneTaken function remains the same as in your original code

function checkPhoneTaken(phoneField, errorMessageElement) {
    // Clear any previous custom validity messages
    phoneField.setCustomValidity('');

    const phone = phoneField.value;
    fetch("/check-phone", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone: phone }),
    })
    .then(response => response.json())
    .then(data => {
        if(data.phone_taken) {
            phoneField.setCustomValidity('Phone number already taken.');
            phoneField.classList.add('error-input');  // Add the error class
            errorMessageElement.textContent = 'Phone number already taken.';  // Set the error message
        } else {
            phoneField.classList.remove('error-input');
            errorMessageElement.textContent = '';  // Clear the error message
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
