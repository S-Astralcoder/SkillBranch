// @ts-nocheck
import {
    getAuthorizationHeaders,
    redirectIfUnauthenticated
} from "../shared/auth.js"
import { API_BASE_URL, PAGE_URLS } from "../shared/config.js"
import { initializeDashboardMenus, initializeDialog } from "../shared/dashboard.js"
import { element } from "../shared/create_element.js"

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
    const skill_container = document.querySelector("#skill-container")
    skill_container.replaceChildren()
    for (const data of skillData){
        const skill_box = element("section", {classlist: ["skill-box"], childern:
            [
                element("div", {classlist: ["skill-info"], childern: 
                    [
                        element("a", {classlist: ["skill-name"], text: data.skill_name}),
                        element("p", {classlist: ["skill-description"], text: data.description})
                    ]}),
                element("div", {classlist: ["skill-data"], childern: 
                    [
                        element("p", {classlist: ["skill-date"], childern: [
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
}

/*
<section class="skill-box">
    <div class="skill-info">
        <a href="" class="skill-name">Skill Name</a>
        <p class="skill-description">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Voluptatum nobis quibusdam ab quos consequatur perspiciatis </p>
    </div>
    <div class="skill-data">
        <p class="skill-date">Created At: <br>Updated At: </p>
    </div>
    <a href="" class="skill-id">#id:dhashdjh32hjdaj34had</a>
</section>



*/


initializeDashboardMenus()
initializeDialog("#new-skill", "#skill-dialog")
redirectIfUnauthenticated()
fetchSkills()
