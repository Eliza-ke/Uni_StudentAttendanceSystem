function ToggleNav() {
  var togglenav = document.getElementById("mySidenav");
  if (togglenav.style.width === "210px") {
    closeNav();
  } else {
    openNav();
  }
}
function openNav() {
  document.getElementById("mySidenav").style.width = "210px";
  document.getElementById("main").style.marginLeft = "210px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

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

  setTimeout(function () {
    toast.remove();
  }, 2000);
}
