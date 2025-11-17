import { createElement } from "./utils";
export class Layout {
    constructor(pages, initial) {
        this.pages = pages;
        this.activeId = initial;
    }
    mount(host) {
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
    show(id) {
        const page = this.pages.find((p) => p.id === id);
        if (!page)
            return;
        this.activeId = id;
        // Update nav styles
        this.sidebar.querySelectorAll(".nav-item").forEach((el) => {
            const isActive = el.dataset.pageId === id;
            el.classList.toggle("active", isActive);
        });
        this.content.innerHTML = "";
        this.content.appendChild(page.render());
        page.onShow?.();
    }
}
