console.log("AFRI LIMITED");

//open and close the sidebar

let btn = document.querySelector("#btn");
let searchIcon = document.querySelector("#searchIcon");
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");

//open and close the sidebar
btn.onclick = function () {
  sidebar.classList.toggle("close");
};
sidebarBtn.onclick = function () {
  sidebar.classList.toggle("close");
};
//console.log(sidebarBtn);
//open and close the search bar
searchIcon.onclick = function () {
  sidebar.classList.toggle("close");
};
//console.log(searchIcon);

// end of open and close the sidebar

//selecting main parent of arrow/menu and displaying the submenu
let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;
    arrowParent.classList.toggle("showMenu");
  });
}

//end of selecting main parent of arrow/menu and displaying the submenu
