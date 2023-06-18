document.getElementById('locationsForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from being submitted the traditional way

    spinner.style.display = 'inline';
    // Disable the submit button when the form is submitted
    submitButton.disabled = true;

    // Gather form data
    var formData = new FormData(this);  // 'this' is the form element

    // Send AJAX request
    $.ajax({
        url: '/generate_map',
        method: 'POST',
        data: formData,
        processData: false,  // jQuery should not process the data
        contentType: false,  // jQuery should not set the content type
        success: function(response) {
            // Handle successful response
            if (response.error) {
                // Show error message
                console.error(response.error);
            } else {
                // Update the map images
                img1.src = '/map1/' + response.filename_plate_carree;
                img2.src = '/map2/' + response.filename_azimuthal_equidistant;
            }

            // Enable the submit button
            submitButton.disabled = false;
            spinner.style.display = 'none';
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle error
            console.error('Error:', textStatus, errorThrown);

            // Enable the submit button
            submitButton.disabled = false;
            spinner.style.display = 'none';
        }
    });
});
