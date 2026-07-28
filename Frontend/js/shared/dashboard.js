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
