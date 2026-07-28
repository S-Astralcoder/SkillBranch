const MOBILE_BREAKPOINT = 600

function getSideMenu() {
    const sideMenu = document.querySelector(".side-menu")

    if (!(sideMenu instanceof HTMLElement)) {
        console.error("Error occurred while accessing the side menu")
        return null
    }

    return sideMenu
}

function toggleSideMenu() {
    const sideMenu = getSideMenu()

    if (sideMenu) {
        const isHidden = getComputedStyle(sideMenu).display === "none"
        sideMenu.style.display = isHidden ? "flex" : "none"
    }
}

function handleResize() {
    if (window.innerWidth >= MOBILE_BREAKPOINT) {
        const sideMenu = getSideMenu()

        if (sideMenu) {
            sideMenu.style.display = "none"
        }
    }
}

export function initializeMobileNavigation() {
    const menuButton = document.querySelector(".mob-nav-btn")

    if (!menuButton) {
        console.error("Error occurred while accessing the navigation button")
        return
    }

    menuButton.addEventListener("click", toggleSideMenu)
    window.addEventListener("resize", handleResize)
}
