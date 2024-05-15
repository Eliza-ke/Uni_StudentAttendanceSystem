// create
$("#yearForm").submit(function (event) {
  event.preventDefault();
  var year = $("#newYear").val(); 
  $.ajax({
    type: "POST",
    url: "/adminyearInfo",
    data: {
      year: year,
    },
    success: function (response) {
      console.log("successful: ", response);
      if (response.success) {
        window.location.href = response.redirect;
      } else {
        showNotification(response.message, "error");
      }
    },
    error: function (xhr, status, error) {
      console.log("failed in ajax function" + error);
    },
  });
});

// update data
function updateData(element) {
  let idvalue = element.getAttribute("data-id-value");
  let yearName = element
    .closest("tr")
    .querySelector("td:first-child").textContent;

  // to update get value firstly
  $("#updateYear").val(yearName);
  document.getElementById("myModalYear").style.display = "block";

  $("#myModalYear .close4").click(function () {
    document.getElementById("myModalYear").style.display = "none";
  });

  // data is modified sent to backend
  $("#updateYearForm").submit(function (event) {
    event.preventDefault();

    var yearName = $("#updateYear").val();
    $.ajax({
      type: "POST",
      url: "/updateyearInfo/" + idvalue,
      data: {
        year: yearName,
      },
      success: function (response) {
        console.log("updated successfully: ", response);
        if (response.success) {
          window.location.href = response.redirect;
        } else if (response.fail) {
          alert("update failed: " + response.message);
        } else {
          window.location.href = "/adminyearInfo";
        }
      },
      error: function (xhr, status, error) {
        console.log("Update failed in ajax function" + error);
      },
    });
  });
}

function deleteAlert(yearId){

  if (confirm("Warning !!! \nIf you delete this class, all associated students and attendance will be deleted. ")) {
    window.location.href = "/deleteyearInfo/"+ yearId;
  }  
}