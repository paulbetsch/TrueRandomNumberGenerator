/* The code $(document).ready(function () {}) is from jQuery and is executed when the DOM ist complety loaded */
function copyToClipboard(value) {
  var textarea = document.createElement("textarea");
  textarea.value = value;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);

  var button = event.target;
  button.style.backgroundColor = "grey"; 
  setTimeout(function() {
    button.style.backgroundColor = ""; 
  }, 1200);
}

function printToTable(response) {
  console.log(response);
  var table = document.getElementById("result");
  table.style.display = "inline-block";
  for (var i = 0; i < response.length; i++) {
    var newRow = document.createElement("tr");
    var cell1 = document.createElement("td");
    cell1.textContent = (i + 1) + ".";
    var cell2 = document.createElement("td");
    var value = response[i];
    cell2.innerHTML = value;
    cell2.id = "trdata";
    var cell3 = document.createElement("td");
    var button = document.createElement("button");
    button.textContent = "COPY";
    button.addEventListener("click", function () {
      copyToClipboard(value);
    });
    cell3.appendChild(button);
    newRow.appendChild(cell1);
    newRow.appendChild(cell3);
    newRow.appendChild(cell2);
    table.appendChild(newRow);
  }
}



$(document).ready(function () {
  baseUrl = "http://127.0.0.1:5520";
  // Sending a request to the API to initialize the random number generator when the button with the ID 'init-btn' is clicked
  $("#init-btn").click(function () {
    var table = document.getElementById("result");
    var tableRows = table.getElementsByTagName("tr");
    table.style.display = "none"
    for (var i = tableRows.length - 1; i > 0; i--) {
      tableRows[i].remove();
    }
    document.getElementById("error").innerText = "";

    $.ajax({
      url: baseUrl + "/randomNum/init",
      type: "GET",
      success: function () {
        $("#init-status").text("Initialized.");
      },
      error: function (response) {
        document.getElementById("error").innerText = response.responseJSON.description;

      },
    });
  });

  // Sending a request to the API to shutdown the random number generator when the button with the ID 'shutdown-btn' is clicked
  $("#shutdown-btn").click(function () {
    var table = document.getElementById("result");
    var tableRows = table.getElementsByTagName("tr");
    table.style.display = "none"
    for (var i = tableRows.length - 1; i > 0; i--) {
      tableRows[i].remove();
    }
    document.getElementById("error").innerText = "";
    $.ajax({
      url: baseUrl + "/randomNum/shutdown",
      type: "GET",
      success: function () {
        $("#init-status").text("Standby mode.");
      },
      error: function (response) {
        document.getElementById("error").innerText = response.responseJSON.description;

      },
    });
  });

  // Sending a request to the API to generate random numbers when the button with the ID 'generate-btn' is clicked
  $("#generate-btn").click(function () {
    var table = document.getElementById("result");
    var tableRows = table.getElementsByTagName("tr");
    table.style.display = "none"
    for (var i = tableRows.length - 1; i > 0; i--) {
      tableRows[i].remove();
    }
    document.getElementById("error").innerText = "";
    var quantity = $("#quantity-input").val();
    var numBits = $("#numBits-input").val();
    // ToDo: Add check for initialized
    if (!quantity.match(/^[1-9]\d*/) || !numBits.match(/^[1-9]\d*/)) {
      document.getElementById("error").innerText = "Please only enter numeric characters (Allowed input:1-9)";
    }
    else {
      // Change back to initialized 
      if (document.getElementById("init-status").textContent === "Initialized.") {
        document.getElementById("statustime").innerText = "Estimated time to wait: " + (Math.floor((quantity * numBits) / 75 / 60) + 1) + " minutes";
        var loaders = document.getElementsByClassName("loader");
        document.getElementById("snow-container").style.display = "flex"
        if (loaders.length > 0) {
          loaders[0].style.display = "inline-block";
        }
        $.ajax({
          url: baseUrl + "/randomNum/getRandom",
          type: "GET",
          dataType: "json",
          data: {
            quantity: quantity,
            numBits: numBits,
          },
          success: function (response) {
            loaders[0].style.display = "none";
            document.getElementById("snow-container").style.display = "none"
            document.getElementById("statustime").innerText = "";
            if (response.status === "Success") {
              console.log(response)
              printToTable(response.result);
            }
          },
          error: function (response) {
            document.getElementById("error").innerText = response.responseJSON.description;

          },
        });

      } else { document.getElementById("error").innerText = "Initialize TRNG before generating"; }
    }
  });
});
