document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially

    // Retrieve checkbox state from local storage and update checkbox state
    var isChecked = localStorage.getItem('includeSecondPair');
    if (isChecked === null) { // First visit
        includeSecondPair.checked = true;
        localStorage.setItem('includeSecondPair', 'checked');
    } else { // Returning visit
        includeSecondPair.checked = (isChecked === 'checked') ? true : false;
    }

    // Apply checkbox state to the visibility of the second pair
    secondPair.style.display = includeSecondPair.checked ? "" : "none";
    var inputs = secondPair.querySelectorAll('input');
    inputs.forEach(function(input) {
        input.disabled = !includeSecondPair.checked;
    });

    includeSecondPair.addEventListener('change', function() {
        if (this.checked) {
            // Show second pair and enable all inputs
            secondPair.style.display = "";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.disabled = false;
            });
            // Save checkbox state
            localStorage.setItem('includeSecondPair', 'checked');
        } else {
            // Hide second pair and disable all inputs
            secondPair.style.display = "none";
            var inputs = secondPair.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.disabled = true;
            });
            // Save checkbox state
            localStorage.setItem('includeSecondPair', '');
        }
    });

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
