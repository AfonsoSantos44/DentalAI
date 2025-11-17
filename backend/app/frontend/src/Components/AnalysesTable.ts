import { AnalysisSummary } from "../types";
import { createElement, formatDate } from "../utils";

export function AnalysesTable(analyses: AnalysisSummary[], onSelect: (id: number) => void): HTMLElement {
  const wrapper = createElement("div", "card");
  const table = createElement("table", "table");
  const header = createElement("thead");
  header.innerHTML = `
    <tr>
      <th>ID</th>
      <th>Created</th>
      <th>Transcription</th>
      <th>Processing</th>
    </tr>
  `;
  table.appendChild(header);
  const body = createElement("tbody");

  analyses.forEach((analysis) => {
    const row = createElement("tr", undefined, [
      createElement("td", "mono", [`#${analysis.id}`]),
      createElement("td", undefined, [formatDate(analysis.created_at)]),
      createElement("td", "truncate", [analysis.transcription || "(empty)"] ),
      createElement("td", "mono", [analysis.processing_ms ? `${analysis.processing_ms} ms` : "--"]),
    ]);
    row.addEventListener("click", () => onSelect(analysis.id));
    body.appendChild(row);
  });

  if (!analyses.length) {
    const empty = createElement("tr", "empty-row", [
      createElement("td", undefined, ["No analyses yet. Run one from Upload."]),
    ]);
    empty.firstElementChild?.setAttribute("colspan", "4");
    body.appendChild(empty);
  }

  table.appendChild(body);
  wrapper.appendChild(table);
  return wrapper;
}
