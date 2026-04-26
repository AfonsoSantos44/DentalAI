import { AnalysesTable } from "../Components/AnalysesTable";
import { LoadingSkeleton } from "../Components/LoadingSkeleton";
import { createElement, fetchJson } from "../utils";
export function AnalysesPage(onSelect) {
    let listContainer;
    const loadAnalyses = async () => {
        listContainer.innerHTML = "";
        listContainer.appendChild(LoadingSkeleton(5));
        try {
            const analyses = await fetchJson("/analyses/");
            listContainer.innerHTML = "";
            listContainer.appendChild(AnalysesTable(analyses, onSelect));
        }
        catch (error) {
            listContainer.textContent = "Failed to load analyses";
        }
    };
    return {
        id: "analyses",
        label: "Analyses",
        render: () => {
            listContainer = createElement("div");
            return createElement("div", "page", [
                createElement("div", "page-header", [
                    createElement("div", undefined, [
                        createElement("p", "eyebrow", ["History"]),
                        createElement("h1", undefined, ["All analyses"]),
                    ]),
                    createElement("span", "badge accent", ["Database"]),
                ]),
                listContainer,
            ]);
        },
        onShow: loadAnalyses,
    };
}
