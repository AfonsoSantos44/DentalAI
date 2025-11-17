import { createElement } from "../utils";

export function StatsCard(label: string, value: string): HTMLElement {
  return createElement("div", "stat-card", [
    createElement("span", "stat-card__label", [label]),
    createElement("strong", "stat-card__value", [value]),
  ]);
}
