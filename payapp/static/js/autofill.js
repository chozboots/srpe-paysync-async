const form = document.getElementById('userRegistrationForm');

// Load saved data from local storage when the page loads
window.addEventListener('load', function() {
    const savedData = JSON.parse(localStorage.getItem('formData'));
    if (savedData) {
        for (let key in savedData) {
            form[key].value = savedData[key];
        }
    }
});

// Save form data to local storage every 10 seconds
setInterval(function() {
    localStorage.setItem('formData', JSON.stringify({
        first_name: form.first_name.value,
        last_name: form.last_name.value,
        // ... other fields ...
    }));
}, 10000);