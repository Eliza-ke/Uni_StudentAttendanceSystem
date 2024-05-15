var modalprofile = document.getElementById("myModalProfile");
var btn = document.getElementById("myBtnProfile");
var closebtn = document.getElementsByClassName("close3")[0];

btn.onclick = function() {
  modalprofile.style.display = "block";
}

closebtn.onclick = function() {
  modalprofile.style.display = "none";
}

$(document).ready(function(){
      $("#updateProfileForm").submit(function(event){
          event.preventDefault();
          var email = $("#email").val();
          var name = $("#name").val();
          var year = $("#year").val();
          var batch = $("#batch").val();
          var phone = $("#phone").val();

          $.ajax({
              type: "POST",
              url: "/student/updateprofile", 
              data: {
                  email: email,
                  name: name,
                  year: year,
                  batch: batch,
                  phone: phone,
              },
            success: function (response) {
                  console.log("updated successful: ", response);
                  if (response.success){
                    window.location.href = response.redirect;
                  }else{
                    alert('update failed: '+response.message)
                  }
                },
            error: function (xhr, status, error) {
                  console.log("Update failed in ajax function"+ error);
              }
          });
      });
 });
