import { createElement, badge } from "../utils";
const STEP_LABELS = [
    "Upload audio",
    "Transcribe note",
    "Extract clinical JSON",
    "Generate summaries",
];
export function ProcessingSteps(current) {
    const wrapper = createElement("div", "processing-steps");
    STEP_LABELS.forEach((label, index) => {
        const status = current[index] ?? "pending";
        const row = createElement("div", "processing-step", [
            createElement("div", "processing-step__label", [label]),
            badge(statusLabel(status), toneFor(status)),
        ]);
        wrapper.appendChild(row);
    });
    return wrapper;
}
function statusLabel(status) {
    switch (status) {
        case "active":
            return "In progress";
        case "done":
            return "Complete";
        case "error":
            return "Error";
        default:
            return "Pending";
    }
}
function toneFor(status) {
    switch (status) {
        case "active":
            return "accent";
        case "done":
            return "success";
        case "error":
            return "warning";
        default:
            return "muted";
    }
}
