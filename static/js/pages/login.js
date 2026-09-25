import { completeAuthentication } from "../shared/auth.js"
import { API_BASE_URL } from "../shared/config.js"
import {
    getFormElements,
    getInputValue,
    initializePasswordToggle,
    renderErrors
} from "../shared/forms.js"
import { initializeMobileNavigation } from "../shared/navigation.js"

async function loginUser(email, password, feedback) {
    const body = new URLSearchParams()
    body.append("username", email)
    body.append("password", password)

    const response = await fetch(`${API_BASE_URL}/user/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body
    })

    if (response.ok) {
        const data = await response.json()
        completeAuthentication(data.access_token)
    } else if (response.status === 477) {
        feedback.textContent = "Provide a valid field info"
    } else {
        console.error("Unexpected error occurred", await response.json())
    }
}

function initializeLoginForm() {
    const elements = getFormElements()

    if (!elements) {
        return
    }

    const { form, feedback } = elements

    form.addEventListener("submit", (event) => {
        event.preventDefault()

        const email = getInputValue(form, "email")
        const password = getInputValue(form, "password")
        const errors = []

        if (email.length < 6 || email.length > 200) {
            errors.push("email should of length (6~200)")
        }

        if (password.length < 8 || password.length > 200) {
            errors.push("password should of length (1~200)")
        }

        if (errors.length === 0) {
            void loginUser(email, password, feedback)
        } else {
            renderErrors(feedback, errors)
        }
    })
}

initializeMobileNavigation()
initializeLoginForm()
initializePasswordToggle()
