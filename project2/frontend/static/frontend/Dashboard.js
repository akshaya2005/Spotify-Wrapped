// Global variables to manage slides and modal content
let currentSlideIndex = 0; // Index of the currently displayed slide
let slides = []; // Array to hold slide data
let currentWrapTitle = ""; // Store the current wrap title globally
let currentWrapType = ""; // Store the current wrap type globally
let currentTimePeriod = ""; // Store the current time period globally (default to medium-term)

/**
 * Displays a modal popup with detailed content for a selected wrap item.
 * @param {HTMLElement} element - The HTML element triggering the modal popup.
 */
function showPopup(element) {
    if (event.target.classList.contains('delete-wrap-button')) {
        return; // Exit if the delete button is clicked, avoiding modal display
    }

    // Retrieve modal elements
    const modal = document.getElementById("popupModal");
    const modalTitle = document.getElementById("modalTitle");

    // Debug log for raw JSON data
    console.log("Raw JSON String:", element.getAttribute("data-details"));

    // Parse details from the triggering element
    const details = JSON.parse(element.getAttribute("data-details"));
    currentWrapType = element.getAttribute("data-wrap-type");
    currentTimePeriod = element.getAttribute("time_period");
    currentWrapTitle = element.getAttribute("data-title");

    // Convert wrap type to singular form
    const singularWrapType = (() => {
        switch (currentWrapType) {
            case "top_tracks":
                return "top track";
            case "top_artists":
                return "top artist";
            case "top_albums":
                return "top album";
            case "top_genres":
                return "top genre";
            case "top_playlists":
                return "top playlist";
            default:
                return currentWrapType.replace("_", " "); // Fallback
        }
    })();

    // Build slides with transitions
    const originalSlides = details.content;
    slides = [];
    originalSlides.forEach((item, index) => {
        slides.push({
            type: "transition",
            text: `Your #${originalSlides.length - index} most-listened-to ${singularWrapType} is...`,
        });
        slides.push(item); // Add the actual item after the transition
    });
    currentSlideIndex = 0; // Reset to the first slide

    // Set modal title and display the initial slide
    modalTitle.textContent = currentWrapTitle;
    renderCurrentSlide();

    // Show the modal
    modal.style.display = 'flex';

    // Update navigation button visibility
    updateSlideControls();
}

/**
 * Navigates between slides in the modal.
 * @param {number} direction - The slide direction (1 for next, -1 for previous).
 */
function changeSlide(direction) {
    currentSlideIndex += direction; // Update the current slide index

    // Ensure the index is within bounds
    if (currentSlideIndex < 0) {
      currentSlideIndex = 0;
    } else if (currentSlideIndex >= slides.length) {
      currentSlideIndex = slides.length - 1;
    }

    renderCurrentSlide(); // Render the updated slide
    updateSlideControls(); // Update navigation controls
}

/**
 * Renders the content of the currently active slide.
 */
function renderCurrentSlide() {
    const slideContent = document.getElementById("slideContent");
    const currentSlide = slides[currentSlideIndex]; // Get the current slide data

    // Clear previous content
    slideContent.innerHTML = "";

    // Render based on wrap type
    if (currentSlide.type === "transition") {
        slideContent.innerHTML = `<div class="slide transition-slide" style="text-align: center; font-size: 1.5em;">
            <p>${currentSlide.text}</p>
        </div>`;
    } else if (currentWrapType === "top_tracks") {
        const trackHTML = `
            <div class="slide main-slide">
                <p><strong>Name:</strong> ${currentSlide.name}</p>
                <p><strong>Artists:</strong> ${currentSlide.artists}</p>
                <p><strong>Album:</strong> ${currentSlide.album}</p>
                ${currentSlide.album_cover ? `<img src="${currentSlide.album_cover}" alt="Album Cover" style="width: 100px; height: auto;">` : ""}
                ${currentSlide.preview_url ? `
                    <audio controls>
                        <source src="${currentSlide.preview_url}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>` : ""}
            </div>`;
        slideContent.innerHTML = trackHTML;
    }
    // Additional conditions for other wrap types...
}

/**
 * Updates the visibility and state of slide navigation buttons.
 */
function updateSlideControls() {
    const prevButton = document.getElementById("prevSlide");
    const nextButton = document.getElementById("nextSlide");

    // Enable or disable buttons based on the current slide index
    prevButton.disabled = currentSlideIndex === 0;
    nextButton.disabled = currentSlideIndex === slides.length - 1;
}

/**
 * Closes the currently open modal popup.
 */
function closePopup() {
    document.getElementById('popupModal').style.display = 'none';
}

/**
 * Displays the options modal.
 */
function showOptions() {
    const modal = document.getElementById("options-modal");
    modal.style.display = 'flex';
}

/**
 * Closes the options modal popup.
 */
function closeOptionsPopup() {
    document.getElementById('options-modal').style.display = 'none';
}
