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
    
    // --- New Input Element ---
    const locationInput = document.getElementById('location-input'); // Targeting the new ID

    // --- CRITICAL CHANGE: Dynamic Location Suggestions via Fetch ---
    const datalist = document.getElementById('location-suggestions');
    // Use absolute path /static/... to ensure the browser always finds the file
    const JSON_URL = '/static/location_suggestions.json'; 

    async function populateLocationSuggestions() {
        try {
            const response = await fetch(JSON_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const locationData = await response.json();
            
            datalist.innerHTML = ''; 

            locationData.forEach(location => {
                const option = document.createElement('option');
                option.value = location;
                datalist.appendChild(option);
            });
            console.log(`Datalist population complete. Total items added: ${locationData.length}`);
        } catch (error) {
            console.error('Failed to fetch location data.', error);
        }
    }

    populateLocationSuggestions(); // Run on load

    // --- NEW: Force Datalist Opening on Focus (Browser Dependent Trick) ---
    if (locationInput) {
        locationInput.addEventListener('focus', function() {
            // If the input value is empty, temporarily add and remove a space
            // This is a common trick to force the browser to display suggestions
            if (this.value === "") {
                this.value = ' '; 
                this.value = ''; 
            }
        });
    }

    // --- 1. Authentication Simulation ---
    authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        setTimeout(() => {
            authScreen.classList.add('hidden');
            appScreen.classList.remove('hidden');
        }, 500);
    });

    // --- 2. Multi-Step Navigation ---
    document.querySelectorAll('.next-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const currentStepDiv = document.getElementById(`step-${currentStep}`);
            const nextStepId = e.target.dataset.next;
            
            const currentInputs = currentStepDiv.querySelectorAll('input[required], select[required]');
            let isValid = true;
            currentInputs.forEach(input => {
                if (!input.value) {
                    isValid = false;
                    input.reportValidity();
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
        
        const formData = new FormData(predictionForm);
        const data = {};
        
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        data['Gated_Community'] = data['Gated_Community'] || 'No';
        data['Balcony'] = data['Balcony'] || 'No';

        console.log('Data payload sent to API:', data);

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
                priceOutput.textContent = `₹ ${result.predicted_price_lakhs.toLocaleString()} Lakhs`;
                resultScreen.classList.remove('hidden');
            } else {
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
        predictionForm.reset();
        resultScreen.classList.add('hidden');
        document.getElementById(`step-1`).classList.remove('hidden');
        currentStep = 1;
    });

});