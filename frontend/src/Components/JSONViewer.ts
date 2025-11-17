import { createElement } from "../utils";

export function JSONViewer(data: Record<string, unknown> | null): HTMLElement {
  const pre = createElement("pre", "json-viewer");
  pre.textContent = data ? JSON.stringify(data, null, 2) : "No clinical JSON captured yet.";
  return pre;
}
