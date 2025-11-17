import { StatsCard } from "../Components/StatsCard";
import { LoadingSkeleton } from "../Components/LoadingSkeleton";
import { createElement, fetchJson } from "../utils";
import { Stats } from "../types";

export function DashboardPage() {
  let statsContainer: HTMLElement;

  const renderStats = async () => {
    statsContainer.innerHTML = "";
    statsContainer.appendChild(LoadingSkeleton(2));
    try {
      const stats = await fetchJson<Stats>("/stats/");
      statsContainer.innerHTML = "";
      statsContainer.append(
        StatsCard("Total Analyses", String(stats.total_analyses ?? 0)),
        StatsCard("Avg. Processing", stats.avg_processing ?? "--"),
        StatsCard("Success Rate", stats.success_rate ?? "--"),
      );
    } catch (error) {
      statsContainer.innerHTML = "Failed to load stats";
    }
  };

  return {
    id: "dashboard",
    label: "Dashboard",
    render: () => {
      statsContainer = createElement("div", "grid three-col stats-grid");
      const page = createElement("div", "page", [
        createElement("div", "page-header", [
          createElement("div", undefined, [
            createElement("p", "eyebrow", ["Realtime"],),
            createElement("h1", undefined, ["Operational metrics"]),
          ]),
          createElement("span", "badge accent", ["Live"]),
        ]),
        statsContainer,
      ]);
      return page;
    },
    onShow: renderStats,
  };
}
