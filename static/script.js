document.getElementById('toggleSecondPair').addEventListener('change', function() {
    document.getElementById('secondPair').hidden = !this.checked;
});

table {
    width: 100%;
    margin-bottom: 20px;
}

table th, table td {
    padding: 10px;
    text-align: left;
}
