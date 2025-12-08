// main_app.js

// imports

// Select the elements
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

// Format time helper
const timeFormatter = (seconds) => {
    if (!seconds || isNaN(seconds)) return "00:00";
    let m = Math.floor(seconds / 60).toString().padStart(2, "0");
    let s = Math.floor(seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
};

let isPlaying = false;

// Unified play/pause function
function togglePlayPause() {
    if (isPlaying) {
        video.pause();
        playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
    } else {
        videoThumbnail.style.display = "none";
        video.play();
        playpause.innerHTML = '<i class="fa-solid fa-pause"></i>';
    }
}

// Play/pause button
playpause.addEventListener("click", togglePlayPause);

// Keybind for pausing and resuming video
document.addEventListener("keydown", (event) => {
    if (event.key === " " || event.key === "Spacebar") {
        event.preventDefault();
        togglePlayPause();
    }
});

// Keep pause/resume states in sync with original video
video.addEventListener("play", () => {
    isPlaying = true;
    playpause.innerHTML = '<i class="fa-solid fa-pause"></i>';
});

video.addEventListener("pause", () => {
    isPlaying = false;
    playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
});

// UI reset function
video.addEventListener("ended", () => {
    isPlaying = false;
    playpause.innerHTML = '<i class="fa-solid fa-play"></i>';
    progressBar.style.width = "0%";
    videoThumbnail.style.display = "block";
});

// Fast Forward and Rewind
frwd.addEventListener("click", () => {
    video.currentTime = Math.min(video.duration, video.currentTime + 5);
});

bkwrd.addEventListener("click", () => {
    video.currentTime = Math.max(0, video.currentTime - 5);
});

// Mute and unmute button
mutebtn.addEventListener("click", () => {
    video.muted = !video.muted;
    mutebtn.innerHTML = video.muted
        ? '<i class="fa-solid fa-volume-xmark"></i>'
        : '<i class="fas fa-volume-up"></i>';

    volume.value = video.muted ? 0 : video.volume;
});

// Keybind for mute function
document.addEventListener("keydown", (event) => {
    if (event.key.toLowerCase() === "m") {
        video.muted = !video.muted;
        mutebtn.innerHTML = video.muted
            ? '<i class="fa-solid fa-volume-xmark"></i>'
            : '<i class="fas fa-volume-up"></i>';

        volume.value = video.muted ? 0 : video.volume;
    }
});

// Volume slider
volume.addEventListener("input", () => {
    video.volume = volume.value;
    video.muted = video.volume === 0;

    mutebtn.innerHTML =
        video.muted
            ? '<i class="fa-solid fa-volume-xmark"></i>'
            : '<i class="fas fa-volume-up"></i>';
});

// Show controls while hovering over UI
videoContainer.addEventListener("mouseenter", () => {
    controls.style.opacity = 1;
});

videoContainer.addEventListener("mouseleave", () => {
    controls.style.opacity = 0;
});

// Update progress bar based on current video details (time/duration)
video.addEventListener("timeupdate", () => {
    const percentage = (video.currentTime / video.duration) * 100;
    progressBar.style.width = `${percentage}%`;
});

// Loads duration of the video once video metadata is available
video.addEventListener("loadedmetadata", () => {
    maxDuration.innerText = timeFormatter(video.duration);
});

// Update current time periodically
setInterval(() => {
    currentTimeRef.innerHTML = timeFormatter(video.currentTime);
}, 200);

// Seeking by clicking progress line
playbackline.addEventListener("click", (e) => {
    const rect = playbackline.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const progress = clickX / rect.width;

    video.currentTime = video.duration * progress;
});