function validateEmailDetailed(emailField, errorMessageElement) {
    // Clear previous states
    emailField.setCustomValidity('');
    emailField.classList.remove('error-input');
    errorMessageElement.textContent = '';

    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    
    if (emailField.value === '') {
        return;  // Exit early if the field is empty
    }

    if (!emailRegex.test(emailField.value)) {
        emailField.setCustomValidity('Invalid email format.');
        emailField.classList.add('error-input');
        errorMessageElement.textContent = 'Invalid email format.';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    let emailField = document.getElementById("email");
    let emailError = document.getElementById('emailError');

    emailField.addEventListener("blur", function() {
        // Check the format of the email
        validateEmailDetailed(emailField, emailError);
        
        // If there's no error-input class, then we check if the email is taken.
        if (emailField.value && !emailField.classList.contains('error-input')) {
            checkEmailTaken(emailField, emailError);
        }
    });
});

function checkEmailTaken(emailField, errorMessageElement) {
    const email = emailField.value;
    fetch("/check-email", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        if(data.email_taken) {
            emailField.setCustomValidity('Email already taken.');
            emailField.classList.add('error-input');
            errorMessageElement.textContent = 'Email already taken.';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
