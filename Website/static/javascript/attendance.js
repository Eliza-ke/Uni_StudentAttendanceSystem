var presentbtn = document.getElementById("present")
var absentbtn = document.getElementById("absent")
var letterbox = document.getElementById("letterbox")

absentbtn.onclick = function (){
    letterbox.style.display = "block";
}

presentbtn.onclick = function (){
    letterbox.style.display = "none";
}


$(document).ready(function(){
    $("#attendanceForm").submit(function(event){
        event.preventDefault();
        var yearid = $("#yearid").val()
        var period = $("#period").val();
        var statusElement = document.getElementsByName('status')
        var leaveletter = $("#leaveletter").val(); 
        var status;

        for (var i = 0; i < statusElement.length; i++){
            if (statusElement[i].checked) {
                status = statusElement[i].value;
                break; // Exit loop once a checked radio button is found
            }
        }
        $.ajax({
            type: "POST",
            url: "/student/attendance", 
            data: {
                yearid: yearid,
                period: period,
                status: status,
                leaveletter: leaveletter
            },
            success: function (response) {
                console.log("Attendance record successful:", response);
                if (response.success) {
                    showNotification(response.message, "success");
                    document.getElementsByName('form')[0].reset()
                } else {
                    showNotification(response.message, "error");
                }
            },
            error: function (xhr, status, error) {
                console.log("Attendance record failed:", error);
                showNotification('Attendance record failed in server error: ' + error, "error");
            }
        });
    });
});


function showNotification(message, type) {
    var toast = document.createElement("div");
    toast.classList.add("toast");
    if (type === "success") {
        toast.classList.add("success");
    } else if (type === "error") {
        toast.classList.add("error");
    }
    toast.textContent = message;
    var container = document.getElementById("toastContainer"); // Replace "toastContainer" with the ID of your container element
    container.appendChild(toast);

    setTimeout(function() {
        toast.remove();
    }, 2000);
}