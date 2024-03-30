$(document).ready(function () {
    // Hide elements when the page is loaded
    $('.image-section').hide();
    $('.image-after').hide();
    $('.loader').hide();
    $('#result').hide();

    // Function to read the URL of the image and preview before upload
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Handle event when the upload file changes
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Handle event when the "Predict" button is clicked
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Hide the Predict button and show the loader
        $(this).hide();
        $('.loader').show();

        // Make a call to the /predict API
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Hide the loader and show the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data.result);

                // Update the image path
                loadImageSrc(data.image_path);
                $('.image-after').show(); // Show the image section

                console.log('Success!');
                console.log(data.result);
                console.log(data.image_path);
            },
        });
    });

    // Function to update the image path
    function loadImageSrc(src) {
        var imageElement = document.getElementById('imageAfter');
        imageElement.setAttribute('src', src);
    }
});
