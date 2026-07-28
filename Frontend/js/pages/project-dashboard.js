import { getAuthorizationHeaders, redirectIfUnauthenticated } from "../shared/auth.js"
import { activateLogout, initializeDashboardMenus, initializeDialog } from "../shared/dashboard.js"
import { API_BASE_URL } from "../shared/config.js"
import { PAGE_URLS } from "../shared/config.js"
import { redirectOnExpiration } from "../shared/auth.js"
import { element } from "../shared/create_element.js"
initializeDashboardMenus()
initializeDialog("#create-project", "#project-dialog")
redirectIfUnauthenticated()

const skill_id = sessionStorage.getItem("skill_id")

function updateSkillCard(skill_data){
    const skill_name = document.querySelector("#skill-name")
    const skill_description = document.querySelector("#skill-description")
    const skill_id = document.querySelector("#skill-id")
    const skill_created_at = document.querySelector("#skill-created_at")
    const skill_updated_at = document.querySelector("#skill-updated_at")
    if (skill_name && skill_description && skill_id && skill_created_at && skill_updated_at){
        skill_name.textContent = skill_data.skill_name
        skill_description.textContent = skill_data.description
        skill_id.textContent = skill_data.id
        skill_created_at.textContent = skill_data.created_at
        skill_updated_at.textContent = skill_data.updated_at
    }
}


function renderProjects(project_data){
    const project_container = document.querySelector("#project-container")
    if (!(project_container instanceof HTMLElement)){
        return
    }
    project_container.replaceChildren()
    for (const project of project_data){
        // @ts-ignore
        const project_box = element("section", {classlist: ["project-box"], children: [
            // @ts-ignore
            element("div", {classlist: ["project-info"], children: [
                // @ts-ignore
                element("a", {
                    // @ts-ignore
                    classlist: ["project-name"],
                    text: project.project_name
                }),
                // @ts-ignore
                element("p", {classlist: ["project-description"], text: project.description})
            ]}),
            // @ts-ignore
            element("div", {classlist: ["project-data"], children: [
                // @ts-ignore
                element("p", {classlist: ["project-date"], children: [
                    // @ts-ignore
                    element("span", {text: `Created At: ${new Date(project.created_at).toDateString()}`}),
                    // @ts-ignore
                    element("br"),
                    // @ts-ignore
                    element("span", {text: `Updated At: ${new Date(project.updated_at).toDateString()}`})
                ]})
            ]}),
            // @ts-ignore
            element("a", {
                // @ts-ignore
                classlist: ["project-id"],
                text: project.id
            })
        ]})
        // @ts-ignore
        project_container.appendChild(project_box)
    }
}

async function loadProjects(){
    const response = await fetch(`${API_BASE_URL}/project/projects/${skill_id}`, {headers: getAuthorizationHeaders()})
    if (response.ok){
        const data = await response.json()
        renderProjects(data)
        initializeProjectSelection()
    }
}


function initializeProjectSelection(){
    const project_boxes = document.querySelectorAll(".project-box")
    for (const project of project_boxes){
        project.addEventListener("click", (event) => {
            // @ts-ignore
            sessionStorage.setItem("project_id", event.currentTarget.querySelector(".project-id").textContent)
            window.location.href = PAGE_URLS.task_dashboard
        })
    }
}


async function renderProjectPage() {
    if (skill_id === null){
        window.location.replace(PAGE_URLS.dashboard)
    }
    const response = await fetch(`${API_BASE_URL}/skill/skill/${skill_id}`, {
        headers: getAuthorizationHeaders()
    })
    if (redirectOnExpiration(response.status)) {        
        return
    }
    if (response.ok){
        const skill_data = await response.json()
        updateSkillCard(skill_data)
        loadProjects()
        
    }    
}



renderProjectPage()
activateLogout()
