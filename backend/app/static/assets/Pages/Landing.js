import { GradientButton } from "../Components/GradientButton.js";
import { InfoCard } from "../Components/InfoCard.js";
import { createElement } from "../utils.js";
export function LandingPage(onGetStarted) {
    return {
        id: "landing",
        label: "Landing",
        render: () => {
            const hero = createElement("div", "hero", [
                createElement("div", "hero__copy", [
                    createElement("p", "eyebrow", ["Dental AI Assistant"]),
                    createElement("h1", undefined, ["Audio to clinical insight in seconds."]),
                    createElement("p", "muted", [
                        "Upload a chairside dictation or record a new note to generate transcriptions, clinical JSON, and bilingual summaries with a single click.",
                    ]),
                    GradientButton("Start with an upload", onGetStarted),
                ]),
                createElement("div", "hero__grid", [
                    InfoCard("Upload", "Drop an MP3, WAV, or M4A and we will validate and transcribe it."),
                    InfoCard("Process", "Clinical JSON extraction and Portuguese/English summaries run automatically."),
                    InfoCard("Review", "See transcripts, JSON, summaries, and stats across all analyses."),
                ]),
            ]);
            return createElement("div", "page", [hero]);
        },
    };
}
