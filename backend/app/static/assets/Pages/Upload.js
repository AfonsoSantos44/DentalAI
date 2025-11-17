import { FileUpload } from "../Components/FileUpload.js";
import { createElement } from "../utils.js";
export function UploadPage(onProcessed) {
    const upload = new FileUpload({ onProcessed });
    return {
        id: "upload",
        label: "Upload",
        render: () => createElement("div", "page", [
            createElement("div", "page-header", [
                createElement("div", undefined, [
                    createElement("p", "eyebrow", ["Pipeline"]),
                    createElement("h1", undefined, ["Upload or record new audio"]),
                ]),
                createElement("span", "badge accent", ["Audio → JSON"]),
            ]),
            upload.render(),
        ]),
    };
}
