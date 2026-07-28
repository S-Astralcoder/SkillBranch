import { PAGE_URLS } from "./config.js"

function initializeMenu(buttonSelector, menuSelector) {
    const button = document.querySelector(buttonSelector)
    const menu = document.querySelector(menuSelector)

    if (!button || !(menu instanceof HTMLElement)) {
        console.error(`Failed to initialize dashboard menu: ${menuSelector}`)
        return
    }

    button.addEventListener("click", () => {
        const isHidden = getComputedStyle(menu).display === "none"
        menu.style.display = isHidden ? "flex" : "none"
    })
}

export function initializeDashboardMenus() {
    initializeMenu("#options-btn", "#user-options")
    initializeMenu("#filter-btn", "#filter-options")
}

export function initializeDialog(buttonSelector, dialogSelector) {
    const button = document.querySelector(buttonSelector)
    const dialog = document.querySelector(dialogSelector)

    if (!button || !(dialog instanceof HTMLDialogElement)) {
        console.error(`Failed to initialize dialog: ${dialogSelector}`)
        return
    }

    button.addEventListener("click", () => dialog.showModal())
}

export function activateLogout(){
    const logout = document.querySelector("#log-out")
    logout?.addEventListener("click", ()=>{
        localStorage.removeItem("access_token")
        window.location.replace(PAGE_URLS.home)
    })
}

export function activatetoggleAlert(){
    const toggle_alert = document.querySelector("#toggle-alert")
    toggle_alert?.addEventListener("click", ()=> {
        const side_bar = document.querySelector("#near-deadline-task")
        const main_box = document.querySelector("#home-page-content")
        if(side_bar instanceof HTMLElement && main_box instanceof HTMLElement){
            side_bar.style.display = side_bar.style.display == "flex" ? "none" : "flex"
            
            if (side_bar.style.display == "none"){
                main_box.style.gridTemplateColumns = "1fr"
            }
            else {
                main_box.style.gridTemplateColumns = "1fr 400px"

            }
        }
    })

}

export function get_dialog_data(dialog_id){
    const dialog_box = document.querySelector(dialog_id)
    if (dialog_box instanceof HTMLElement){
        const name = dialog_box.querySelector("#name")?.value.trim()
        const description = dialog_box.querySelector("#description")?.value.trim()
        
    }
}