window.addEventListener('load', function() {
    var spinner = document.getElementById('spinner');
    spinner.style.display = "none"; // Hide the spinner initially

    document.getElementById('locationsForm').addEventListener('submit', function(e) {
        spinner.style.display = 'inline';
        if(!document.getElementById('includeSecondPair').checked) {
            document.getElementById('secondPair').style.display = 'none';
        }
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
    var isChecked = localStorage.getItem('includeSecondPair');
    var checkbox = document.getElementById('includeSecondPair');
    checkbox.checked = (isChecked === 'checked') ? true : false;
    checkbox.dispatchEvent(new Event('change'));
});
