import { createElement } from "../utils";

export function InfoCard(title: string, body: string): HTMLElement {
  return createElement("div", "info-card", [
    createElement("p", "info-card__title", [title]),
    createElement("p", "info-card__body", [body]),
  ]);
}
