document.addEventListener('DOMContentLoaded', () => {
    const authScreen = document.getElementById('auth-screen');
    const authForm = document.getElementById('auth-form');
    const appScreen = document.getElementById('app-screen');
    const predictionForm = document.getElementById('prediction-form');
    const resultScreen = document.getElementById('result-screen');
    const priceOutput = document.getElementById('price-output');
    const loadingSpinner = document.getElementById('loading-spinner');
    const startOverBtn = document.getElementById('start-over-btn');

    let currentStep = 1;
    const totalSteps = 3;

    // --- CRITICAL CHANGE: Location Suggestions Data & Population ---
    
    // NOTE: You MUST replace these placeholders with the actual, correctly spelled 
    // names of the top 20-50 localities from your hyderabad_real_estate_dataset3.csv
    const locationData = [
        "Gachibowli", 
        "Kondapur", 
        "Hitech City", 
        "Madhapur", 
        "Jubilee Hills",
        "Banjara Hills",
        "Kukatpally",
        "Miyapur",
        "Manikonda",
        "Secunderabad",
        "Shamshabad",
        "Kompally"
        // Add more locations from your dataset here...
    ];

    const datalist = document.getElementById('location-suggestions');

    function populateLocationSuggestions() {
        locationData.forEach(location => {
            const option = document.createElement('option');
            option.value = location;
            datalist.appendChild(option);
        });
        console.log(`Populated ${locationData.length} location suggestions.`);
    }

    populateLocationSuggestions(); // Run on load

    // --- 1. Authentication Simulation ---
    authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Simple simulation: hide auth, show app after a delay
        setTimeout(() => {
            authScreen.classList.add('hidden');
            appScreen.classList.remove('hidden');
            console.log('Authentication simulated. App started.');
        }, 500);
    });

    // --- 2. Multi-Step Navigation ---
    document.querySelectorAll('.next-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const currentStepDiv = document.getElementById(`step-${currentStep}`);
            const nextStepId = e.target.dataset.next;
            
            // Basic validation check (ensure fields in current step are filled)
            const currentInputs = currentStepDiv.querySelectorAll('input[required], select[required]');
            let isValid = true;
            currentInputs.forEach(input => {
                if (!input.value) {
                    isValid = false;
                    input.reportValidity(); // Show native browser validation error
                }
            });

            if (isValid) {
                currentStepDiv.classList.add('hidden');
                document.getElementById(nextStepId).classList.remove('hidden');
                currentStep = parseInt(nextStepId.split('-')[1]);
            }
        });
    });

    document.querySelectorAll('.prev-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const currentStepDiv = document.getElementById(`step-${currentStep}`);
            const prevStepId = e.target.dataset.prev;
            
            currentStepDiv.classList.add('hidden');
            document.getElementById(prevStepId).classList.remove('hidden');
            currentStep = parseInt(prevStepId.split('-')[1]);
        });
    });

    // --- 3. Prediction Submission and API Call ---
    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // 1. Gather all form data
        const formData = new FormData(predictionForm);
        const data = {};
        
        // Convert FormData to a JSON object
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Handle checkboxes: Ensure unchecked boxes are sent as 'No'
        data['Gated_Community'] = data['Gated_Community'] || 'No';
        data['Balcony'] = data['Balcony'] || 'No';

        console.log('Data payload sent to API:', data);

        // Hide form, show loading
        document.getElementById('step-3').classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
        
        const apiUrl = 'http://127.0.0.1:5000/predict'; 

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            
            loadingSpinner.classList.add('hidden');
            
            if (response.ok) {
                // Show result screen (Step 4)
                priceOutput.textContent = `₹ ${result.predicted_price_lakhs.toLocaleString()} Lakhs`;
                resultScreen.classList.remove('hidden');
            } else {
                // Handle API error
                priceOutput.textContent = `Error: ${result.error || 'Server Problem'}`;
                resultScreen.classList.remove('hidden');
                console.error('API Error:', result);
            }

        } catch (error) {
            loadingSpinner.classList.add('hidden');
            priceOutput.textContent = 'Network Error. Is the Flask server running?';
            resultScreen.classList.remove('hidden');
            console.error('Fetch Error:', error);
        }
    });
    
    // --- 4. Reset Button ---
    startOverBtn.addEventListener('click', () => {
        // Reset form and navigation
        predictionForm.reset();
        resultScreen.classList.add('hidden');
        document.getElementById(`step-1`).classList.remove('hidden');
        currentStep = 1;
    });

});