/* The code $(document).ready(function () {}) is from jQuery and is executed when the DOM ist complety loaded */

$(document).ready(function () {
  baseUrl = "http://localhost:5520/trng";
  // Sending a request to the API to initialize the random number generator when the button with the ID 'init-btn' is clicked
  $("#init-btn").click(function () {
    $.ajax({
      url: baseUrl + "/randomNum/init",
      type: "GET",
      success: function () {
        $("#init-status").text("Initialized.");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        if (jqXHR.status === 403) $("#init-status").text(jqXHR.text + ", " +jqXHR.status);
        else $("#init-status").text(jqXHR.text + ", " +jqXHR.status);
      },
    });
  });

  // Sending a request to the API to shutdown the random number generator when the button with the ID 'shutdown-btn' is clicked
  $("#shutdown-btn").click(function () {
    $.ajax({
      url: baseUrl + "/randomNum/shutdown",
      type: "GET",
      success: function () {
        $("#init-status").text(jqXHR.text + ", " +jqXHR.status);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("#init-status").text(jqXHR.text + ", " +jqXHR.status);
      },
    });
  });

  // Sending a request to the API to generate random numbers when the button with the ID 'generate-btn' is clicked
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
            jqXHR.text + ", " +jqXHR.status
          );
        } else if (jqXHR.status === 432) {
          $("#init-status").text(jqXHR.text + ", " +jqXHR.status);
        } else {
          $("#init-status").text(
            jqXHR.text + ", " +jqXHR.status +", " + errorThrown
          );
        }
      },
    });
  });
});
