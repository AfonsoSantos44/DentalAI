import { createElement } from "../utils.js";
export function SettingsPage() {
    const toggles = [
        { label: "Auto-run summaries after transcription", checked: true },
        { label: "Email me when an analysis finishes", checked: false },
        { label: "Show confidence badge on results", checked: true },
    ];
    return {
        id: "settings",
        label: "Settings",
        render: () => {
            const list = createElement("div", "card settings");
            toggles.forEach((toggle) => {
                const row = createElement("label", "setting-row", [
                    createElement("span", undefined, [toggle.label]),
                ]);
                const input = document.createElement("input");
                input.type = "checkbox";
                input.checked = toggle.checked;
                row.appendChild(input);
                list.appendChild(row);
            });
            return createElement("div", "page", [
                createElement("div", "page-header", [
                    createElement("div", undefined, [
                        createElement("p", "eyebrow", ["Preferences"]),
                        createElement("h1", undefined, ["Settings"]),
                    ]),
                    createElement("span", "badge accent", ["Local"]),
                ]),
                list,
            ]);
        },
    };
}
