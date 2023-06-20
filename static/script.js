document.addEventListener('DOMContentLoaded', function() {
    var spinner = document.getElementById('spinner');
    var firstPair = document.getElementById('firstPair');
    var secondPair = document.getElementById('secondPair');
    var pair1Checkbox = document.getElementById('pair1Checkbox');
    var pair2Checkbox = document.getElementById('pair2Checkbox');
    var dropdown1 = document.getElementById('dropdown1');
    var dropdown2 = document.getElementById('dropdown2');

    spinner.style.display = "none"; // Hide the spinner initially

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

            // Set the first item of each dropdown as the selected item and populate the fields accordingly
            dropdown1.selectedIndex = 1;
            let selectedPair1 = data[0];
            document.getElementById('location1Name').value = selectedPair1.location1.name;
            document.getElementById('latitude1').value = selectedPair1.location1.latitude;
            document.getElementById('longitude1').value = selectedPair1.location1.longitude;
            document.getElementById('location2Name').value = selectedPair1.location2.name;
            document.getElementById('latitude2').value = selectedPair1.location2.latitude;
            document.getElementById('longitude2').value = selectedPair1.location2.longitude;

            dropdown2.selectedIndex = 2;
            let selectedPair2 = data[1];
            document.getElementById('location3Name').value = selectedPair2.location1.name;
            document.getElementById('latitude3').value = selectedPair2.location1.latitude;
            document.getElementById('longitude3').value = selectedPair2.location1.longitude;
            document.getElementById('location4Name').value = selectedPair2.location2.name;
            document.getElementById('latitude4').value = selectedPair2.location2.latitude;
            document.getElementById('longitude4').value = selectedPair2.location2.longitude;

            // Set the checkboxes as checked by default
            pair1Checkbox.checked = true;
            pair2Checkbox.checked = true;
        });
});
