let currentSlideIndex = 0;
let slides = [];
let currentWrapTitle = ""; // Store the current wrap title globally
let currentWrapType = "";

function showPopup(element) {
    if (event.target.classList.contains('delete-wrap-button')) {
        return; // Exit the function, do not expand the wrap card
  }
  // Get the modal and modal content elements
  const modal = document.getElementById("popupModal");
  const modalTitle = document.getElementById("modalTitle");
  const slideContent = document.getElementById("slideContent");
  console.log("Raw JSON String:", element.getAttribute("data-details"));

  const details = JSON.parse(element.getAttribute("data-details"));

  currentWrapType = element.getAttribute("data-wrap-type");
  currentWrapTitle = element.getAttribute("data-title");


  slides = details.content; // Example: Use '|' as a delimiter for multiple slides
  currentSlideIndex = 0; // Start at the first slide

  // Set the modal title and initial slide content
  modalTitle.textContent = currentWrapTitle;
  renderCurrentSlide()


  // Show the modal
  modal.style.display = 'flex';

  // Update navigation button visibility
  updateSlideControls();

}
function changeSlide(direction) {
  //const slideContent = document.getElementById("slideContent");

  // Update the current slide index
  currentSlideIndex += direction;

  // Ensure the index is within bounds
  if (currentSlideIndex < 0) {
    currentSlideIndex = 0;
  } else if (currentSlideIndex >= slides.length) {
    currentSlideIndex = slides.length - 1;
  }

  // Update the slide content

  renderCurrentSlide();

  // Update navigation button visibility
  updateSlideControls();
}


function renderCurrentSlide(title) {
  const slideContent = document.getElementById("slideContent");
  const currentSlide = slides[currentSlideIndex];

  // Clear previous content
  slideContent.innerHTML = "";

  if (currentWrapType === "top_tracks") {
    // Render top tracks
    const trackHTML = `
      <div>
        <p><strong>Name:</strong> ${currentSlide.name}</p>
        <p><strong>Artists:</strong> ${currentSlide.artists}</p>
        <p><strong>Album:</strong> ${currentSlide.album}</p>
        ${
          currentSlide.album_cover
            ? `<img src="${currentSlide.album_cover}" alt="Album Cover" style="width: 100px; height: auto;">`
            : ""
        }
        ${
          currentSlide.preview_url
            ? `
            <audio controls>
              <source src="${currentSlide.preview_url}" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>
            `
            : ""
        }
      </div>
    `;
    slideContent.innerHTML = trackHTML;

  } else if (currentWrapType === "top_artists") {
    // Render top artists
    const artistHTML = `
      <div>
        <p><strong>Artist Name:</strong> ${currentSlide.artist_name}</p>
        <p><strong>Popularity:</strong> ${currentSlide.popularity}</p>
        <p><strong>Genres:</strong> ${currentSlide.genres.join(", ")}</p>
        ${
          currentSlide.profile_picture
            ? `<img src="${currentSlide.profile_picture}" alt="Artist Profile Picture" style="width: 100px; height: auto;">`
            : ""
        }
      </div>
    `;
    slideContent.innerHTML = artistHTML;

  } else if (currentWrapType === "top_albums") {
    // Render top albums
    const albumHTML = `
      <div>
        <p><strong>Album Name:</strong> ${currentSlide.name}</p>
        <p><strong>Artists:</strong> ${currentSlide.artists.join(", ")}</p>
        <p><strong>Release Date:</strong> ${currentSlide.release_date}</p>
        <p><strong>Total Tracks:</strong> ${currentSlide.total_tracks}</p>
        ${
          currentSlide.album_cover
            ? `<img src="${currentSlide.album_cover}" alt="Album Cover" style="width: 100px; height: auto;">`
            : ""
        }
      </div>
    `;
    slideContent.innerHTML = albumHTML;

  } else if (currentWrapType === "top_genres") {
    // Render top genres
    const genreHTML = `
      <div>
        <p><strong>Genre:</strong> ${currentSlide.genre}</p>
        <p><strong>Count:</strong> ${currentSlide.count}</p>
      </div>
    `;
    slideContent.innerHTML = genreHTML;

  } else if (currentWrapType === "top_playlists") {
    // Render top playlists
    const playlistHTML = `
      <div>
        <p><strong>Playlist Name:</strong> ${currentSlide.name}</p>
        <p><strong>Description:</strong> ${currentSlide.description}</p>
        <p><strong>Owner:</strong> ${currentSlide.owner}</p>
        <p><strong>Total Tracks:</strong> ${currentSlide.tracks_count}</p>
        ${
          currentSlide.playlist_cover
            ? `<img src="${currentSlide.playlist_cover}" alt="Playlist Cover" style="width: 100px; height: auto;">`
            : ""
        }
      </div>
    `;
    slideContent.innerHTML = playlistHTML;

  } else {
    slideContent.innerHTML = `<p>Unknown wrap type: ${currentWrapType}</p>`;
  }
}

function updateSlideControls() {
  const prevButton = document.getElementById("prevSlide");
  const nextButton = document.getElementById("nextSlide");

  // Disable/enable buttons based on slide index
  prevButton.disabled = currentSlideIndex === 0;
  nextButton.disabled = currentSlideIndex === slides.length - 1;
}


function closePopup() {
      // Hide the modal
    document.getElementById('popupModal').style.display = 'none';
}

function showOptions() {
    const modal = document.getElementById("options-modal")
    modal.style.display = 'block';
}

function closeOptionsPopup() {
    document.getElementById('options-modal').style.display ='none';
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
