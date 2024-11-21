

let currentSlideIndex = 0;
let slides = [];

function showPopup(element) {
  // Get the modal and modal content elements
  const modal = document.getElementById("popupModal");
  const modalTitle = document.getElementById("modalTitle");
  const slideContent = document.getElementById("slideContent");

  // Get the title and details from the clicked card's data attributes
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




