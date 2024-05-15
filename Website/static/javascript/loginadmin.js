$(document).ready(function(){
$("#loginForm").submit(function(event){
    event.preventDefault();
    var emailogin = $("#email").val();
    var passwordlogin = $("#password").val();
    console.log(emailogin)
    console.log(passwordlogin)
    $.ajax({
        type: "POST",
        url: "/adminlogin", 
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