import { createElement } from "../utils";

export function GradientButton(label: string, onClick: () => void): HTMLButtonElement {
  const button = createElement("button", "btn btn--gradient", [label]);
  button.type = "button";
  button.addEventListener("click", onClick);
  return button as HTMLButtonElement;
}
