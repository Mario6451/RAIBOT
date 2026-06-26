// ======================================================
// RAIBOT XP UI CORE
// ======================================================

// ------------------------------
// LOGGING SYSTEM
// ------------------------------
function addLog(text) {
    const log = document.getElementById("log-output");
    log.textContent += text + "\n";
    log.scrollTop = log.scrollHeight;
}

addLog("RAIBOT Web UI initialized.");


// ======================================================
// XP WINDOW BUTTON LOGIC
// ======================================================

function attachWindowControls() {
    document.querySelectorAll(".xp-window").forEach(win => {
        const content = win.querySelector(".xp-content");
        const btnMin = win.querySelector(".xp-min");
        const btnMax = win.querySelector(".xp-max");
        const btnClose = win.querySelector(".xp-close");

        if (btnMin) {
            btnMin.addEventListener("click", () => {
                content.style.display =
                    content.style.display === "none" ? "block" : "none";
                addLog("[UI] Minimize toggle");
            });
        }

        if (btnMax) {
            btnMax.addEventListener("click", () => {
                if (!win.classList.contains("xp-maximized")) {
                    win.dataset.prevLeft = win.style.left;
                    win.dataset.prevTop = win.style.top;
                    win.dataset.prevWidth = win.style.width;
                    win.dataset.prevHeight = win.style.height;

                    win.style.position = "absolute";
                    win.style.left = "0px";
                    win.style.top = "0px";
                    win.style.width = "100%";
                    win.style.height = "100%";

                    win.classList.add("xp-maximized");
                } else {
                    win.style.left = win.dataset.prevLeft;
                    win.style.top = win.dataset.prevTop;
                    win.style.width = win.dataset.prevWidth;
                    win.style.height = win.dataset.prevHeight;

                    win.classList.remove("xp-maximized");
                }
                addLog("[UI] Maximize toggle");
            });
        }

        if (btnClose) {
            btnClose.addEventListener("click", () => {
                win.style.display = "none";
                addLog("[UI] Window closed");
            });
        }
    });
}

attachWindowControls();


// ======================================================
// DRAGGABLE WINDOWS
// ======================================================

function makeWindowsDraggable() {
    let activeWindow = null;
    let offsetX = 0;
    let offsetY = 0;

    document.querySelectorAll(".xp-window").forEach(win => {
        const titlebar = win.querySelector(".xp-titlebar");
        if (!titlebar) return;

        titlebar.style.cursor = "move";

        titlebar.addEventListener("mousedown", (e) => {
            activeWindow = win;

            // Bring to front
            win.style.zIndex = (parseInt(win.style.zIndex) || 10) + 1000;

            // Calculate offset
            const rect = win.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;

            addLog("[UI] Drag start");
        });
    });

    document.addEventListener("mousemove", (e) => {
        if (!activeWindow) return;

        activeWindow.style.position = "absolute";
        activeWindow.style.left = (e.clientX - offsetX) + "px";
        activeWindow.style.top = (e.clientY - offsetY) + "px";
    });

    document.addEventListener("mouseup", () => {
        if (activeWindow) {
            addLog("[UI] Drag end");
        }
        activeWindow = null;
    });
}

makeWindowsDraggable();


// ======================================================
// TAB SWITCHING
// ======================================================

function switchMainTab(tab) {
    const panel = document.getElementById("main-panel");

    const templates = {
        Dashboard: `
            <h2>Dashboard</h2>
            <p>Overview of RAIBOT status, bots, and recent activity.</p>
        `,
        Bots: `
            <h2>Bot Manager</h2>
            <p>List of bots, their states, and controls will appear here.</p>
        `,
        Training: `
            <h2>Training</h2>
            <p>Self-learning, imitation, and instruction training controls.</p>
        `,
        Analytics: `
            <h2>Analytics</h2>
            <p>Performance metrics, pathfinding stats, and behavior analytics.</p>
        `,
        Logs: `
            <h2>Logs</h2>
            <p>Runtime logs are shown in the bottom panel.</p>
        `,
        Chat: `
            <h2>Chat Monitor</h2>
            <p>Live chat feed and AI responses.</p>
        `,
        Map: `
            <h2>Map</h2>
            <p>Detailed bot map view (mini-map on the right).</p>
        `,
        Pathfinding: `
            <h2>Pathfinding</h2>
            <p>Path grid, waypoints, and navigation debugging.</p>
        `,
        Camera: `
            <h2>Camera</h2>
            <p>Camera feed and vision debugging.</p>
        `,
        Personality: `
            <h2>Personality Designer</h2>
            <p>Traits, styles, and behavior tuning.</p>
        `,
        Settings: `
            <h2>Settings</h2>
            <p>RAIBOT configuration and integration options.</p>
        `
    };

    panel.innerHTML = templates[tab] || `<h2>${tab}</h2><p>Not implemented.</p>`;
    addLog(`[UI] Switched main tab to: ${tab}`);
}


// ======================================================
// MINI MAP RENDERING
// ======================================================

const canvas = document.getElementById("map-canvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    drawDemoBots();
}

function drawDemoBots() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Grid
    ctx.strokeStyle = "#cccccc";
    for (let x = 0; x < canvas.width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // Demo bots
    const bots = [
        { x: 40, y: 60 },
        { x: 120, y: 140 },
        { x: 200, y: 80 }
    ];

    ctx.fillStyle = "red";
    bots.forEach(bot => {
        ctx.fillRect(bot.x - 3, bot.y - 3, 6, 6);
    });

    addLog("[Map] Demo bots drawn on mini-map.");
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
