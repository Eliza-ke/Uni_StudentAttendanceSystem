var modaladminprofile = document.getElementById("myModalAdminProfile");
var btn = document.getElementById("myBtnAdminProfile");
var closebtn = document.getElementsByClassName("close6")[0];

btn.onclick = function() {
  modaladminprofile.style.display = "block";
}

closebtn.onclick = function() {
  modaladminprofile.style.display = "none";
}

$(document).ready(function(){
      $("#updateAdminProfileForm").submit(function(event){
          event.preventDefault();
          var email = $("#email").val();
          var name = $("#name").val();
          var phone = $("#phone").val();

          $.ajax({
              type: "POST",
              url: "/updateAdminProfile", 
              data: {
                  email: email,
                  name: name,
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
