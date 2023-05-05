/* The code $(document).ready(function(){}) is used in jQuery and is executed when the DOM ist complety loaded */

$(document).ready(function () {
  baseUrl = "http://localhost:5520/trng";
  // Initialize the random number generator
  $("#init-btn").click(function () {
    // This code is using the jQuery selector "$()" to select the DOM element with the ID "init-btn".
    $.ajax({
      url: baseUrl + "/randomNum/init",
      //headers: { 'Access-Control-Allow-Origin': '*'},
      type: "GET",
      success: function () {
        $("#init-status").text("Initialized.");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        if (jqXHR.status === 403) $("#init-status").text("system already running.");
        else $("#init-status").text("Failed to initialize.");
      },
    });
  });

  // Shutdown the random number generator
  $("#shutdown-btn").click(function () {
    $.ajax({
      url: baseUrl + "/randomNum/shutdown",
      type: "GET",
      success: function () {
        $("#init-status").text("Standby mode.");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("#init-status").text("Failed to shutdown.");
      },
    });
  });

  // Generate random numbers
  $("#generate-btn").click(function () {
    var quantity = $("#quantity-input").val();
    var numBits = $("#numBits-input").val();
    $.ajax({
      url: baseUrl + "/randomNum/getRandom",
      type: "GET",
      dataType: "json",
      data: {
        quantity: quantity,
        numBits: numBits,
      },
      success: function (response) {
        $("#result").text(JSON.stringify(response));
      },
      error: function (jqXHR, textStatus, errorThrown) {
        if (jqXHR.status === 500) {
          $("#init-status").text(
            "System deliverd an empty array; check noise source."
          );
        } else if (jqXHR.status === 432) {
          $("#init-status").text("System not ready; Initalize again.");
        } else {
          $("#init-status").text(
            "API has not been started yet. " + errorThrown
          );
        }
      },
    });
  });
});
