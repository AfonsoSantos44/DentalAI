export async function fetchJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        let message = `Request failed (${response.status})`;
        try {
            const payload = (await response.json());
            if (typeof payload?.detail === "string") {
                message = payload.detail;
            }
            else if (payload?.detail && typeof payload.detail === "object") {
                const detail = payload.detail;
                message = detail.message ?? message;
            }
        }
        catch (error) {
            // ignore json parse errors
        }
        throw new Error(message);
    }
    return (await response.json());
}
export function formatDate(iso) {
    if (!iso)
        return "--";
    const date = new Date(iso);
    return date.toLocaleString();
}
export function createElement(tag, className, children) {
    const el = document.createElement(tag);
    if (className)
        el.className = className;
    if (children) {
        for (const child of children) {
            if (child === null || child === undefined)
                continue;
            if (typeof child === "string") {
                el.appendChild(document.createTextNode(child));
            }
            else {
                el.appendChild(child);
            }
        }
    }
    return el;
}
export function badge(text, tone = "muted") {
    const span = document.createElement("span");
    span.className = `badge ${tone}`;
    span.textContent = text;
    return span;
}
