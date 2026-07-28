import { getAuthorizationHeaders, redirectOnExpiration } from "./auth.js"
import { API_BASE_URL, PAGE_URLS } from "./config.js"
import { element } from "./create_element.js"

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

function resolveButton(target) {
    if (target instanceof HTMLButtonElement) {
        return target
    }
    return document.querySelector(target)
}

export function activateEditDelete(
    editTarget,
    deleteTarget,
    entityName,
    editAction,
    deleteAction
) {
    const editButton = resolveButton(editTarget)
    const deleteButton = resolveButton(deleteTarget)

    if (editButton instanceof HTMLButtonElement) {
        editButton.addEventListener("click", async () => {
            if (window.confirm(`Are you sure you want to edit this ${entityName}?`)) {
                await editAction()
            }
        })
    }

    if (deleteButton instanceof HTMLButtonElement) {
        deleteButton.addEventListener("click", async () => {
            if (window.confirm(`Are you sure you want to delete this ${entityName}?`)) {
                await deleteAction()
            }
        })
    }
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

async function findSkillForProject(projectId) {
    const skills_response = await fetch(`${API_BASE_URL}/skill/skills`, {
        headers: getAuthorizationHeaders()
    })
    if (redirectOnExpiration(skills_response.status)) {
        return null
    }
    if (!skills_response.ok) {
        return null
    }

    const skills = await skills_response.json()
    for (const skill of skills) {
        const projects_response = await fetch(
            `${API_BASE_URL}/project/projects/${skill.id}`,
            {headers: getAuthorizationHeaders()}
        )
        if (redirectOnExpiration(projects_response.status)) {
            return null
        }
        if (!projects_response.ok) {
            continue
        }

        const projects = await projects_response.json()
        if (projects.some((project) => project.id === projectId)) {
            return skill.id
        }
    }
    return null
}

async function openUrgentTaskProject(projectId, skillId = null) {
    const owning_skill_id = skillId || await findSkillForProject(projectId)
    if (owning_skill_id === null) {
        window.alert("Unable to find the project for this task.")
        return
    }

    sessionStorage.setItem("skill_id", owning_skill_id)
    sessionStorage.setItem("project_id", projectId)
    window.location.href = PAGE_URLS.task_dashboard
}

export async function loadurgenttasks(){
    const task_container = document.querySelector("#urgent-tasks-container")
    if (!(task_container instanceof HTMLElement)) {
        return
    }

    const response = await fetch(`${API_BASE_URL}/task/near_deadline_tasks`, {
        method: "POST",
        headers: getAuthorizationHeaders()
    })
    if (redirectOnExpiration(response.status)) {
        return
    }
    if (!response.ok) {
        console.error(`Failed to load urgent tasks: ${response.status}`)
        return
    }

    const tasks = await response.json()
    task_container.replaceChildren()

    if (tasks.length === 0) {
        const empty_message = element("p", {text: "No urgent tasks."})
        task_container.appendChild(empty_message)
        return
    }

    for (const task of tasks) {
        const parsed_deadline = new Date(task.deadline)
        const task_name = element("a", {
            text: task.task_name,
            classlist: ["urgent-task-name"]
        })
        const deadline = element("p", {
            text: Number.isNaN(parsed_deadline.getTime())
                ? "Deadline: Invalid deadline"
                : `Deadline: ${parsed_deadline.toLocaleString()}`,
            classlist: ["urgent-deadline-date"]
        })
        const task_id = element("p", {
            text: task.id,
            classlist: ["task-id"],
            attributes: {hidden: ""}
        })
        const project_id = element("p", {
            text: task.project_id,
            classlist: ["urgent-project-id"],
            attributes: {hidden: ""}
        })
        const task_box = element("section", {
            classlist: ["urgent-task-box"],
            attributes: {tabindex: "0", role: "link"},
            children: [task_name, deadline, task_id, project_id]
        })

        task_box.addEventListener("click", () => {
            openUrgentTaskProject(project_id.textContent, task.skill_id)
        })
        task_box.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault()
                openUrgentTaskProject(project_id.textContent, task.skill_id)
            }
        })

        task_container.appendChild(task_box)
    }
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
    let datetime_iso = null

    if (date_input instanceof HTMLInputElement &&
        time_input instanceof HTMLInputElement &&
        !date_input.disabled &&
        !time_input.disabled) {
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

        if (date_input.value && time_input.value) {
            const datetime = new Date(`${date_input.value}T${time_input.value}`)
            if (Number.isNaN(datetime.getTime())) {
                date_input.setCustomValidity("Enter a valid deadline date and time.")
                errors.push("Enter a valid deadline date and time.")
            }
            else {
                datetime_iso = datetime.toISOString()
            }
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

    name_input.value = ""
    description_input.value = ""

    if (datetime_iso !== null) {
        date_input.value = ""
        time_input.value = ""
        dialog_box.close()
        return [name, description, datetime_iso]
    }
    dialog_box.close()
    return [name, description]
}
