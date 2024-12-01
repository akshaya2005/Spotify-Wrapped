// Global variables to manage slides and modal content
let currentSlideIndex = 0; // Index of the currently displayed slide
let slides = []; // Array to hold slide data
let currentWrapTitle = ""; // Store the current wrap title globally
let currentWrapType = ""; // Store the current wrap type globally
let currentTimePeriod = ""; // Store the current time period globally (default to medium-term)

/**
 * Displays a modal popup with slide content.
 * @param {HTMLElement} element - The HTML element that triggered the popup, containing slide data.
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
    currentTimePeriod = element.getAttribute("time_period")
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
    });    currentSlideIndex = 0; // Reset to the first slide

    // Set modal title and display the initial slide
    modalTitle.textContent = currentWrapTitle;
    renderCurrentSlide();

    // Show the modal
    modal.style.display = 'flex';

    // Update navigation button visibility
    updateSlideControls();
}

/**
 * Changes the current slide by a given direction.
 * @param {number} direction - The direction to move (1 for next, -1 for previous).
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
 * Renders the content of the current slide based on its type.
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
    } else if (currentWrapType === "top_artists") {
        const artistHTML = `
            <div class="slide main-slide">
                <p><strong>Artist Name:</strong> ${currentSlide.artist_name}</p>
                <p><strong>Popularity:</strong> ${currentSlide.popularity}</p>
                <p><strong>Genres:</strong> ${currentSlide.genres.join(", ")}</p>
                ${currentSlide.profile_picture ? `<img src="${currentSlide.profile_picture}" alt="Artist Profile Picture" style="width: 100px; height: auto;">` : ""}
            </div>`;
        slideContent.innerHTML = artistHTML;
    } else if (currentWrapType === "top_albums") {
        const albumHTML = `
            <div class="slide main-slide">
                <p><strong>Album Name:</strong> ${currentSlide.name}</p>
                <p><strong>Artists:</strong> ${currentSlide.artists.join(", ")}</p>
                <p><strong>Release Date:</strong> ${currentSlide.release_date}</p>
                <p><strong>Total Tracks:</strong> ${currentSlide.total_tracks}</p>
                ${currentSlide.album_cover ? `<img src="${currentSlide.album_cover}" alt="Album Cover" style="width: 100px; height: auto;">` : ""}
            </div>`;
        slideContent.innerHTML = albumHTML;
    } else if (currentWrapType === "top_genres") {
        const genreHTML = `
            <div class="slide main-slide">
                <p><strong>Genre:</strong> ${currentSlide.genre}</p>
                <p><strong>Count:</strong> ${currentSlide.count}</p>
            </div>`;
        slideContent.innerHTML = genreHTML;
    } else if (currentWrapType === "top_playlists") {
        const playlistHTML = `
            <div class="slide main-slide">
                <p><strong>Playlist Name:</strong> ${currentSlide.name}</p>
                <p><strong>Description:</strong> ${currentSlide.description}</p>
                <p><strong>Owner:</strong> ${currentSlide.owner}</p>
                <p><strong>Total Tracks:</strong> ${currentSlide.tracks_count}</p>
                ${currentSlide.playlist_cover ? `<img src="${currentSlide.playlist_cover}" alt="Playlist Cover" style="width: 100px; height: auto;">` : ""}
            </div>`;
        slideContent.innerHTML = playlistHTML;
    } else {
        slideContent.innerHTML = `<p>Unknown wrap type: ${currentWrapType}</p>`;
    }
}

/**
 * Updates the visibility and state of slide navigation controls.
 */
function updateSlideControls() {
    const prevButton = document.getElementById("prevSlide");
    const nextButton = document.getElementById("nextSlide");

    // Enable or disable buttons based on the current slide index
    prevButton.disabled = currentSlideIndex === 0;
    nextButton.disabled = currentSlideIndex === slides.length - 1;
}


/**
 * Closes the modal popup.
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
 * Closes the options modal.
 */
function closeOptionsPopup() {
    document.getElementById('options-modal').style.display = 'none';
}

const themeToggle = document.getElementById('theme-toggle');

// Check for saved theme in localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.body.classList.add('dark-mode');
  themeToggle.textContent = '☀️ Light Mode'; // Update toggle text
}

// Add event listener to toggle button
themeToggle.addEventListener('click', () => {
  const isDarkMode = document.body.classList.toggle('dark-mode');

  // Update button text based on mode
  themeToggle.textContent = isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode';

  // Save the selected theme in localStorage
  localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
});

document.addEventListener("DOMContentLoaded", function () {
  const userMenuToggle = document.querySelector(".user-menu-toggle");
  const userMenu = document.querySelector(".user-menu");
  const deleteAccountButton = document.querySelector(".delete-account-btn");
  const confirmDeleteModal = document.getElementById("confirm-delete-modal");

  // Toggle dropdown on username click
  userMenuToggle.addEventListener("click", function () {
    userMenu.classList.toggle("active");
  });

  deleteAccountButton.addEventListener("click", () => {
    confirmDeleteModal.style.display = "flex";
  });

  window.closeDeleteModal = function () {
    confirmDeleteModal.style.display = "none";
  };

  // Close dropdown if click occurs outside of user menu or dropdown
  document.addEventListener("click", function (event) {
    if (!userMenu.contains(event.target) && !userMenuToggle.contains(event.target)) {
      userMenu.classList.remove("active");
    }
  });
});

