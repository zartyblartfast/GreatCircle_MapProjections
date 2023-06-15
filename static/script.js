document.getElementById('locationsForm').addEventListener('submit', function() {
    // Disable the submit button
    this.querySelector('[type="submit"]').disabled = true;
});

document.getElementById('toggleSecondPair').addEventListener('click', function() {
    var secondPair = document.getElementById('secondPair');
    if (secondPair.hidden) {
        secondPair.hidden = false;
    } else {
        secondPair.hidden = true;
    }
});
