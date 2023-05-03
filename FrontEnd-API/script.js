$(document).ready(function() {
    baseUrl = "http://localhost:5000/trng"
    // Initialize the random number generator
    $("#init-btn").click(function() {
        $.ajax({
            url: baseUrl + "/randomNum/init",
            headers: { 'Access-Control-Allow-Origin': '*'},
            type: "GET",
            success: function(response) {
                if (response === "ok") {
                    $("#init-status").text("Initialized");
                } else {
                    $("#init-status").text("Failed to initialize");
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $("#init-status").text("Error: " + errorThrown);
            }
        });
    });

    // Shutdown the random number generator
    $("#shutdown-btn").click(function() {
        $.ajax({
            url: baseUrl + "/randomNum/shutdown",
            type: "GET",
            success: function(response) {
                if (response === "ok") {
                    $("#init-status").text("Standby mode");
                } else {
                    $("#init-status").text("Failed to shutdown");
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $("#init-status").text("Error: " + errorThrown);
            }
        });
    });

    // Generate random numbers
    $("#generate-btn").click(function() {
        var quantity = $("#quantity-input").val();
        var numBits = $("#numBits-input").val();
        $.ajax({
            url: baseUrl + "/randomNum/generate",
            type: "GET",
            dataType: "json",
            data: {
                quantity: quantity,
                numBits: numBits
            },
            success: function(response) {
                $("#result").text(JSON.stringify(response));
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $("#result").text("Error: " + errorThrown);
            }
        });
    });
});