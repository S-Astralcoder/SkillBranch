// @ts-nocheck
import {
    getAuthorizationHeaders,
    redirectIfUnauthenticated
} from "../shared/auth.js"
import { API_BASE_URL, PAGE_URLS } from "../shared/config.js"
import { activateLogout, activatetoggleAlert, initializeDashboardMenus, initializeDialog } from "../shared/dashboard.js"
import { element } from "../shared/create_element.js"
import { redirectOnExpiration } from "../shared/auth.js"


// Responsible for loading skills
async function fetchSkills() {
    const response = await fetch(`${API_BASE_URL}/skill/skills`, {
        headers: getAuthorizationHeaders()
    })

    if (redirectOnExpiration(response.status)) {        
        return
    }

    if (response.ok) {
        const data = await response.json()
        renderSkills(data)
    }
}

async function renderSkills(skillData) {
    const skill_container = document.querySelector("#skill-container")
    skill_container.replaceChildren()
    for (const data of skillData){
        const skill_box = element("section", {classlist: ["skill-box"], children:
            [
                element("div", {classlist: ["skill-info"], children:
                    [
                        element("a", {classlist: ["skill-name"], text: data.skill_name}),
                        element("p", {classlist: ["skill-description"], text: data.description})
                    ]}),
                element("div", {classlist: ["skill-data"], children:
                    [
                        element("p", {classlist: ["skill-date"], children: [
                            element("span", {text: `created at: ${new Date(data.created_at).toDateString()}`}),
                            element("br"),
                            element("span", {text: `updated at: ${new Date(data.updated_at).toDateString()}`})
                        ]})
                    ]}),
                element("a", {classlist:["skill-id"], text:data.id})
            ]})
        if (skill_container instanceof HTMLElement){
            skill_container.appendChild(skill_box)
        }
    }
    initializeSkillSelection()
}




function initializeSkillSelection(){
    const skill_boxes = document.querySelectorAll(".skill-box")
    for (const skill of skill_boxes){
        skill.addEventListener("click", (event) => {
            sessionStorage.setItem("skill_id", event.currentTarget.querySelector(".skill-id").textContent)
            window.location.href = PAGE_URLS.project_dashboard
        })
    }
}



initializeDashboardMenus()
initializeDialog("#new-skill", "#skill-dialog")
redirectIfUnauthenticated()
fetchSkills()
activateLogout()
activatetoggleAlert()