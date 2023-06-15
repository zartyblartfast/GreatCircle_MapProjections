window.addEventListener('load', function() {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially

    // Always show the second pair on the initial load
    secondPair.style.display = "";

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
        if(!includeSecondPair.checked) {
            secondPair.style.display = 'none';
        }
    });

    includeSecondPair.addEventListener('change', function() {
        if (this.checked) {
            // Show second pair and enable all inputs
