import { ProcessingSteps } from "./ProcessingSteps.js";
import { createElement, fetchJson } from "../utils.js";
export class FileUpload {
    constructor(options) {
        this.options = options;
        this.selectedFile = null;
        this.mediaRecorder = null;
        this.recordedChunks = [];
    }
    render() {
        const wrapper = createElement("div", "card upload-card");
        this.statusBadge = createElement("span", "badge accent", ["Ready to upload"]);
        this.fileName = createElement("p", "muted", ["No audio selected yet."]);
        this.progressBar = createElement("div", "progress-bar");
        this.stepsContainer = ProcessingSteps(["active", "pending", "pending", "pending"]);
        const dropzone = createElement("div", "dropzone", [
            createElement("p", undefined, ["Drag & drop an audio file or click to browse"]),
            createElement("small", "muted", ["WAV, MP3, or M4A. Max 10 minutes."])
        ]);
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = "audio/*";
        fileInput.style.display = "none";
        fileInput.addEventListener("change", (event) => {
            const target = event.target;
            const file = target.files?.[0];
            if (file)
                this.setFile(file);
        });
        ["dragenter", "dragover"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.add("dragging");
            });
        });
        ["dragleave", "drop"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.remove("dragging");
            });
        });
        dropzone.addEventListener("drop", (event) => {
            const file = event.dataTransfer?.files?.[0];
            if (file)
                this.setFile(file);
        });
        dropzone.addEventListener("click", () => fileInput.click());
        this.processButton = createElement("button", "btn btn--primary", ["Process audio"]);
        this.processButton.addEventListener("click", () => this.process());
        this.recordButton = createElement("button", "btn", ["Record note"]);
        this.recordButton.addEventListener("click", () => this.toggleRecording());
        const actions = createElement("div", "actions", [this.processButton, this.recordButton]);
        wrapper.append(createElement("div", "upload-header", [
            createElement("div", undefined, [
                createElement("p", "eyebrow", ["Full pipeline"]),
                createElement("h2", undefined, ["Upload or record your clinical note"]),
                this.fileName,
            ]),
            this.statusBadge,
        ]), dropzone, fileInput, this.progressBar, this.stepsContainer, actions);
        return wrapper;
    }
    setFile(file) {
        this.selectedFile = file;
        this.fileName.textContent = `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`;
        this.statusBadge.textContent = "Ready to process";
        this.statusBadge.className = "badge accent";
    }
    setProgress(percent) {
        this.progressBar.style.width = `${percent}%`;
    }
    setSteps(status) {
        this.stepsContainer.replaceWith(this.stepsContainer = ProcessingSteps(status));
    }
    resetButtons(disabled) {
        this.processButton.disabled = disabled;
        this.recordButton.disabled = disabled;
    }
    async process() {
        if (!this.selectedFile) {
            this.statusBadge.textContent = "Select an audio file first";
            this.statusBadge.className = "badge warning";
            return;
        }
        const formData = new FormData();
        formData.append("file", this.selectedFile);
        this.resetButtons(true);
        this.setProgress(18);
        this.setSteps(["done", "active", "pending", "pending"]);
        this.statusBadge.textContent = "Processing…";
        this.statusBadge.className = "badge accent";
        try {
            const response = await fetchJson("/audio/process_full", { method: "POST", body: formData });
            this.setProgress(76);
            this.setSteps(["done", "done", "done", "active"]);
            await this.options.onProcessed(response.analysis_id);
            this.setProgress(100);
            this.setSteps(["done", "done", "done", "done"]);
            this.statusBadge.textContent = `Analysis #${response.analysis_id} ready`;
            this.statusBadge.className = "badge success";
        }
        catch (error) {
            const message = error instanceof Error ? error.message : "Processing failed";
            this.statusBadge.textContent = message;
            this.statusBadge.className = "badge warning";
            this.setSteps(["done", "error", "pending", "pending"]);
        }
        finally {
            this.resetButtons(false);
            setTimeout(() => this.setProgress(0), 500);
        }
    }
    async toggleRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === "recording") {
            this.mediaRecorder.stop();
            this.recordButton.textContent = "Record note";
            this.recordButton.classList.remove("btn--muted");
            return;
        }
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.recordedChunks = [];
            this.mediaRecorder = new MediaRecorder(stream);
            this.mediaRecorder.ondataavailable = (event) => this.recordedChunks.push(event.data);
            this.mediaRecorder.onstop = () => {
                const blob = new Blob(this.recordedChunks, { type: "audio/webm" });
                const file = new File([blob], `recording-${Date.now()}.webm`, { type: "audio/webm" });
                this.setFile(file);
            };
            this.mediaRecorder.start();
            this.recordButton.textContent = "Stop recording";
            this.recordButton.classList.add("btn--muted");
        }
        catch (error) {
            this.statusBadge.textContent = "Microphone permission denied";
            this.statusBadge.className = "badge warning";
        }
    }
}
