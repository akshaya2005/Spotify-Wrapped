function showPopup(element) {
  // Get the modal and modal content elements
  const modal = document.getElementById("popupModal");
  const modalTitle = document.getElementById("modalTitle");
  const modalDetails = document.getElementById("modalDetails");

  // Get the title and details from the clicked card's data attributes
  const title = element.getAttribute("data-title");
  const details = element.getAttribute("data-details");


  // Set the content of the modal
  modalTitle.textContent = title;
  modalDetails.textContent = details;

  // Show the modal
  modal.style.display = 'flex';
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

function toggleDropdown() {

}

