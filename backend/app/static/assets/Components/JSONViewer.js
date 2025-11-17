import { createElement } from "../utils.js";
export function JSONViewer(data) {
    const pre = createElement("pre", "json-viewer");
    pre.textContent = data ? JSON.stringify(data, null, 2) : "No clinical JSON captured yet.";
    return pre;
}
