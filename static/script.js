document.addEventListener('DOMContentLoaded', (event) => {
    var spinner = document.getElementById('spinner');
    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    spinner.style.display = "none"; // Hide the spinner initially

    // Set the initial checkbox and second pair states.
    var isChecked = localStorage.getItem('includeSecondPair');
    if (isChecked === null) { // First visit
        includeSecondPair.checked = true;
        localStorage.setItem('includeSecondPair', 'checked');
    } else { // Returning visit
        includeSecondPair.checked = isChecked === 'checked';
    }
    updateSecondPairState();

    // When checkbox state changes, update the second pair state.
    includeSecondPair.addEventListener('change', function() {
        localStorage.setItem('includeSecondPair', this.checked ? 'checked' : '');
        updateSecondPairState();
    });

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
    });

