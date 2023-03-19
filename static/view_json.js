$(document).ready(function() {
    $.ajax({
        url: "http://localhost:5000/get_all_files",
        method: "GET",
        success: function(data) {
            console.log("Received data:", data);

            let formattedData = JSON.stringify(data, null, 2);
            formattedData = formattedData.replace(/\\n/g, "\n"); // Replace newline escape sequences with actual newlines

            $("#jsonOutput").text(formattedData);
        },
        error: function() {
            alert("An error occurred while fetching the JSON data.");
        }
    });
});
