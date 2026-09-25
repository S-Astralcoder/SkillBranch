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
initializeDialog("#create-task", "#task-dialog")
redirectIfUnauthenticated()

const skill_id = sessionStorage.getItem("skill_id")
const project_id = sessionStorage.getItem("project_id")
let current_project_data = null
let dialog_mode = "create-task"
let editing_task = null

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

function updateProjectCard(project_data){
    current_project_data = project_data
    const project_name = document.querySelector("#project-name")
    const project_description = document.querySelector("#project-description")
    const project_id = document.querySelector("#project-id")
    const project_date = document.querySelector("#project-date")
    if (project_name && project_description && project_id && project_date){
        project_name.textContent = project_data.project_name
        project_description.textContent = project_data.description
        project_id.textContent = project_data.id
        // @ts-ignore
        project_date.replaceChildren(
            // @ts-ignore
            element("span", {text: `Created At: ${new Date(project_data.created_at).toDateString()}`}),
            // @ts-ignore
            element("br"),
            // @ts-ignore
            element("span", {text: `Updated At: ${new Date(project_data.updated_at).toDateString()}`})
        )
    }
}

function formatDeadline(deadline){
    const parsed_deadline = new Date(deadline)
    if (Number.isNaN(parsed_deadline.getTime())){
        return "Invalid deadline"
    }
    return parsed_deadline.toLocaleString()
}

function configureTaskDialog(mode, task = null){
    const dialog = document.querySelector("#task-dialog")
    if (!(dialog instanceof HTMLDialogElement)) {
        return
    }
    const name_label = dialog.querySelector("label[for='name']")
    const description_label = dialog.querySelector("label[for='description']")
    const name_input = dialog.querySelector("#name")
    const description_input = dialog.querySelector("#description")
    const deadline_box = dialog.querySelector("#deadline-box")
    const date_input = dialog.querySelector("#deadline-date")
    const time_input = dialog.querySelector("#deadline-time")
    const submit_button = dialog.querySelector("#submit-btn")
    const error_feedback = dialog.querySelector(".dialog-error")

    if (!(name_input instanceof HTMLInputElement) ||
        !(description_input instanceof HTMLTextAreaElement) ||
        !(deadline_box instanceof HTMLElement) ||
        !(date_input instanceof HTMLInputElement) ||
        !(time_input instanceof HTMLInputElement)) {
        return
    }

    dialog_mode = mode
    editing_task = task
    if (error_feedback) {
        error_feedback.textContent = ""
    }

    if (mode === "edit-project" && current_project_data !== null) {
        name_label.textContent = "Project Name"
        description_label.textContent = "Project Description"
        submit_button.textContent = "Update"
        name_input.value = current_project_data.project_name
        description_input.value = current_project_data.description
        deadline_box.style.display = "none"
        date_input.disabled = true
        time_input.disabled = true
        return
    }

    name_label.textContent = "Task Name"
    description_label.textContent = "Task Description"
    submit_button.textContent = mode === "edit-task" ? "Update" : "Add"
    deadline_box.style.display = ""
    date_input.disabled = false
    time_input.disabled = false

    if (mode === "edit-task" && task !== null) {
        const parsed_deadline = new Date(task.deadline)
        const local_deadline = Number.isNaN(parsed_deadline.getTime())
            ? ""
            : new Date(
                parsed_deadline.getTime() -
                parsed_deadline.getTimezoneOffset() * 60000
            ).toISOString().slice(0, 16)
        const [date = "", time = ""] = local_deadline.split("T")

        name_input.value = task.task_name
        description_input.value = task.description
        date_input.value = date
        time_input.value = time
        return
    }

    name_input.value = ""
    description_input.value = ""
    date_input.value = ""
    time_input.value = ""
}

function renderTasks(task_data){
    const task_container = document.querySelector("#task-container")
    if (!(task_container instanceof HTMLElement)){
        return
    }
    task_container.replaceChildren()
    for (const task of task_data){
        const checkbox_attributes = {
            type: "checkbox",
            name: "task-complete",
            "aria-label": `Mark ${task.task_name} as complete`
        }
        if (task.completed === true){
            checkbox_attributes.checked = ""
        }
        // @ts-ignore
        const task_box = element("section", {classlist: ["task-box"], children: [
            // @ts-ignore
            element("div", {classlist: ["task-info"], children: [
                // @ts-ignore
                element("a", {
                    // @ts-ignore
                    classlist: ["task-name"],
                    text: task.task_name
                }),
                // @ts-ignore
                element("p", {classlist: ["task-description"], text: task.description})
            ]}),
            // @ts-ignore
            element("div", {classlist: ["task-data"], children: [
                // @ts-ignore
                element("p", {classlist: ["task-date"], children: [
                    // @ts-ignore
                    element("span", {text: `Created At: ${new Date(task.created_at).toDateString()}`}),
                    // @ts-ignore
                    element("br"),
                    // @ts-ignore
                    element("span", {text: `Deadline: ${formatDeadline(task.deadline)}`})
                ]})
            ]}),
            // @ts-ignore
            element("a", {
                // @ts-ignore
                classlist: ["task-card-id"],
                text: task.id
            }),
            // @ts-ignore
            element("div", {classlist: ["task-options"], children: [
                // @ts-ignore
                element("button", {
                    text: "Edit",
                    classlist: ["task-edit", "option-btn"],
                    attributes: {
                        type: "button",
                        "aria-label": `Edit ${task.task_name}`
                    }
                }),
                // @ts-ignore
                element("button", {
                    text: "Delete",
                    classlist: ["task-delete", "option-btn"],
                    attributes: {
                        type: "button",
                        "aria-label": `Delete ${task.task_name}`
                    }
                })
            ]}),
            // @ts-ignore
            element("input", {classlist: ["task-checkbox"], attributes: checkbox_attributes})
        ]})
        const edit_button = task_box.querySelector(".task-edit")
        const delete_button = task_box.querySelector(".task-delete")
        const checkbox = task_box.querySelector(".task-checkbox")

        activateEditDelete(
            edit_button,
            delete_button,
            "task",
            () => editTask(task),
            () => deleteTask(task.id)
        )
        if (checkbox instanceof HTMLInputElement) {
            checkbox.addEventListener("change", () => toggleTask(task.id, checkbox))
        }
        // @ts-ignore
        task_container.appendChild(task_box)
    }
}

async function loadTasks(){
    const response = await fetch(`${API_BASE_URL}/task/tasks/${skill_id}/${project_id}`, {headers: getAuthorizationHeaders()})
    if (redirectOnExpiration(response.status)){
        return
    }
    if (response.ok){
        const data = await response.json()
        renderTasks(data)
    }
}

async function activateTaskDialog(){
    document.querySelector("#create-task")?.addEventListener("click", () => {
        configureTaskDialog("create-task")
    })

    const task_submit = document.querySelector("#task-dialog #submit-btn")
    task_submit?.addEventListener("click", async ()=>{
        const dialog_data = get_dialog_data("#task-dialog")
        if (dialog_data === null) {
            return
        }

        if (dialog_mode === "edit-project") {
            const [project_name, description] = dialog_data
            const response = await fetch(`${API_BASE_URL}/project/update_project`, {
                method: "PUT",
                headers: getAuthorizationHeaders(),
                body: JSON.stringify({
                    skill_id,
                    project_id,
                    project_name,
                    description
                })
            })
            if (redirectOnExpiration(response.status)) {
                return
            }
            if (response.ok) {
                updateProjectCard(await response.json())
                return
            }
            await showRequestError(response, "Failed to update project.")
            return
        }

        const [task_name, description, deadline] = dialog_data
        if (dialog_mode === "edit-task" && editing_task !== null) {
            const response = await fetch(`${API_BASE_URL}/task/update_task`, {
                method: "PUT",
                headers: getAuthorizationHeaders(),
                body: JSON.stringify({
                    skill_id,
                    project_id,
                    task_id: editing_task.id,
                    task_name,
                    description,
                    deadline
                })
            })
            if (redirectOnExpiration(response.status)) {
                return
            }
            if (response.ok) {
                await loadTasks()
                await loadurgenttasks()
                return
            }
            await showRequestError(response, "Failed to update task.")
            return
        }

        const response = await fetch(`${API_BASE_URL}/task/create_task`, {
            method: "POST",
            headers: getAuthorizationHeaders(),
            body: JSON.stringify({
                skill_id,
                project_id,
                task_name,
                description,
                deadline
            })
        })
        if (redirectOnExpiration(response.status)) {
            return
        }
        if (response.ok) {
            await loadTasks()
            await loadurgenttasks()
            return
        }
        await showRequestError(response, "Failed to create task.")
    })
}

async function editTask(task){
    configureTaskDialog("edit-task", task)
    const dialog = document.querySelector("#task-dialog")
    if (dialog instanceof HTMLDialogElement) {
        dialog.showModal()
    }
}

async function deleteTask(task_id){
    const response = await fetch(`${API_BASE_URL}/task/delete_task`, {
        method: "DELETE",
        headers: getAuthorizationHeaders(),
        body: JSON.stringify({skill_id, project_id, task_id})
    })
    if (redirectOnExpiration(response.status)) {
        return
    }
    if (response.ok) {
        await loadTasks()
        await loadurgenttasks()
        return
    }
    await showRequestError(response, "Failed to delete task.")
}

async function toggleTask(task_id, checkbox){
    const response = await fetch(`${API_BASE_URL}/task/toggle_task`, {
        method: "PATCH",
        headers: getAuthorizationHeaders(),
        body: JSON.stringify({
            skill_id,
            project_id,
            task_id,
            toggle: checkbox.checked
        })
    })
    if (redirectOnExpiration(response.status)) {
        return
    }
    if (response.ok) {
        await loadurgenttasks()
        return
    }
    checkbox.checked = !checkbox.checked
    await showRequestError(response, "Failed to update task completion.")
}

async function editProject(){
    if (current_project_data === null) {
        return
    }
    configureTaskDialog("edit-project")
    const dialog = document.querySelector("#task-dialog")
    if (dialog instanceof HTMLDialogElement) {
        dialog.showModal()
    }
}

async function deleteProject(){
    const response = await fetch(`${API_BASE_URL}/project/delete_project`, {
        method: "DELETE",
        headers: getAuthorizationHeaders(),
        body: JSON.stringify({skill_id, project_id})
    })
    if (redirectOnExpiration(response.status)) {
        return
    }
    if (response.ok) {
        sessionStorage.removeItem("project_id")
        window.location.replace(PAGE_URLS.project_dashboard)
        return
    }
    await showRequestError(response, "Failed to delete project.")
}



async function renderTaskPage() {
    if (skill_id === null){
        window.location.replace(PAGE_URLS.dashboard)
    }
    if (project_id === null){
        window.location.replace(PAGE_URLS.project_dashboard)
    }
    const response = await fetch(`${API_BASE_URL}/project/project/${skill_id}/${project_id}`, {
        headers: getAuthorizationHeaders()
    })
    if (redirectOnExpiration(response.status)) {        
        return
    }
    if (response.ok){
        const project_data = await response.json()
        updateProjectCard(project_data)
        loadTasks()
        
    }    
}



renderTaskPage()
activateLogout()
activatetoggleAlert()
activateTaskDialog()
activateEditDelete(
    "#project-edit",
    "#project-delete",
    "project",
    editProject,
    deleteProject
)
loadurgenttasks()
