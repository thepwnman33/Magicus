$(document).ready(function() {
    $("#searchForm").submit(function(event) {
        event.preventDefault();

        const searchValue = $("#search").val();

        $.ajax({
            url: "http://localhost:5000/search",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "name": searchValue,
                "description": searchValue,
                "code": searchValue
            }),
            success: function(data) {
                console.log("Received data:", data); // Debugging: log the received data

                const results = data.map(function(result) {
                    return `<div>
                        <h2>${result.name}</h2>
                        <p>${result.description}</p>
                        <p><strong>File Path:</strong> ${result.file_path}</p>
                        <p><strong>Latest Commit:</strong> ${result.latest_commit}</p>
                        <pre>${result.code}</pre>
                    </div>`;
                });

                console.log("Generated HTML:", results.join("")); // Debugging: log the generated HTML

                $("#results").html(results.join(""));
            },
            error: function() {
                alert("An error occurred while searching.");
            }
        });
    });
});
