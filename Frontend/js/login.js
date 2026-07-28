const DASHBOARD_URL = "http://127.0.0.1:5500/Frontend/pages/skill_dashboard.html"

const DOMAIN_URL = "http://127.0.0.1:8000"



const form = document.querySelector("#signup-form")
const error_feedback = document.querySelector("#error-feedback")

if (!form || !error_feedback) {
    console.error("Failed to access elements.")
}


async function login_user(email, password) {
    const FormData = new URLSearchParams()
    FormData.append("username", email)
    FormData.append("password", password)
    const response = await fetch(`${DOMAIN_URL}/user/login`, {
        method: "POST",
        headers: {
            'Content-Type' : "application/x-www-form-urlencoded"
        },
        body: FormData
    })

    if (response.ok) {
        const data = await response.json()
        localStorage.setItem("access_token", data.access_token)
        window.location.replace(DASHBOARD_URL)
    }
    else if (response.status === 477){
        error_feedback.innerHTML = "Provide a valid field info"
    }
    else {
        console.error("Unexpected error occurred")
        console.log(await response.json())
    }
}

form.addEventListener("submit", async (event)=> {
    event.preventDefault()

    let error_container = []

    let email = form.elements["email"].value.trim()
    let password = form.elements["password"].value.trim()

    if (email.length < 6 || email.length > 200) {
        error_container.push("email should of length (6~200)")
    }

    if (password.length < 8 || password.length > 200) {
        error_container.push("password should of length (1~200)")
    }

    if (error_container.length === 0){
        login_user(email, password)
    }
    else {
        error_feedback.innerHTML = ""
        for (error of error_container) {
            const p = document.createElement("p")
            p.textContent = error
            error_feedback.appendChild(p)
        }
    }
})



// Hide/SHow password


const pass_btn = document.querySelector("#show-password")
const password_input = document.querySelector("#password")
pass_btn.addEventListener("click", ()=> {
    password_input.type = password_input.type === "password" ? "text" : "password"
})