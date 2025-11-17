import { ApiError } from "./types";

export async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const payload = (await response.json()) as ApiError;
      if (typeof payload?.detail === "string") {
        message = payload.detail;
      } else if (payload?.detail && typeof payload.detail === "object") {
        const detail = payload.detail as { message?: string };
        message = detail.message ?? message;
      }
    } catch (error) {
      // ignore json parse errors
    }
    throw new Error(message);
  }
  return (await response.json()) as T;
}

export function formatDate(iso?: string | null): string {
  if (!iso) return "--";
  const date = new Date(iso);
  return date.toLocaleString();
}

export function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className?: string,
  children?: (HTMLElement | string | null | undefined)[]
): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (children) {
    for (const child of children) {
      if (child === null || child === undefined) continue;
      if (typeof child === "string") {
        el.appendChild(document.createTextNode(child));
      } else {
        el.appendChild(child);
      }
    }
  }
  return el;
}

export function badge(text: string, tone: "accent" | "success" | "warning" | "muted" = "muted"):
  HTMLSpanElement {
  const span = document.createElement("span");
  span.className = `badge ${tone}`;
  span.textContent = text;
  return span;
}
