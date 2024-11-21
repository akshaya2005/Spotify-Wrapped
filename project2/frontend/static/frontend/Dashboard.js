function showPopup(element) {
    // Get the modal and its content
    const modal = document.getElementById("popupModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalDetails = document.getElementById("modalDetails");

    // Get the data attributes
    const title = element.getAttribute("data-title");
    const details = element.getAttribute("data-details");

    // Set the modal content
    modalTitle.textContent = title;
    modalDetails.textContent = details;

    // Show the modal
    modal.style.display = 'flex';
}

function closePopup() {
    const modal = document.getElementById('popupModal');
    modal.style.display = 'none'; // Hide the modal
}

function showOptions() {
    const optionsModal = document.getElementById("options-modal");
    optionsModal.style.display = 'flex'; // Show the options modal
}

function closeOptionsPopup() {
    const optionsModal = document.getElementById("options-modal");
    optionsModal.style.display = 'none'; // Hide the options modal
}

// Close modal when clicking outside the content
window.onclick = function (event) {
    const popupModal = document.getElementById("popupModal");
    const optionsModal = document.getElementById("options-modal");

    if (event.target === popupModal) {
        popupModal.style.display = 'none';
    }

    if (event.target === optionsModal) {
        optionsModal.style.display = 'none';
    }
};
