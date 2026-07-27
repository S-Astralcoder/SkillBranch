function toggle_menu(menu_id){
    const menu = document.querySelector(`#${menu_id}`)
    if (menu){
        let ishidden = getComputedStyle(menu).display === "none"

        menu.style.display = ishidden ? "flex" : "none"
    }
    else{
        console.error("Error occurred while accessing the sidemenu")
    }
}


const option_btn = document.querySelector("#options-btn")
const filter_btn = document.querySelector("#filter-btn") 

if(!option_btn || !filter_btn){
    console.error("Error occurred while accessing the buttons")
}

option_btn.addEventListener("click", () => {toggle_menu("user-options")})
filter_btn.addEventListener("click", () => {toggle_menu("filter-options")})


