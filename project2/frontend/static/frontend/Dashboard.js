let currentSlideIndex = 0;
let slides = [];

function showPopup(element) {
  // Get the modal and modal content elements
  const modal = document.getElementById("popupModal");
  const modalTitle = document.getElementById("modalTitle");
  const slideContent = document.getElementById("slideContent");

    // Get the data attributes
    const title = element.getAttribute("data-title");
    const details = element.getAttribute("data-details");

  slides = details.split('},'); // Example: Use '|' as a delimiter for multiple slides
  currentSlideIndex = 0; // Start at the first slide

  // Set the modal title and initial slide content
  modalTitle.textContent = title;
  slideContent.textContent = slides[currentSlideIndex];

  // Show the modal
  modal.style.display = 'flex';

  // Update navigation button visibility
  updateSlideControls();

}
function changeSlide(direction) {
  const slideContent = document.getElementById("slideContent");

  // Update the current slide index
  currentSlideIndex += direction;

  // Ensure the index is within bounds
  if (currentSlideIndex < 0) {
    currentSlideIndex = 0;
  } else if (currentSlideIndex >= slides.length) {
    currentSlideIndex = slides.length - 1;
  }

  // Update the slide content
  slideContent.textContent = slides[currentSlideIndex];

  // Update navigation button visibility
  updateSlideControls();
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

function createWrap() {
    // Get the selected wrap type
    const wrapDropdown = document.getElementById("wrapTypeDropdown");
    const selectedWrap = wrapDropdown.value;

    // Get the selected time period
    const timeDropdown = document.getElementById("timePeriodDropdown");
    const selectedTimePeriod = timeDropdown.value;

    // Add logic to handle the wrap creation
    console.log(`Creating wrap for: ${selectedWrap}, Time Period: ${selectedTimePeriod}`);

    // Close the modal
    closeOptionsPopup();

    // Optionally, provide feedback to the user
    alert(`Wrap for ${wrapDropdown.options[wrapDropdown.selectedIndex].text} over ${timeDropdown.options[timeDropdown.selectedIndex].text} is being created!`);
}