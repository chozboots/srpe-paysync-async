// Script to fill the form for testing purposes
document.addEventListener('DOMContentLoaded', function() {
    let fillTestValues = function() {
        document.getElementById('firstName').value = 'John';
        document.getElementById('lastName').value = 'Doe';
        document.getElementById('email').value = 'john.doe@test.com';
        document.getElementById('phone').value = '(555) 555-5555';
        document.getElementById('password').value = 'Password123!';
        document.getElementById('confirmPassword').value = 'Password123!';
        document.getElementById('address1').value = '123 Test Street';
        document.getElementById('address2').value = 'Apt 4B';
        document.getElementById('city').value = 'Milton';
        document.getElementById('state').value = 'FL';
        document.getElementById('zipCode').value = '12345';
        document.getElementById('terms').checked = true;
    };

    // Uncomment the next line to auto-fill when the page loads
    // fillTestValues();

    // If you want to add a button that fills the form when clicked:
    let btn = document.createElement('button');
    btn.innerText = 'Fill Test Values';
    btn.onclick = fillTestValues;
    let cardBody = document.querySelector('.card-body');  // This selects the card-body where the form is
    cardBody.appendChild(btn);  // Appends the button within that card body.;
});
