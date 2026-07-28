import { PAGE_URLS } from "./config.js"

export function redirectIfUnauthenticated() {
    if (localStorage.getItem("access_token") === null) {
        window.location.replace(PAGE_URLS.signup)
    }
}

export function getAuthorizationHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
}

export function completeAuthentication(accessToken) {
    localStorage.setItem("access_token", accessToken)
    window.location.replace(PAGE_URLS.dashboard)
}
