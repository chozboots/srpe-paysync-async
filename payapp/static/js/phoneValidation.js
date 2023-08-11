document.addEventListener("DOMContentLoaded", function() {
    let phoneField = document.getElementById("phone");
    let phoneError = document.getElementById('phoneError');

    // Phone InputMask Initialization
    $(phoneField).inputmask({"mask": "(999) 999-9999"});

    phoneField.addEventListener("blur", function() {
        // Once the phone input loses focus, it checks if the phone number is taken
        if (phoneField.value) {
            checkPhoneTaken(phoneField, phoneError);
        }
    });
});

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
