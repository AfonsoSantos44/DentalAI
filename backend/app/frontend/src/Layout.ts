import { createElement } from "./utils";

export interface PageConfig {
  id: string;
  label: string;
  icon?: string;
  render: () => HTMLElement;
  onShow?: () => void;
}

export class Layout {
  private sidebar!: HTMLElement;
  private content!: HTMLElement;
  private activeId: string;

  constructor(private pages: PageConfig[], initial: string) {
    this.activeId = initial;
  }

  mount(host: HTMLElement): void {
    this.sidebar = createElement("aside", "sidebar");
    const navHeader = createElement("div", "sidebar__brand", [
      createElement("div", "brand-mark"),
      createElement("div", "brand-text", ["Dental AI"]),
    ]);

    const navList = createElement("nav", "sidebar__nav");
    this.pages.forEach((page) => {
      const button = createElement("button", "nav-item", [page.label]);
      button.dataset.pageId = page.id;
      button.addEventListener("click", () => this.show(page.id));
      navList.appendChild(button);
    });

    this.sidebar.append(navHeader, navList);

    this.content = createElement("main", "app-main");

    const layout = createElement("div", "app-shell", [this.sidebar, this.content]);
    host.innerHTML = "";
    host.appendChild(layout);

    this.show(this.activeId);
  }

  show(id: string): void {
    const page = this.pages.find((p) => p.id === id);
    if (!page) return;
    this.activeId = id;

    // Update nav styles
    this.sidebar.querySelectorAll(".nav-item").forEach((el) => {
      const isActive = (el as HTMLElement).dataset.pageId === id;
      el.classList.toggle("active", isActive);
    });

    this.content.innerHTML = "";
    this.content.appendChild(page.render());
    page.onShow?.();
  }
}
