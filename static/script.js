document.getElementById('locationsForm').addEventListener('submit', function() {
    // Disable the submit button
    this.querySelector('[type="submit"]').disabled = true;
});

document.getElementById('includeSecondPair').addEventListener('change', function() {
    var secondPair = document.getElementById('secondPair');
    var inputs = secondPair.querySelectorAll('input');
    if (this.checked) {
        // Enable all inputs in second pair
        inputs.forEach(function(input) {
            input.disabled = false;
        });
        // Save checkbox state
        localStorage.setItem('includeSecondPair', 'checked');
    } else {
        // Disable all inputs in second pair
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
};
