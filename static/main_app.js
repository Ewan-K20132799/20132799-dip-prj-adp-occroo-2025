// main_app.js

// -------------------- Select elements --------------------
const video = document.getElementById("video");
const videoThumbnail = document.getElementById("video-thumbnail");
const playpause = document.getElementById("play-pause");
const frwd = document.getElementById("skip-10");
const bkwrd = document.getElementById("skip-minus-10");
const volume = document.getElementById("volume");
const mutebtn = document.getElementById("mute");
const videoContainer = document.querySelector(".video-container");
const controls = document.querySelector(".controls");
const progressBar = document.querySelector(".progress-bar");
const playbackline = document.querySelector(".playback-line");
const currentTimeRef = document.getElementById("current-time");
const maxDuration = document.getElementById("max-duration");

// Always use the latest video
video.src = "/resources/current-video";
video.load();
video.style.display = "block";

let isPlaying = false;

// -------------------- Helpers --------------------
const timeFormatter = (seconds) => {
    if (!seconds || isNaN(seconds)) return "00:00";
    const m = Math.floor(seconds / 60).toString().padStart(2, "0");
    const s = Math.floor(seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
};

const updateMuteIcon = () => {
    mutebtn.innerHTML = video.muted || video.volume === 0
        ? '<i class="fa-solid fa-volume-xmark"></i>'
        : '<i class="fas fa-volume-up"></i>';
};

// -------------------- Play/Pause --------------------
const togglePlayPause = () => {
    if (isPlaying) {
        video.pause();
        playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
    } else {
        videoThumbnail.style.display = "none";
        video.play();
        playpause.innerHTML = '<i class="fa-solid fa-pause"></i>';
    }
};
playpause.addEventListener("click", togglePlayPause);
document.addEventListener("keydown", (event) => {
    if (event.key === " " || event.key === "Spacebar") {
        event.preventDefault();
        togglePlayPause();
    }
});
video.addEventListener("play", () => {
    isPlaying = true;
    playpause.innerHTML = '<i class="fa-solid fa-pause"></i>';
    videoThumbnail.style.display = "none";
});
video.addEventListener("pause", async () => {
    isPlaying = false;
    playpause.innerHTML = '<i class="fa-solid fa-play"></i>';

    const currentTime = Math.floor(video.currentTime);
    try {
        const response = await fetch("/api/generate-ocr", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({seconds: currentTime})
        });

        if (!response.ok) {
            console.warn(`OCR request failed: ${response.status}`);
            return;
        }

        const data = await response.json();
        const ocrOutput = document.getElementById("ocr-output");
        if (ocrOutput) ocrOutput.textContent = data.ocr_text;

    } catch (error) {
        console.error("Failed to generate OCR:", error);
    }
});

// -------------------- Video End --------------------
video.addEventListener("ended", () => {
    isPlaying = false;
    playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
    progressBar.style.width = "0%";
    videoThumbnail.style.display = "block";
});

// -------------------- Skip --------------------
frwd.addEventListener("click", () => video.currentTime = Math.min(video.duration, video.currentTime + 5));
bkwrd.addEventListener("click", () => video.currentTime = Math.max(0, video.currentTime - 5));

// -------------------- Volume --------------------
mutebtn.addEventListener("click", () => {
    video.muted = !video.muted;
    updateMuteIcon();
    volume.value = video.muted ? 0 : video.volume;
});
document.addEventListener("keydown", (event) => {
    if (event.key.toLowerCase() === "m") {
        video.muted = !video.muted;
        updateMuteIcon();
        volume.value = video.muted ? 0 : video.volume;
    }
});
volume.addEventListener("input", () => {
    video.volume = volume.value;
    video.muted = video.volume === 0;
    updateMuteIcon();
});

// -------------------- Controls visibility --------------------
videoContainer.addEventListener("mouseenter", () => controls.style.opacity = 1);
videoContainer.addEventListener("mouseleave", () => controls.style.opacity = 0);

// -------------------- Progress bar --------------------
video.addEventListener("timeupdate", () => {
    progressBar.style.width = `${(video.currentTime / video.duration) * 100}%`;
});
video.addEventListener("loadedmetadata", () => {
    maxDuration.innerText = timeFormatter(video.duration);
});
setInterval(() => currentTimeRef.innerText = timeFormatter(video.currentTime), 200);
playbackline.addEventListener("click", (e) => {
    const rect = playbackline.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    video.currentTime = video.duration * (clickX / rect.width);
});

// -------------------- OCR Buttons --------------------
document.querySelector(".ocr button:nth-child(1)").addEventListener("click", async () => {
    const seconds = Math.floor(video.currentTime);
    const res = await fetch("/api/generate-ocr", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({seconds})
    });
    const data = await res.json();
    const ocrOutput = document.getElementById("ocr-output");
    if (ocrOutput) ocrOutput.textContent = data.ocr_text;
});

document.querySelector(".ocr button:nth-child(2)").addEventListener("click", async () => {
    const seconds = Math.floor(video.currentTime);
    const filename = prompt("Enter filename for OCR text:", "ocr_output") || "ocr_output";

    const response = await fetch("/api/save-ocr-as-txt", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({seconds, filename})
    });

    if (!response.ok) return alert("Failed to save OCR!");
    const data = await response.json();
    alert(`OCR saved to: ${data.saved_path}`);
});

// -------------------- Load New Video --------------------
document.querySelector(".ocr button:nth-child(3)").addEventListener("click", async () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "video/*";
    fileInput.click();

    fileInput.onchange = async () => {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/api/load-video", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            if (!response.ok || data.error) {
                console.warn("Video load failed:", data?.error);
                alert(`Video load failed: ${data?.error || "Unknown error"}`);
                return;
            }

            // Reload video from current-video endpoint
            setTimeout(() => {
                video.src = "/resources/current-video";
                video.load();
                videoThumbnail.style.display = "block";
                progressBar.style.width = "0%";
                currentTimeRef.innerText = "00:00";
                maxDuration.innerText = "00:00";
                isPlaying = false;
                playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
            }, 1000);

            alert("Video loaded successfully!");
        } catch (err) {
            console.error("Failed to load video:", err);
            alert("Failed to load video. Check console for details.");
        }
    };
});
