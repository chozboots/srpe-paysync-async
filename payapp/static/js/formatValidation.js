document.getElementById('userRegistrationForm').addEventListener('submit', function(e) {
    const pwd = document.getElementById('password').value;
    const confirmPwd = document.getElementById('confirmPassword').value;

    if (pwd !== confirmPwd) {
        alert('Passwords do not match.');
        e.preventDefault();  // Prevent form submission
    }
});