import { createElement } from "../utils";
export function GradientButton(label, onClick) {
    const button = createElement("button", "btn btn--gradient", [label]);
    button.type = "button";
    button.addEventListener("click", onClick);
    return button;
}
