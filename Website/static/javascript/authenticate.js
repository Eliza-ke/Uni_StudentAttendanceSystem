// student register modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var closebtn = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

closebtn.onclick = function() {
  modal.style.display = "none";
}

// student login modal
var modal2 = document.getElementById("myModal2");
var btnlogin = document.getElementById("myBtnLogin");
var closebtnlogin = document.getElementsByClassName("close2")[0];

btnlogin.onclick = function() {
  modal2.style.display = "block";
}

closebtnlogin.onclick = function() {
  modal2.style.display = "none";
}

// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
//   if (event.target == modal2) {
//     modal2.style.display = "none";
//   }
// }

$(document).ready(function(){
  // register
    $("#registerForm").submit(function(event){
        event.preventDefault();
        var email = $("#email").val();
        var name = $("#name").val();
        var year = $("#year").val();
        var batch = $("#batch").val();
        var phone = $("#phone").val();
        var password1 = $("#password1").val();
        var password2 = $("#password2").val();

        $.ajax({
            type: "POST",
            url: "/student/register", 
            data: {
                email: email,
                name: name,
                year: year,
                batch: batch,
                phone: phone,
                password1: password1,
                password2: password2,
            },
            success: function (response) {
                console.log("registration successful: ", response);
                if (response.success){
                  window.location.href = response.redirect;
                }else{
                  alert('registration failed: '+response.message)
                }
              },
              error: function (xhr, status, error) {
                console.log("Registration failed in ajax function"+ error);
            }
        });
    });

// student login
$("#loginForm").submit(function(event){
  event.preventDefault();
  var emailogin = $("#emailogin").val();
  var passwordlogin = $("#passwordlogin").val();

  $.ajax({
      type: "POST",
      url: "/student/login", 
      data: {
          emailogin: emailogin,
          passwordlogin: passwordlogin,
      },
      success: function (response) {
          console.log("Login successful:", response);
          if (response.success) {
              window.location.href = response.redirect; // Redirect to the attendance page
          } else {
            alert('Login failed: ' + response.message);
          }
      },
      error: function (xhr, status, error) {
          console.error("Login failed:", error);
          alert('Login failed: ' + error);
      }
  });
});
});
