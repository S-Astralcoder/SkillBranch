import { getAuthorizationHeaders, redirectIfUnauthenticated } from "../shared/auth.js"
import { activateLogout, initializeDashboardMenus, initializeDialog } from "../shared/dashboard.js"
import { API_BASE_URL } from "../shared/config.js"
import { PAGE_URLS } from "../shared/config.js"
import { redirectOnExpiration } from "../shared/auth.js"
import { element } from "../shared/create_element.js"
initializeDashboardMenus()
initializeDialog("#create-task", "#task-dialog")
redirectIfUnauthenticated()

const skill_id = sessionStorage.getItem("skill_id")
const project_id = sessionStorage.getItem("project_id")

function updateProjectCard(project_data){
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
                    element("span", {text: `Deadline: ${new Date(task.deadline).toDateString()}`})
                ]})
            ]}),
            // @ts-ignore
            element("a", {
                // @ts-ignore
                classlist: ["task-card-id"],
                text: task.id
            }),
            // @ts-ignore
            element("input", {classlist: ["task-checkbox"], attributes: checkbox_attributes})
        ]})
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