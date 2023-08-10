document.addEventListener("DOMContentLoaded", function() {
    let emailField = document.getElementById("email");
    let phoneField = document.getElementById("phone");

    emailField.addEventListener("input", function() {
        validateEmail(emailField);  // Ensure this function is either defined or removed
    });

    // Phone InputMask Initialization
    $(phoneField).inputmask({"mask": "(999) 999-9999"});
});
