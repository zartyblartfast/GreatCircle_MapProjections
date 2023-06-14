document.getElementById('toggleSecondPair').addEventListener('click', function() {
    var secondPair = document.getElementById('secondPair');
    if (secondPair.hidden) {
        secondPair.hidden = false;
    } else {
        secondPair.hidden = true;
    }
});
