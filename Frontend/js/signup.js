const DASHBOARD_URL = "http://127.0.0.1:5500/Frontend/pages/skill_dashboard.html"
const LOGIN_URL = "http://127.0.0.1:5500/Frontend/pages/login.html"

const DOMAIN_URL = "http://127.0.0.1:8000"



const form = document.querySelector("#signup-form")
const error_feedback = document.querySelector("#error-feedback")

if (!form || !error_feedback) {
    console.error("Failed to access elements.")
}


async function signup_user(username, email, password) {
    const response = await fetch(`${DOMAIN_URL}/user/signup`, {
        method: "POST",
        headers: {
            'Content-Type' : "application/json"
        },
        body: JSON.stringify({username: username, email: email, password:password})
    })

    if (response.ok) {
        const data = await response.json()
        localStorage.setItem("access_token", data.access_token)
        window.location.replace(DASHBOARD_URL)
    }
    else if (response.status === 409){
        error_feedback.innerHTML = "User Already Exists"
        setTimeout(()=> {window.location.replace(LOGIN_URL)}, 3000)
    }
    else if (response.status === 477){
        error_feedback.innerHTML = "Provide a valid field info"
    }
    else {
        console.error("Unexpected error occurred")
    }
}

form.addEventListener("submit", async (event)=> {
    event.preventDefault()

    let error_container = []

    let username = form.elements["name"].value.trim()
    let email = form.elements["email"].value.trim()
    let password = form.elements["password"].value.trim()

    if (username.length > 100) {
        error_container.push("Username should of length (1~100)")
    }

    if (email.length < 6 || email.length > 200) {
        error_container.push("email should of length (6~200)")
    }

    if (password.length < 8 || password.length > 200) {
        error_container.push("password should of length (1~200)")
    }

    if (error_container.length === 0){
        signup_user(username,email, password)
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