// --- Custom Dropdown Logic ---
// I'm building a custom dropdown to match my site's brutaliast style.
const customSelectWrapper = document.getElementById('custom-service-select');
const customSelectTrigger = customSelectWrapper.querySelector('.custom-select-trigger');
const customSelectOptions = customSelectWrapper.querySelectorAll('.custom-option');
const hiddenServiceInput = document.getElementById('service');
const customSelectText = customSelectWrapper.querySelector('.custom-select-text');

// I'll toggle the dropdown open/close when the trigger is clicked.
customSelectTrigger.addEventListener('click', function(e) {
    customSelectWrapper.classList.toggle('open');
    e.stopPropagation(); // This prevents the body click from firing immediately.
});

// Now, I'll handle the option selection.
customSelectOptions.forEach(option => {
    option.addEventListener('click', function() {
        // First, I remove the active class from all options.
        customSelectOptions.forEach(opt => opt.classList.remove('active'));
        // Then, I add the active class to the one I clicked.
        this.classList.add('active');
        
        // I need to update the text in the trigger to show the selected option.
        customSelectText.textContent = this.textContent;
        // And I'll update the hidden input's value for my API payload.
        hiddenServiceInput.value = this.getAttribute('data-value');
        
        // Finally, I close the dropdown.
        customSelectWrapper.classList.remove('open');
    });
});

// I want to close the dropdown if the user clicks anywhere else on the screen.
document.addEventListener('click', function(e) {
    if (!customSelectWrapper.contains(e.target)) {
        customSelectWrapper.classList.remove('open');
    }
});

// --- 1. UI Logic for Custom City Buttons ---
// I created this function to handle the logic for my city selector buttons.
function setupCitySelectors(groupId) {
    const container = document.getElementById(groupId);
    const buttons = container.querySelectorAll('.city-btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            // I remove the 'active' class from all buttons in this group first.
            buttons.forEach(b => b.classList.remove('active'));
            // Then I add the 'active' class to the button that was just clicked.
            btn.classList.add('active');
        });
    });
}

// I need to initialize both of my button groups.
setupCitySelectors('origin-selector');
setupCitySelectors('destination-selector');

// --- 2. API Logic ---
// Here's where I handle the form submission and API call.
const form = document.getElementById('prediction-form');
const resultBox = document.getElementById('result-box');
const timeOutput = document.getElementById('time-output');
const submitBtn = document.querySelector('.submit-btn');

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    // I want to give the user some feedback while the API is working.
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="ph-bold ph-spinner-gap ph-spin"></i> Calculating...';

    // I need to find which button has the 'active' class in each group.
    const activeOrigin = document.querySelector('#origin-selector .city-btn.active').getAttribute('data-value');
    const activeDest = document.querySelector('#destination-selector .city-btn.active').getAttribute('data-value');

    // This is the data I'll send to my API.
    const payload = {
        origin: activeOrigin,
        destination: activeDest,
        weight: parseFloat(document.getElementById('weight').value),
        service: document.getElementById('service').value
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            // If the API call is successful, I'll display the result.
            timeOutput.innerText = data.predicted_hours;
            resultBox.style.display = 'block';
            // I'm resetting the error colors just in case they were set from a previous error.
            resultBox.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
            resultBox.style.borderColor = 'rgba(16, 185, 129, 0.2)';
            document.querySelector('#result-box p').innerText = "ESTIMATED TRANSIT TIME";
            document.querySelector('#result-box p').style.color = "#6ee7b7";
            timeOutput.style.color = "#34d399";
        } else {
            throw new Error(data.error || "Server error");
        }
    } catch (error) {
        // If there's an error, I want to display an error state.
        resultBox.style.display = 'block';
        resultBox.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
        resultBox.style.borderColor = 'rgba(239, 68, 68, 0.2)';
        document.querySelector('#result-box p').innerText = "ERROR";
        document.querySelector('#result-box p').style.color = "#fca5a5";
        timeOutput.innerText = "N/A";
        timeOutput.style.color = "#f87171";
        console.error('Prediction failed:', error);
    } finally {
        // I need to revert the button text back to its original state.
        submitBtn.innerHTML = originalBtnText;
    }
});