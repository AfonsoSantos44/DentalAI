import { Layout } from "./Layout";
import { LandingPage } from "./Pages/Landing";
import { DashboardPage } from "./Pages/Dashboard";
import { UploadPage } from "./Pages/Upload";
import { AnalysesPage } from "./Pages/Analyses";
import { SettingsPage } from "./Pages/Settings";
import { ResultsPage } from "./Pages/Results";
import { fetchJson } from "./utils";
async function fetchAnalysisWithSummaries(id) {
    const [analysis, summaries] = await Promise.all([
        fetchJson(`/analyses/${id}`),
        fetchJson(`/summaries/${id}`),
    ]);
    return { ...analysis, summary_pt: summaries.pt, summary_en: summaries.en };
}
document.addEventListener("DOMContentLoaded", () => {
    const appRoot = document.getElementById("app");
    if (!appRoot)
        return;
    const resultsPage = new ResultsPage();
    let layout;
    const selectAnalysis = async (id) => {
        resultsPage.showLoading();
        layout.show("results");
        const full = await fetchAnalysisWithSummaries(id);
        resultsPage.setResult(full);
    };
    layout = new Layout([
        LandingPage(() => layout.show("upload")),
        DashboardPage(),
        UploadPage(selectAnalysis),
        AnalysesPage(selectAnalysis),
        { id: "results", label: "Results", render: () => resultsPage.render() },
        SettingsPage(),
    ], "landing");
    layout.mount(appRoot);
});
