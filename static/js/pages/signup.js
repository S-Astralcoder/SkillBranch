import { completeAuthentication } from "../shared/auth.js"
import { API_BASE_URL, PAGE_URLS } from "../shared/config.js"
import {
    getFormElements,
    getInputValue,
    initializePasswordToggle,
    renderErrors
} from "../shared/forms.js"
import { initializeMobileNavigation } from "../shared/navigation.js"

async function signupUser(username, email, password, feedback) {
    const response = await fetch(`${API_BASE_URL}/user/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
    })

    if (response.ok) {
        const data = await response.json()
        completeAuthentication(data.access_token)
    } else if (response.status === 409) {
        feedback.textContent = "User Already Exists"
        setTimeout(() => window.location.replace(PAGE_URLS.login), 3000)
    } else if (response.status === 477) {
        feedback.textContent = "Provide a valid field info"
    } else {
        console.error("Unexpected error occurred")
    }
}

function initializeSignupForm() {
    const elements = getFormElements()

    if (!elements) {
        return
    }

    const { form, feedback } = elements

    form.addEventListener("submit", (event) => {
        event.preventDefault()

        const username = getInputValue(form, "name")
        const email = getInputValue(form, "email")
        const password = getInputValue(form, "password")
        const errors = []

        if (username.length > 100) {
            errors.push("Username should of length (1~100)")
        }

        if (email.length < 6 || email.length > 200) {
            errors.push("email should of length (6~200)")
        }

        if (password.length < 8 || password.length > 200) {
            errors.push("password should of length (1~200)")
        }

        if (errors.length === 0) {
            void signupUser(username, email, password, feedback)
        } else {
            renderErrors(feedback, errors)
        }
    })
}

initializeMobileNavigation()
initializeSignupForm()
initializePasswordToggle()
