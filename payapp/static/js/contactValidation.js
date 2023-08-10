document.addEventListener("DOMContentLoaded", function() {
    let emailField = document.getElementById("email");
    let emailError = document.getElementById('emailError');

    emailField.addEventListener("blur", function() {
        // This checks the format of the email
        validateEmailDetailed(emailField, emailError);
        
        // This checks if the email is already taken
        checkEmailTaken(emailField, emailError);
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
            emailField.classList.add('error-input');  // Add the error class
            errorMessageElement.textContent = 'Email already taken.';  // Set the error message
        } else {
            if(!emailField.classList.contains('error-input')) { // only if there's no other error
                emailField.setCustomValidity('');
                errorMessageElement.textContent = '';  // Clear the error message
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
