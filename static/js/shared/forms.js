import { element } from "./create_element.js"

export function getFormElements() {
    const form = document.querySelector("#signup-form")
    const feedback = document.querySelector("#error-feedback")

    if (!(form instanceof HTMLFormElement) || !(feedback instanceof HTMLElement)) {
        console.error("Failed to access form elements.")
        return null
    }

    return { form, feedback }
}

export function getInputValue(form, name) {
    const input = form.elements.namedItem(name)
    return input instanceof HTMLInputElement ? input.value.trim() : ""
}

export function renderErrors(feedback, errors) {
    feedback.replaceChildren()

    for (const error of errors) {
        const message = element("p", {text: error})
        feedback.appendChild(message)
    }
}

export function initializePasswordToggle() {
    const button = document.querySelector("#show-password")
    const passwordInput = document.querySelector("#password")

    if (!(button instanceof HTMLButtonElement) || !(passwordInput instanceof HTMLInputElement)) {
        console.error("Failed to access password controls.")
        return
    }

    button.addEventListener("click", () => {
        passwordInput.type = passwordInput.type === "password" ? "text" : "password"
    })
}
