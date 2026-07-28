import {
    getAuthorizationHeaders,
    redirectIfUnauthenticated
} from "../shared/auth.js"
import { API_BASE_URL, PAGE_URLS } from "../shared/config.js"
import { initializeDashboardMenus, initializeDialog } from "../shared/dashboard.js"

async function fetchSkills() {
    const response = await fetch(`${API_BASE_URL}/skill/skills`, {
        headers: getAuthorizationHeaders()
    })

    if (response.status === 401) {
        alert("Token Expired, Signin Again")
        window.location.replace(PAGE_URLS.login)
        return
    }

    if (response.ok) {
        const data = await response.json()
        renderSkills(data)
    }
}

function renderSkills(skillData) {
    void skillData
}

initializeDashboardMenus()
initializeDialog("#new-skill", "#skill-dialog")
redirectIfUnauthenticated()
void fetchSkills()
