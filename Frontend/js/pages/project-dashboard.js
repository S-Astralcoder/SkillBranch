import { getAuthorizationHeaders, redirectIfUnauthenticated } from "../shared/auth.js"
import {
    activateEditDelete,
    activateLogout,
    activatetoggleAlert,
    get_dialog_data,
    initializeDashboardMenus,
    initializeDialog,
    loadurgenttasks
} from "../shared/dashboard.js"
import { API_BASE_URL } from "../shared/config.js"
import { PAGE_URLS } from "../shared/config.js"
import { redirectOnExpiration } from "../shared/auth.js"
import { element } from "../shared/create_element.js"
initializeDashboardMenus()
initializeDialog("#create-project", "#project-dialog")
redirectIfUnauthenticated()

const skill_id = sessionStorage.getItem("skill_id")
let current_skill_data = null
let dialog_mode = "create-project"

async function showRequestError(response, fallback_message){
    let message = fallback_message
    try {
        const data = await response.json()
        message = data.detail || message
    }
    catch {
        // Keep the fallback message when the response has no JSON body.
    }
    window.alert(message)
}

function updateSkillCard(skill_data){
    current_skill_data = skill_data
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

function configureProjectDialog(mode){
    const dialog = document.querySelector("#project-dialog")
    if (!(dialog instanceof HTMLDialogElement)) {
        return
    }
    const name_label = dialog.querySelector("label[for='name']")
    const description_label = dialog.querySelector("label[for='description']")
    const name_input = dialog.querySelector("#name")
    const description_input = dialog.querySelector("#description")
    const submit_button = dialog.querySelector("#submit-btn")
    const error_feedback = dialog.querySelector(".dialog-error")

    if (!(name_input instanceof HTMLInputElement) ||
        !(description_input instanceof HTMLTextAreaElement)) {
        return
    }

    dialog_mode = mode
    if (error_feedback) {
        error_feedback.textContent = ""
    }

    if (mode === "edit-skill" && current_skill_data !== null) {
        name_label.textContent = "Skill Name"
        description_label.textContent = "Skill Description"
        submit_button.textContent = "Update"
        name_input.value = current_skill_data.skill_name
        description_input.value = current_skill_data.description
        return
    }

    name_label.textContent = "Project Name"
    description_label.textContent = "Project Description"
    submit_button.textContent = "Create"
    name_input.value = ""
    description_input.value = ""
}

async function activateProjectDialog(){
    document.querySelector("#create-project")?.addEventListener("click", () => {
        configureProjectDialog("create-project")
    })

    const project_submit = document.querySelector("#project-dialog #submit-btn")
    project_submit?.addEventListener("click", async ()=>{
        const dialog_data = get_dialog_data("#project-dialog")
        if (dialog_data === null) {
            return
        }
        const [name, description] = dialog_data

        if (dialog_mode === "edit-skill") {
            const response = await fetch(`${API_BASE_URL}/skill/update_skill`, {
                method: "PUT",
                headers: getAuthorizationHeaders(),
                body: JSON.stringify({id: skill_id, name, description})
            })
            if (redirectOnExpiration(response.status)) {
                return
            }
            if (response.ok) {
                updateSkillCard(await response.json())
                return
            }
            await showRequestError(response, "Failed to update skill.")
            return
        }

        const response = await fetch(`${API_BASE_URL}/project/create_project`, {
            method: "POST",
            headers: getAuthorizationHeaders(),
            body: JSON.stringify({
                skill_id,
                project_name: name,
                description
            })
        })
        if (redirectOnExpiration(response.status)) {
            return
        }
        if (response.ok) {
            await loadProjects()
            return
        }
        await showRequestError(response, "Failed to create project.")
    })
}

async function editSkill(){
    if (current_skill_data === null) {
        return
    }
    configureProjectDialog("edit-skill")
    const dialog = document.querySelector("#project-dialog")
    if (dialog instanceof HTMLDialogElement) {
        dialog.showModal()
    }
}

async function deleteSkill(){
    const response = await fetch(`${API_BASE_URL}/skill/delete_skill`, {
        method: "PUT",
        headers: getAuthorizationHeaders(),
        body: JSON.stringify({id: skill_id})
    })
    if (redirectOnExpiration(response.status)) {
        return
    }
    if (response.ok) {
        sessionStorage.removeItem("skill_id")
        sessionStorage.removeItem("project_id")
        window.location.replace(PAGE_URLS.dashboard)
        return
    }
    await showRequestError(response, "Failed to delete skill.")
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
activatetoggleAlert()
activateProjectDialog()
activateEditDelete("#skill-edit", "#skill-delete", "skill", editSkill, deleteSkill)
loadurgenttasks()
