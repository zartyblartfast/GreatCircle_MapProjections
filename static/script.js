window.addEventListener('load', function() {
    var spinner = document.getElementById('spinner');
    spinner.style.display = "none"; // Hide the spinner initially

    var secondPair = document.getElementById('secondPair');
    var includeSecondPair = document.getElementById('includeSecondPair');

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
        if(!includeSecondPair.checked) {
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

    // Retrieve checkbox state and trigger the change event at page load to apply correct state
    var isChecked = localStorage.getItem('includeSecondPair');
    if(isChecked === null) {
        // If no value is found in local storage, default to checked
        includeSecondPair.checked = true;
        secondPair.style.display = "";
        var inputs = secondPair.querySelectorAll('input');
        inputs.forEach(function(input) {
            input.disabled = false;
        });
        localStorage.setItem('includeSecondPair', 'checked');
    } else {
        includeSecondPair.checked = (isChecked === 'checked') ? true : false;
        includeSecondPair.dispatchEvent(new Event('change'));
    }
});
