document.addEventListener('DOMContentLoaded', function() {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');
    var dropdown1 = document.getElementById('dropdown1');
    var dropdown2 = document.getElementById('dropdown2');

    spinner.style.display = "none"; // Hide the spinner initially
    includeSecondPair.checked = true; // Check the checkbox initially

    // Always show the second pair on the initial load
    secondPair.style.display = "";

    // Retrieve checkbox state from local storage and update checkbox state
    var isChecked = localStorage.getItem('includeSecondPair');
    if (isChecked === 'unchecked') {
        includeSecondPair.checked = false;
        secondPair.style.display = "none";
    }

    // Fetch the locations.json file
    fetch('/static/locations.json')
        .then(response => response.json())
        .then(data => {
            // Loop through each item in the data
            for (let i = 0; i < data.length; i++) {
                let locationPair = data[i];

                // Create a new option for the dropdown
                let option1 = document.createElement("option");
                option1.value = i;  // Store the index as the option's value
                option1.text = locationPair.location1.name;

                // Create a new option for the second dropdown
                let option2 = document.createElement("option");
                option2.value = i;  // Store the index as the option's value
                option2.text = locationPair.location2.name;

                // Add the options to their respective dropdowns
                dropdown1.appendChild(option1);
                dropdown2.appendChild(option2);
            }

            // Update input fields when a dropdown value is selected
            dropdown1.addEventListener('change', function() {
                let selectedPairIndex = this.value;
                let selectedPair = data[selectedPairIndex];

                // Update input fields for the first pair
                document.getElementById('location1Name').value = selectedPair.location1.name;
                document.getElementById('latitude1').value = selectedPair.location1.latitude;
                document.getElementById('longitude1').value = selectedPair.location1.longitude;
                document.getElementById('location2Name').value = selectedPair.location2.name;
                document.getElementById('latitude2').value = selectedPair.location2.latitude;
                document.getElementById('longitude2').value = selectedPair.location2.longitude;
            });

            dropdown2.addEventListener('change', function() {
                let selectedPairIndex = this.value;
                let selectedPair = data[selectedPairIndex];

                // Update input fields for the second pair
                document.getElementById('location3Name').value = selectedPair.location1.name;
                document.getElementById('latitude3').value = selectedPair.location1.latitude;
                document.getElementById('longitude3').value = selectedPair.location1.longitude;
                document.getElementById('location4Name').value = selectedPair.location2.name;
                document.getElementById('latitude4').value = selectedPair.location2.latitude;
                document.getElementById('longitude4').value = selectedPair.location2.longitude;
            });
        });

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
        // Save checkbox state
        localStorage.setItem('includeSecondPair', includeSecondPair.checked ? 'checked' : 'unchecked');
    });

    includeSecondPair.addEventListener('change', function() {
        if (this.checked) {
            // Show second pair and enable all inputs
            secondPair.style.display = "";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.disabled = false;
            });
        } else {
            // Hide second pair and disable all inputs
            secondPair.style.display = "none";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.disabled = true;
            });
        }
    });
});
