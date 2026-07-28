const DOMAIN_URL = "http://127.0.0.1:8000"



const create_skill_btn = document.querySelector("#new-skill")
const skill_model = document.querySelector("#skill-dialog")

create_skill_btn.addEventListener("click", () => {skill_model.showModal()})


// User validation protocols

const SIGNUP_URL = "http://127.0.0.1:5500/Frontend/pages/signup.html"
const LOGIN_URL = "http://127.0.0.1:5500/Frontend/pages/login.html"
function check_if_user() {
    let has_access_token = localStorage.getItem("access_token") !== null

    if (!has_access_token) {
        window.location.replace(SIGNUP_URL)
    }
}



// Fetch skills


const header_data = {
    'Content-Type' : 'application/json',
    'Authorization' : `Bearer ${localStorage.getItem("access_token")}`
} 


async function fetch_data() {
    const response = await fetch(`${DOMAIN_URL}/skill/skills`, {
        headers: header_data
    })
    
    if(response.status === 401){
        alert("Token Expired, Signin Again")
        window.location.replace(LOGIN_URL)
    }
    if (response.ok) {
        const data = await response.json()
        render_skills(data)
    }
}


function create_element(tag_name, id, class_list, attributes, text_content = "", children){
    const tag = document.createElement(tag_name)
    tag.id = id
    tag.classList.add(...class_list)
    for (const [key, value] of Object.entries(attributes)){
        tag.setAttribute(key, value)
    }
    if (text_content){
        tag.textContent = text_content
    }
    for (const child of children){
        tag.appendChild(child)
    }
    return tag
}

async function render_skills(data) {
    const skill_container = document.querySelector("#skill-container")
    if (skill_container) {
        skill_container.innerHTML = ""
        for (const d of data){
            const skill_box = create_element("section", "", ["skill-box"], {}, "", [
                create_element("div", "", ["skill-info"], {}, "", [
                    create_element("a", "", ["skill-name"], {}, d.skill_name, []),
                    create_element("p", "", ["skill-description"], {}, d.description, [])
                ]),
                create_element("div", "", ["skill-data"], {}, "", [
                    create_element("p", "", ["skill-date"], {}, `Created At: ${d.created_at}<br>Updated At: ${d.updated_at}`)
                ]),
                create_element("a", "", ["skill-id"], {}, d.id, [])
            ])
            skill_container.appendChild(skill_box)
        }
    }
}

check_if_user()
fetch_data()
