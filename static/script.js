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
    } else {
        // Disable all inputs in second pair
        inputs.forEach(function(input) {
            input.disabled = true;
        });
    }
});

// Trigger the change event at page load to apply correct state
document.getElementById('includeSecondPair').dispatchEvent(new Event('change'));
