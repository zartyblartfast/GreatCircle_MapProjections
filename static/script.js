document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially

    // Always show the second pair and check the checkbox on initial load
    secondPair.style.display = "";
    includeSecondPair.checked = true;

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

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
    });
});
