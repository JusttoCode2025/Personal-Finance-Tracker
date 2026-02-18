// Wait for the DOM to load to ensure elements exist
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            
            const emailInput = document.querySelector('input[placeholder="Email"]');
            const passwordInput = document.querySelector('input[placeholder="Password"]');

            const validEmail = "group1@gmail.com";
            const validPassword = "group1";

            if (emailInput.value === validEmail && passwordInput.value === validPassword) {
                alert("Success! You are now logged in.");
                window.location.href = "/home";
            } else {
                alert("Error: Invalid email or password. Please try again.");
            }
        });
    }
});

