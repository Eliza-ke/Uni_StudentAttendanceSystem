// add data
$("#periodForm").submit(function (event) {
    event.preventDefault();
    var period_name = $("#period_name").val(); 
    var period_time = $("#period_time").val(); 
    $.ajax({
      type: "POST",
      url: "/adminperiodInfo",
      data: {
        period_name: period_name,
        period_time: period_time,
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

  function updateDataPeriod(element) {
    let idvalue = element.getAttribute("data-id-value");
    let periodName = element
      .closest("tr")
      .querySelector("td:first-child").textContent;
  
    let periodTime = element
      .closest("tr")
      .querySelector("td:nth-child(2)").textContent;
  
    // to update get value firstly
    $("#updatePeriodName").val(periodName);
    $("#updatePeriodTime").val(periodTime);
    document.getElementById("myModalPeriod").style.display = "block";
  
    $("#myModalPeriod .close5").click(function () {
        document.getElementById("myModalPeriod").style.display = "none";
    });
  
    // data is modified sent to backend
    $("#updatePeriodForm").submit(function (event) {
      event.preventDefault();
  
      var periodName = $("#updatePeriodName").val();
      var periodTime = $("#updatePeriodTime").val();
      $.ajax({
        type: "POST",
        url: "/updateperiodInfo/" + idvalue,
        data: {
          periodName: periodName,
          periodTime: periodTime,
        },
        success: function (response) {
          console.log("updated successfully: ", response);
          if (response.success) {
            window.location.href = response.redirect;
          } else if (response.fail) {
            alert("update failed: " + response.message);
          } else {
            window.location.href = "/adminperiodInfo";
          }
        },
        error: function (xhr, status, error) {
          console.log("Update failed in ajax function" + error);
        },
      });
    });
  }
  
  function deleteperiodAlert(periodId){

    if (confirm("Warning !!!\nIf you delete this period, all associated attendance will be deleted. ")) {
      window.location.href = "/deleteperiodInfo/"+ periodId;
    }  
  }