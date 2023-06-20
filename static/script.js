document.addEventListener('DOMContentLoaded', function() {
    var spinner = document.getElementById('spinner');
    var firstPair = document.getElementById('firstPair');
    var secondPair = document.getElementById('secondPair');
    var pair1Checkbox = document.getElementById('pair1Checkbox');
    var pair2Checkbox = document.getElementById('pair2Checkbox');
    var dropdown1 = document.getElementById('dropdown1');
    var dropdown2 = document.getElementById('dropdown2');

    spinner.style.display = "none"; // Hide the spinner initially

    // Retrieve checkbox states from local storage and update checkbox states
    var isChecked1 = localStorage.getItem('includeFirstPair');
    if (isChecked1 === 'unchecked') {
        pair1Checkbox.checked = false;
    }

    var isChecked2 = localStorage.getItem('includeSecondPair');
    if (isChecked2 === 'unchecked') {
        pair2Checkbox.checked = false;
    }

    // Fetch the locations.json file
    fetch('/static/locations.json')
        .then(response => response.json())
        .then(data => {
            // Clear existing dropdown options
            dropdown1.innerHTML = "";
            dropdown2.innerHTML = "";

            // Create a default placeholder option for dropdown1
            let placeholderOption1 = document.createElement("option");
            placeholderOption1.value = ""; // Empty value for placeholder
            placeholderOption1.text = "Select a pair";
            dropdown1.appendChild(placeholderOption1);

            // Create a default placeholder option for dropdown2
            let placeholderOption2 = document.createElement("option");
            placeholderOption2.value = ""; // Empty value for placeholder
            placeholderOption2.text = "Select a pair";
            dropdown2.appendChild(placeholderOption2);

            // Loop through each item in the data
            for (let i = 0; i < data.length; i++) {
                let locationPair = data[i];

                // Create a new option for the dropdown
                let option1 = document.createElement("option");
                option1.value = i;  // Store the index as the option's value
                option1.text = locationPair.name;

                // Create a new option for the second dropdown
                let option2 = document.createElement("option");
                option2.value = i;  // Store the index as the option's value
                option2.text = locationPair.name;

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

            // Enable the checkboxes and dropdowns now that the data has been loaded
            pair1Checkbox.disabled = false;
            pair2Checkbox.disabled = false;
            dropdown1.disabled = false;
            dropdown2.disabled = false;

            // Hide the spinner
            spinner.style.display = "none";
        })
        .catch(error => console.error('Error:', error));

    pair1Checkbox.addEventListener('change', function() {
        var inputs = firstPair.querySelectorAll('input');
        if (this.checked) {
            // Enable all inputs
            inputs.forEach(function(input) {
                input.disabled = false;
            });
        } else {
            // Disable all inputs except the checkbox itself
            inputs.forEach(function(input) {
                if (input.id !== 'pair1Checkbox') {
                    input.disabled = true;
                    input.value = '';
                }
            });
        }
    });
    
    pair2Checkbox.addEventListener('change', function() {
        var inputs = secondPair.querySelectorAll('input');
        if (this.checked) {
            // Enable all inputs
            inputs.forEach(function(input) {
                input.disabled = false;
            });
        } else {
            // Disable all inputs except the checkbox itself
            inputs.forEach(function(input) {
                if (input.id !== 'pair2Checkbox') {
                    input.disabled = true;
                    input.value = '';
                }
            });
        }
    });

});
