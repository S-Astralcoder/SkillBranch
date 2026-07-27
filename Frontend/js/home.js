function toggle_side_menu(){
    const side_menu = document.querySelector("#side-menu")
    if (side_menu){
        let ishidden = getComputedStyle(side_menu).display === "none"

        side_menu.style.display = ishidden ? "flex" : "none"
    }
    else{
        console.error("Error occurred while accessing the sidemenu")
    }
}

const menu_btn = document.querySelector(".mob-nav-btn")
if (menu_btn){
    menu_btn.addEventListener("click", toggle_side_menu)
} 
else{
    console.error("Error occurred while accessing the nav-button")
}


function handle_resize() {
    if (window.innerWidth >= 600){
        let side_menu = document.querySelector("#side-menu")
        if (side_menu){
            side_menu.style.display = "none"
        }
        else{
            console.error("Error occurred while accessing the sidemenu")
        }
    }
}

window.addEventListener("resize", handle_resize)
