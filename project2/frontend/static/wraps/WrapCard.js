let currentSlideIndex = 0;

function openSlideshowModal(title, slides) {
  // Set the title in the modal
  document.getElementById('modalTitle').innerText = title;

  // Populate the slideshow container with slides
  const slideshowContainer = document.getElementById('modalDetails');
  slideshowContainer.innerHTML = ''; // Clear any previous slides

  slides.forEach((slide, index) => {
    const slideDiv = document.createElement('div');
    slideDiv.className = 'slide';
    slideDiv.style.display = index === 0 ? 'block' : 'none'; // Show only the first slide initially
    slideDiv.innerHTML = `
      <p>${slide}</p>
    `;
    slideshowContainer.appendChild(slideDiv);
  });

  // Show the modal
  document.getElementById('popupModal').style.display = 'flex';
  currentSlideIndex = 0; // Reset to the first slide
}

function closeSlideshowModal() {
  // Hide the modal
  document.getElementById('popupModal').style.display = 'none';
}

function changeSlide(n) {
  const slides = document.querySelectorAll('#modalDetails .slide');
  slides[currentSlideIndex].style.display = 'none';
  currentSlideIndex = (currentSlideIndex + n + slides.length) % slides.length;
  slides[currentSlideIndex].style.display = 'block';
}

// Export functions for use in other files
export { openSlideshowModal, closeSlideshowModal, changeSlide };

window.closeSlideshowModal = closeSlideshowModal;
window.changeSlide = changeSlide;
window.showPopup = showPopup;