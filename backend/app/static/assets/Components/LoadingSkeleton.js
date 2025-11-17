import { createElement } from "../utils.js";
export function LoadingSkeleton(lines = 3) {
    const wrapper = createElement("div", "skeleton");
    for (let i = 0; i < lines; i += 1) {
        wrapper.appendChild(createElement("div", "skeleton__line"));
    }
    return wrapper;
}
