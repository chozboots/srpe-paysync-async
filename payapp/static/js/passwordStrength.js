document.getElementById('password').addEventListener('input', function(e) {
    const pwd = e.target.value;
    const strengthIndicator = document.getElementById('passwordStrength');

    if (pwd.length < 8 || !/\d/.test(pwd)) {
        strengthIndicator.textContent = 'Weak';
        strengthIndicator.style.color = 'red';
    } else {
        strengthIndicator.textContent = 'Strong';
        strengthIndicator.style.color = 'green';
    }
});