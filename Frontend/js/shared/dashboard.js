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

    button.addEventListener("click", () => {
        const errorFeedback = dialog.querySelector(".dialog-error")
        if (errorFeedback) {
            errorFeedback.textContent = ""
        }
        dialog.showModal()
    })
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
    if (!(dialog_box instanceof HTMLDialogElement)){
        console.error(`Failed to get dialog data: ${dialog_id}`)
        return null
    }

    const name_input = dialog_box.querySelector("#name")
    const description_input = dialog_box.querySelector("#description")
    const error_feedback = dialog_box.querySelector(".dialog-error")

    if (!(name_input instanceof HTMLInputElement) ||
        !(description_input instanceof HTMLTextAreaElement)) {
        console.error(`Dialog is missing its name or description field: ${dialog_id}`)
        return null
    }

    const name = name_input.value.trim()
    const description = description_input.value.trim()
    const errors = []

    name_input.setCustomValidity("")
    description_input.setCustomValidity("")

    if (name.length === 0) {
        name_input.setCustomValidity("Name is required.")
        errors.push("Name is required.")
    }
    else if (name.length > 400) {
        name_input.setCustomValidity("Name must be 400 characters or fewer.")
        errors.push("Name must be 400 characters or fewer.")
    }

    if (description.length === 0) {
        description_input.setCustomValidity("Description is required.")
        errors.push("Description is required.")
    }
    else if (description.length > 1000) {
        description_input.setCustomValidity("Description must be 1,000 characters or fewer.")
        errors.push("Description must be 1,000 characters or fewer.")
    }

    const date_input = dialog_box.querySelector("#deadline-date")
    const time_input = dialog_box.querySelector("#deadline-time")

    if (date_input instanceof HTMLInputElement &&
        time_input instanceof HTMLInputElement) {
        date_input.setCustomValidity("")
        time_input.setCustomValidity("")

        if (!date_input.value) {
            date_input.setCustomValidity("Deadline date is required.")
            errors.push("Deadline date is required.")
        }

        if (!time_input.value) {
            time_input.setCustomValidity("Deadline time is required.")
            errors.push("Deadline time is required.")
        }

    }

    if (error_feedback) {
        error_feedback.textContent = errors.join(" ")
    }

    if (errors.length > 0) {
        const first_invalid_input = dialog_box.querySelector(":invalid")
        if (first_invalid_input instanceof HTMLInputElement ||
            first_invalid_input instanceof HTMLTextAreaElement) {
            first_invalid_input.reportValidity()
        }
        return null
    }

    return [name, description]
}
