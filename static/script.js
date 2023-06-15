document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially

    // Always show the second pair on the initial load
    secondPair.style.display = "";

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
        if (!includeSecondPair.checked) {
            secondPair.style.display = 'none';
        }
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

    // Retrieve checkbox state from local storage and update checkbox state
    var isChecked = localStorage.getItem('includeSecondPair');
    includeSecondPair.checked = (isChecked === 'checked') ? true : false;
});
