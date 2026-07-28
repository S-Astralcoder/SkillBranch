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


function create_element(
    tag_name,
    {
        id = "",
        classes = [],
        attributes = {},
        text = "",
        children = []
    } = {}
) {
    const element = document.createElement(tag_name)

    if (id) {
        element.id = id
    }

    element.classList.add(...classes.filter(Boolean))

    for (const [key, value] of Object.entries(attributes)) {
        if (value !== null && value !== undefined) {
            element.setAttribute(key, value)
        }
    }

    if (text !== "") {
        element.textContent = String(text)
    }

    for (const child of children.flat(Infinity)) {
        if (child !== null && child !== undefined && child !== false) {
            element.append(child)
        }
    }

    return element
}

function render_skills(data) {
    const skill_container = document.querySelector("#skill-container")
    if (!skill_container) {
        return
    }

    const skill_fragment = document.createDocumentFragment()

    for (const skill of data) {
        const skill_box = create_element("section", {
            classes: ["skill-box"],
            children: [
                create_element("div", {
                    classes: ["skill-info"],
                    children: [
                        create_element("a", {
                            classes: ["skill-name"],
                            text: skill.skill_name
                        }),
                        create_element("p", {
                            classes: ["skill-description"],
                            text: skill.description
                        })
                    ]
                }),
                create_element("div", {
                    classes: ["skill-data"],
                    children: [
                        create_element("p", {
                            classes: ["skill-date"],
                            children: [
                                `Created At: ${skill.created_at}`,
                                create_element("br"),
                                `Updated At: ${skill.updated_at}`
                            ]
                        })
                    ]
                }),
                create_element("a", {
                    classes: ["skill-id"],
                    text: skill.id
                })
            ]
        })

        skill_fragment.appendChild(skill_box)
    }

    skill_container.replaceChildren(skill_fragment)
}

check_if_user()
fetch_data()
