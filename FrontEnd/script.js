/* The code $(document).ready(function () {}) is from jQuery and is executed when the DOM ist complety loaded */

$(document).ready(function () {


  $("#quantity-input, #numBits-input").on("input", function () {
    this.value = this.value.replace(/[^0-9]/g, "");
    if (this.value < 0) {
      this.value = "";
    }
  });

  baseUrl = "http://localhost:5520/trng";
  // Sending a request to the API to initialize the random number generator when the button with the ID 'init-btn' is clicked
  $("#init-btn").click(function () {
    $.ajax({
      url: baseUrl + "/randomNum/init",
      type: "GET",
      success: function (jqXHR) {
        const json = jqXHR.responseText
        const obj = JSON.parse(json);

        $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        const json = jqXHR.responseText
        const obj = JSON.parse(json);

        if (jqXHR.status === 403) $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
        else $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
      },
    });
  });

  // Sending a request to the API to shutdown the random number generator when the button with the ID 'shutdown-btn' is clicked
  $("#shutdown-btn").click(function () {
    $.ajax({
      url: baseUrl + "/randomNum/shutdown",
      type: "GET",
      success: function () {
        const json = jqXHR.responseText
        const obj = JSON.parse(json);
        $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        const json = jqXHR.responseText
        const obj = JSON.parse(json);
        $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
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
        var formattedJSON = JSON.stringify(response, null, 2); // Hier wird der zusätzliche Parameter `2` verwendet, um den Einzug auf 2 Leerzeichen festzulegen
        formattedJSON = formattedJSON.replace(/\n/g, "<br>"); // Ersetzt Zeilenumbrüche durch HTML-Break-Tags
        $("#result").html(formattedJSON); // Verwendet html() statt text(), um die Zeilenumbrüche zu berücksichtigen
      },
      error: function (jqXHR, textStatus, errorThrown) {
        const json = jqXHR.responseText
        const obj = JSON.parse(json);
        if (jqXHR.status === 500) {
          $("#init-status").text(
            obj.description + ", Status: "+jqXHR.status
          );
        } else if (jqXHR.status === 432) {
          $("#init-status").text(obj.description + ", Status: "+jqXHR.status);
        } else {
          $("#init-status").text(
            obj.description + ", Status: "+jqXHR.status + errorThrown
          );
        }
      },
    });
  });
});
