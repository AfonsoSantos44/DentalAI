import { JSONViewer } from "../Components/JSONViewer";
import { LoadingSkeleton } from "../Components/LoadingSkeleton";
import { createElement } from "../utils";
import { AnalysisSummary } from "../types";

export class ResultsPage {
  private container!: HTMLElement;
  private transcription!: HTMLElement;
  private summaries!: HTMLElement;
  private jsonSlot!: HTMLElement;

  render(): HTMLElement {
    this.transcription = createElement("p", "muted", ["Run an analysis to see the transcript."]);
    this.summaries = createElement("div", "grid two-col");
    this.jsonSlot = createElement("div");

    this.container = createElement("div", "page", [
      createElement("div", "page-header", [
        createElement("div", undefined, [
          createElement("p", "eyebrow", ["Results"]),
          createElement("h1", undefined, ["Review the AI outputs"]),
        ]),
        createElement("span", "badge muted", ["Awaiting analysis"]),
      ]),
      createElement("div", "card", [
        createElement("h3", undefined, ["Transcription"]),
        this.transcription,
      ]),
      createElement("div", "grid two-col", [
        createElement("div", "card", [
          createElement("h3", undefined, ["Patient-friendly"]),
          createElement("p", "eyebrow", ["Portuguese"]),
          this.summaries,
        ]),
        createElement("div", "card", [
          createElement("h3", undefined, ["Clinical JSON"]),
          this.jsonSlot,
        ]),
      ]),
    ]);

    return this.container;
  }

  showLoading(): void {
    if (this.summaries) this.summaries.innerHTML = "";
    this.jsonSlot.innerHTML = "";
    this.summaries.appendChild(LoadingSkeleton(4));
    this.jsonSlot.appendChild(LoadingSkeleton(6));
  }

  setResult(result: AnalysisSummary): void {
    if (!this.container) return;
    this.transcription.textContent = result.transcription || "(empty transcription)";
    this.summaries.innerHTML = "";
    this.summaries.appendChild(
      createElement("p", "summary-block", [result.summary_pt || "No summary yet."])
    );
    this.summaries.appendChild(
      createElement("p", "summary-block", [result.summary_en || "No English summary yet."])
    );

    this.jsonSlot.innerHTML = "";
    this.jsonSlot.appendChild(JSONViewer(result.clinical_json));

    const badge = this.container.querySelector(".page-header .badge");
    if (badge) {
      badge.textContent = `Analysis #${result.id}`;
      badge.className = "badge success";
    }
  }
}
