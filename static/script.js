document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially
    includeSecondPair.checked = true; // Check the checkbox initially

    // Always show the second pair on the initial load
    secondPair.style.display = "table";

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent page reload on form submit
        spinner.style.display = 'inline';

        // Hide second pair if the checkbox is not checked
        if (!includeSecondPair.checked) {
            secondPair.style.display = 'none';
        }

        // TODO: Add logic to send a request to the server to generate maps
    });

    includeSecondPair.addEventListener('change', function() {
        if (this.checked) {
            // Show second pair and enable all inputs
            secondPair.style.display = "table";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.disabled = false;
            });
        } else {
            // Hide second pair and disable all inputs
            secondPair.style.display = "none";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input)
