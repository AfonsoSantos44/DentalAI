import { createElement } from "../utils.js";
export function InfoCard(title, body) {
    return createElement("div", "info-card", [
        createElement("p", "info-card__title", [title]),
        createElement("p", "info-card__body", [body]),
    ]);
}
