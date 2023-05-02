$(document).ready(function() {
    // Initialize the random number generator
    $("#init-btn").click(function() {
        $.ajax({
            url: "/randomNum/init",
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
            url: "/randomNum/shutdown",
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
            url: "/randomNum/generate",
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