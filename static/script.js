var spinner = document.getElementById('spinner');

document.getElementById('locationsForm').addEventListener('submit', function(event) {
    // Disable the submit button
    this.querySelector('[type="submit"]').disabled = true;

    // Show the spinner
    spinner.style.display = "";
});

document.getElementById('includeSecondPair').addEventListener('change', function() {
    var secondPair = document.getElementById('secondPair');
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

// Retrieve checkbox state and trigger the change event at page load to apply correct state
window.onload = function() {
    var isChecked = localStorage.getItem('includeSecondPair');
    var checkbox = document.getElementById('includeSecondPair');
    checkbox.checked = (isChecked === 'checked') ? true : false;
    checkbox.dispatchEvent(new Event('change'));

    // Hide the spinner initially
    spinner.style.display = "none";
};
