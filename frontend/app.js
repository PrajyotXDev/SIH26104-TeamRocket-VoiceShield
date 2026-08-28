const $ = (selector) => document.querySelector(selector);

const fileInput = $("#file");
const dropZone = $("#drop");

let selectedFile = null;
let lastResult = null;


/* =========================
   API HEALTH CHECK
========================= */

async function health() {
    try {
        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        $("#api").textContent = "API online";
    } catch (error) {
        $("#api").textContent = "API offline";
        console.error("Health check failed:", error);
    }
}

health();


/* =========================
   FILE SELECTION
========================= */

fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
        loadFile(fileInput.files[0]);
    }
};


dropZone.ondragover = (event) => {
    event.preventDefault();
    dropZone.classList.add("dragging");
};


dropZone.ondragleave = () => {
    dropZone.classList.remove("dragging");
};


dropZone.ondrop = (event) => {
    event.preventDefault();

    dropZone.classList.remove("dragging");

    const droppedFile = event.dataTransfer.files[0];

    if (droppedFile) {
        loadFile(droppedFile);
    }
};


/* =========================
   LOAD AUDIO
========================= */

function loadFile(file) {

    if (!file) return;

    if (file.size > 50 * 1024 * 1024) {
        alert("Maximum file size is 50 MB.");
        return;
    }

    const allowedTypes = [
        "audio/wav",
        "audio/wave",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/ogg",
        "audio/flac"
    ];

    const extension = file.name.toLowerCase();

    const validExtension =
        extension.endsWith(".wav") ||
        extension.endsWith(".mp3") ||
        extension.endsWith(".ogg") ||
        extension.endsWith(".flac");

    if (!allowedTypes.includes(file.type) && !validExtension) {
        alert("Please upload a WAV, MP3, OGG, or FLAC audio file.");
        return;
    }

    selectedFile = file;

    $("#name").textContent = file.name;

    $("#meta").textContent =
        (file.size / 1048576).toFixed(2) + " MB";

    $("#player").src = URL.createObjectURL(file);

    $("#drop").classList.add("hidden");

    $("#sample").classList.remove("hidden");

    drawWaveform();
}


/* =========================
   RESET
========================= */

function reset() {

    selectedFile = null;

    fileInput.value = "";

    $("#player").src = "";

    $("#sample").classList.add("hidden");

    $("#results").classList.add("hidden");

    $("#drop").classList.remove("hidden");
}


/* =========================
   WAVEFORM
========================= */

function drawWaveform() {

    const canvas = $("#wave");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    canvas.width = canvas.clientWidth * 2;
    canvas.height = 200;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#7c5cff";

    ctx.lineWidth = 2;

    ctx.beginPath();

    for (let i = 0; i < canvas.width; i++) {

        const amplitude =
            Math.sin(i / 12) * 25 +
            Math.sin(i / 37) * 15 +
            Math.sin(i / 7) * 8;

        const y = 100 + amplitude;

        if (i === 0) {
            ctx.moveTo(i, y);
        } else {
            ctx.lineTo(i, y);
        }
    }

    ctx.stroke();
}


/* =========================
   ANALYZE AUDIO
========================= */

$("#analyze").onclick = async () => {

    if (!selectedFile) {
        alert("Please select an audio file first.");
        return;
    }

    const button = $("#analyze");

    button.disabled = true;

    button.textContent = "Analyzing...";

    try {

        const formData = new FormData();

        formData.append("file", selectedFile);

        console.log("Sending audio to backend...");

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        console.log("Backend status:", response.status);

        const responseText = await response.text();

        console.log("Backend response:", responseText);

        if (!response.ok) {

            throw new Error(
                `Backend returned HTTP ${response.status}: ${responseText}`
            );
        }

        let result;

        try {
            result = JSON.parse(responseText);
        } catch (error) {
            throw new Error("Backend returned invalid JSON.");
        }

        lastResult = result;

        renderResult(result);

    } catch (error) {

        console.error("ANALYSIS ERROR:", error);

        /*
         IMPORTANT:
         We DO NOT use the old 91% demo fallback anymore.
        */

        $("#results").classList.remove("hidden");

        $("#tag").textContent = "ANALYSIS FAILED";

        $("#title").textContent =
            "Unable to analyze this audio";

        $("#text").textContent =
            "The website could not get a valid response from the VoiceShield backend.";

        $("#score").textContent = "—";

        $("#bp").textContent = "—";

        $("#sp").textContent = "—";

        $("#conf").textContent = "—";

        $("#wins").textContent = "—";

        $("#device").textContent = "—";

        $("#model").textContent = "—";

        $("#windows").innerHTML = `
            <div class="empty">
                Backend error. Open the VS Code terminal
                and check the /predict request.
            </div>
        `;

        $("#explain").innerHTML = `
            <div class="why">
                <b>Backend error</b>
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;

        $("#raw").textContent = error.stack || error.message;

        alert(
            "Backend analysis failed.\n\n" +
            error.message +
            "\n\nCheck the VS Code terminal."
        );
    }

    button.disabled = false;

    button.textContent = "Analyze with VoiceShield →";
};


/* =========================
   RENDER BACKEND RESULT
========================= */

function renderResult(result) {

    $("#results").classList.remove("hidden");


    /* -------------------------
       Backend fields
    ------------------------- */

    const risk = Number(
        result.risk?.risk_score ?? 0
    );

    const verdict = String(
        result.verdict ?? "UNKNOWN"
    ).toUpperCase();

    const model = result.model ?? "AASIST";

    const device = result.device ?? "Unknown";

    const windows = result.windows ?? [];

    const indicators = result.indicators ?? [];

    const quality = result.quality ?? {};

    const decision = result.decision ?? {};

    const audio = result.audio ?? {};

    const performance = result.performance ?? {};


    /* -------------------------
       Main result
    ------------------------- */

    $("#score").textContent =
        Number.isFinite(risk)
            ? Math.round(risk)
            : "—";


    if ($("#ring")) {

        const percentage = Math.max(
            0,
            Math.min(100, risk)
        );

        const ringColor =
            verdict === "SPOOF"
                ? "#ff5c7a"
                : "#00d9a5";

        $("#ring").style.background =
            `conic-gradient(
                ${ringColor} ${percentage * 3.6}deg,
                #222936 0
            )`;
    }


    if (verdict === "SPOOF") {

        $("#tag").textContent =
            "SPOOF DETECTED";

        $("#title").textContent =
            "Potential synthetic / spoofed voice";

        $("#text").textContent =
            "AASIST detected evidence consistent with synthetic or spoofed audio.";

    } else if (verdict === "BONAFIDE") {

        $("#tag").textContent =
            "LIKELY BONAFIDE";

        $("#title").textContent =
            "Likely authentic voice";

        $("#text").textContent =
            "AASIST classified this recording as bonafide.";

    } else {

        $("#tag").textContent =
            "ANALYSIS COMPLETE";

        $("#title").textContent =
            "Voice analysis completed";

        $("#text").textContent =
            "The model returned an analysis result.";
    }


    /* =========================
       SPOOF / BONAFIDE SCORES
    ========================= */

    const meanSpoof =
        Number(result.risk?.mean_spoof_score ?? 0);

    const meanBonafide =
        100 - meanSpoof;


    $("#bp").textContent =
        meanBonafide.toFixed(1) + "%";

    $("#sp").textContent =
        meanSpoof.toFixed(1) + "%";


    if ($("#bb")) {

        $("#bb").style.width =
            Math.max(0, Math.min(100, meanBonafide)) + "%";
    }


    if ($("#sb")) {

        $("#sb").style.width =
            Math.max(0, Math.min(100, meanSpoof)) + "%";
    }


    /* =========================
       CONFIDENCE BAND
    ========================= */

    const confidenceBand =
        decision.confidence_band ?? "UNKNOWN";

    $("#conf").textContent =
        confidenceBand;


    /* =========================
       WINDOWS
    ========================= */

    $("#wins").textContent =
        windows.length || "0";


    $("#windows").innerHTML =
        windows.length
            ? windows.map((window, index) => {

                const spoofScore =
                    Number(window.spoof_score ?? 0) * 100;

                const bonafideScore =
                    Number(window.bonafide_score ?? 0) * 100;

                const label =
                    String(
                        window.label ?? "UNKNOWN"
                    ).toUpperCase();

                const start =
                    Number(window.start_seconds ?? 0);

                const end =
                    Number(window.end_seconds ?? 0);

                return `
                    <div class="window">

                        <div>
                            <b>W${index + 1}</b>

                            <span>
                                ${start.toFixed(2)}s -
                                ${end.toFixed(2)}s
                            </span>
                        </div>

                        <div class="mini">
                            <i
                                style="width:${Math.max(
                                    0,
                                    Math.min(100, spoofScore)
                                )}%"
                            ></i>
                        </div>

                        <div>
                            ${spoofScore.toFixed(1)}%
                            SPOOF
                            ·
                            ${bonafideScore.toFixed(1)}%
                            BONAFIDE
                        </div>

                        <strong>
                            ${label}
                        </strong>

                    </div>
                `;

            }).join("")
            : `
                <div class="empty">
                    No window-level data returned.
                </div>
            `;


    /* =========================
       EXPLAINABILITY
    ========================= */

    $("#explain").innerHTML =
        indicators.length
            ? indicators.map(indicator => {

                const severity =
                    String(
                        indicator.severity ?? "info"
                    ).toUpperCase();

                return `
                    <div class="why">

                        <b>
                            ${escapeHtml(
                                indicator.title ??
                                "Signal"
                            )}
                        </b>

                        <span>
                            ${severity}
                        </span>

                        <p>
                            ${escapeHtml(
                                indicator.detail ?? ""
                            )}
                        </p>

                    </div>
                `;

            }).join("")
            : `
                <div class="empty">
                    No explainability indicators returned.
                </div>
            `;


    /* =========================
       MODEL
    ========================= */

    $("#model").textContent =
        model;

    $("#device").textContent =
        device;


    /* =========================
       RAW RESULT
    ========================= */

    $("#raw").textContent =
        JSON.stringify(result, null, 2);


    /* =========================
       SAVE HISTORY
    ========================= */

    saveHistory({

        file:
            selectedFile?.name ??
            "Unknown",

        label:
            verdict,

        risk:
            risk,

        date:
            new Date().toLocaleString(),

        demo:
            false

    });


    /* =========================
       OPTIONAL DEBUG INFO
    ========================= */

    console.log("VoiceShield result:", result);

    console.log("Audio:", audio);

    console.log("Quality:", quality);

    console.log("Decision:", decision);

    console.log("Performance:", performance);


    /* =========================
       SHOW RESULTS
    ========================= */

    $("#results").scrollIntoView({
        behavior: "smooth"
    });
}


/* =========================
   HISTORY
========================= */

function saveHistory(entry) {

    let historyData =
        JSON.parse(
            localStorage.getItem("vs-history") || "[]"
        );

    historyData.unshift(entry);

    historyData =
        historyData.slice(0, 12);

    localStorage.setItem(
        "vs-history",
        JSON.stringify(historyData)
    );

    renderHistory();
}


function renderHistory() {

    const historyData =
        JSON.parse(
            localStorage.getItem("vs-history") || "[]"
        );

    if (!historyData.length) {

        $("#hist").innerHTML =
            '<div class="empty">No analyses yet.</div>';

        return;
    }


    $("#hist").innerHTML =
        historyData.map(entry => {

            const label =
                String(
                    entry.label ?? "UNKNOWN"
                ).toUpperCase();

            const className =
                label === "SPOOF"
                    ? "bad"
                    : "ok";

            return `
                <div class="histrow">

                    <b>
                        ${escapeHtml(
                            entry.file ?? "Unknown"
                        )}
                    </b>

                    <span>
                        ${escapeHtml(
                            entry.date ?? ""
                        )}
                    </span>

                    <span class="${className}">
                        ${label}
                        ·
                        Risk ${Number(
                            entry.risk ?? 0
                        ).toFixed(1)}
                    </span>

                </div>
            `;

        }).join("");
}


renderHistory();


/* =========================
   CLEAR HISTORY
========================= */

function clearHist() {

    localStorage.removeItem(
        "vs-history"
    );

    renderHistory();
}


/* =========================
   COPY RAW JSON
========================= */

$("#copy").onclick = async () => {

    try {

        await navigator.clipboard.writeText(
            $("#raw").textContent
        );

        alert("Analysis JSON copied.");

    } catch (error) {

        console.error(
            "Copy failed:",
            error
        );
    }
};


/* =========================
   HTML ESCAPE
========================= */

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}