import { AnalysesTable } from "../Components/AnalysesTable";
import { LoadingSkeleton } from "../Components/LoadingSkeleton";
import { createElement, fetchJson } from "../utils";
import { AnalysisSummary } from "../types";

export function AnalysesPage(onSelect: (id: number) => void) {
  let listContainer: HTMLElement;

  const loadAnalyses = async () => {
    listContainer.innerHTML = "";
    listContainer.appendChild(LoadingSkeleton(5));
    try {
      const analyses = await fetchJson<AnalysisSummary[]>("/analyses/");
      listContainer.innerHTML = "";
      listContainer.appendChild(AnalysesTable(analyses, onSelect));
    } catch (error) {
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
