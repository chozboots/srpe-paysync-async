const form = document.getElementById('userRegistrationForm');

// Check if the "error" query parameter is present in the URL
function hasErrorOccurred() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.has('error-input');
}

// Load saved data from local storage when the page loads due to an error
window.addEventListener('load', function() {
    if (hasErrorOccurred()) {
        const savedData = JSON.parse(localStorage.getItem('formData'));
        if (savedData) {
            for (let key in savedData) {
                form[key].value = savedData[key];
            }
        }
    }
});

// Save form data to local storage every 10 seconds
setInterval(function() {
    localStorage.setItem('formData', JSON.stringify({
        first_name: form.first_name.value,
        last_name: form.last_name.value,
        email: form.email.value,
        phone: form.phone.value,
        password: form.password.value,
        address1: form.address1.value,
        address2: form.address2.value,
        city: form.city.value,
        state: form.state.value,
        zip_code: form.zip_code.value
    }));
}, 10000);
