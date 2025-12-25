// ============================================
// 🌿 DietVeda — Core JavaScript Utilities
// ============================================

// ----------------------------
// Loading Spinner Utilities
// ----------------------------
function showLoading(element) {
    if (!element) return;
    element.innerHTML = `
        <div class="loading-spinner"></div>
    `;
}

function hideLoading(element) {
    if (!element) return;
    element.innerHTML = "";
}

// ----------------------------
// API Helper (Fetch Wrapper)
// ----------------------------
async function apiCall(endpoint, method = "GET", data = null) {
    const url = `http://localhost:5000${endpoint}`;

    const options = {
        method: method,
        headers: { "Content-Type": "application/json" }
    };

    if (data) options.body = JSON.stringify(data);

    try {
        const response = await fetch(url, options);

        // Handle non-JSON or server errors gracefully
        if (!response.ok) {
            return {
                error: true,
                status: response.status,
                message: `Server responded with ${response.status}`
            };
        }

        return await response.json();

    } catch (error) {
        console.error("API Error:", error);

        return {
            error: true,
            message: error.message || "Network error"
        };
    }
}

// ----------------------------
// Smooth Scroll Helper
// ----------------------------
function smoothScroll(element) {
    if (!element) return;
    element.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

// ----------------------------
// Utility: Delay (Promise-based timeout)
// Helps in animations or async flows
// ----------------------------
function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ----------------------------
// Utility: Add/Remove classes safely
// ----------------------------
function addClass(el, className) {
    if (el && !el.classList.contains(className)) {
        el.classList.add(className);
    }
}

function removeClass(el, className) {
    if (el && el.classList.contains(className)) {
        el.classList.remove(className);
    }
}

// ----------------------------
// Utility: Safe Element Fetch
// ----------------------------
function $(selector) {
    return document.querySelector(selector);
}

function $all(selector) {
    return document.querySelectorAll(selector);
}
