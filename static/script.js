document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var firstPair = document.getElementById('firstPair');
    var secondPair = document.getElementById('secondPair');
    var dropdown1 = document.getElementById('dropdown1');
    var dropdown2 = document.getElementById('dropdown2');
    var submitButton = document.querySelector('button[type="submit"]');
    var img1 = document.getElementById('mapImage1');
    var img2 = document.getElementById('mapImage2');
    var pair1Checkbox = document.getElementById('pair1Checkbox');
    var pair2Checkbox = document.getElementById('pair2Checkbox');

    spinner.style.display = "none"; // Hide the spinner initially

    // Function to handle form and image visibility
    function handleVisibility(checkbox, fieldset) {
        if (!checkbox) {
            console.log('Checkbox not found');
            return;
        }
        if (!fieldset) {
            console.log('Fieldset not found');
            return;
        }
        
        var inputs = fieldset.querySelectorAll('input, select');
        
        if (inputs.length > 0) {
            inputs.forEach(function(input) {
                if (input !== checkbox) {
                    input.disabled = !checkbox.checked;
                }
            });
        }
    }

    // Initial visibility setup
    handleVisibility(pair1Checkbox, firstPair);
    handleVisibility(pair2Checkbox, secondPair);

    // Function to enable or disable the second pair of locations
    function enableSecondPair() {
        pair2Checkbox.disabled = !pair1Checkbox.checked;
        handleVisibility(pair2Checkbox, secondPair);
    }

    // Add event listeners to the checkboxes
    //pair1Checkbox.addEventListener('change', enableSecondPair);
    //pair2Checkbox.addEventListener('change', function() {
    //    handleVisibility(pair2Checkbox, secondPair);
    //});
    pair1Checkbox.addEventListener('change', function() {
        handleVisibility(pair1Checkbox, firstPair);
        enableSecondPair();
    });
    pair2Checkbox.addEventListener('change', function() {
        handleVisibility(pair2Checkbox, secondPair);
    });

    // Fetch the locations.json file
    fetch('/static/locations.json')
        .then(response => response.json())
        .then(data => {
            // Loop through each item in the data
            for (let i = 0; i < data.length; i++) {
                let locationPair = data[i];

                // Create a new option for the dropdown
                let option = document.createElement("option");
                option.value = i;  // Store the index as the option's value
                option.text = locationPair.name;

                // Add the option to both dropdowns
                dropdown1.add(option);
                dropdown2.add(option.cloneNode(true));  // Clone the option for the second dropdown
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
        // Disable the submit button when the form is submitted
        submitButton.disabled = true;
    });

    // Enable the submit button when both images have finished loading
    function enableButton() {
        if (img1.complete && img2.complete) {
            submitButton.disabled = false;
            spinner.style.display = 'none';
        }
    }

    // Add event listeners to the image load events
   if (img1 && img2) {
     img1.addEventListener('load', enableButton);
     img2.addEventListener('load', enableButton);
   }

    // Handle the initial visibility of the second pair of locations based on the first pair's checkbox
    enableSecondPair();
});
