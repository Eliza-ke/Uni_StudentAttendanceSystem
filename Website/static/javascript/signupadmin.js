var facultybtn = document.getElementById("faculty")
var systemAdminbtn = document.getElementById("system_admin")
var codebox = document.getElementById("codebox")

systemAdminbtn.onclick = function (){
    codebox.style.display = "block";
}

facultybtn.onclick = function (){
    codebox.style.display = "none";
}

$(document).ready(function(){
    // sign up
      $("#signupForm").submit(function(event){
          event.preventDefault();
          var email = $("#email").val();
          var name = $("#name").val();
          var rolecode = $("#rolecode").val();
          var phone = $("#phone").val();
          var password1 = $("#password1").val();
          var password2 = $("#password2").val();
  
          $.ajax({
              type: "POST",
              url: "/adminSignUp", 
              data: {
                  email: email,
                  name: name,
                  rolecode: rolecode,
                  phone: phone,
                  password1: password1,
                  password2: password2,
              },
              success: function (response) {
                  console.log("Sign Up successful: ", response);
                  if (response.success){
                    window.location.href = response.redirect;
                  }else{
                    alert('Sign Up failed: '+response.message)
                  }
                },
                error: function (xhr, status, error) {
                  console.log("Sign Up failed in ajax function"+ error);
              }
          });
      });
    
  });
  