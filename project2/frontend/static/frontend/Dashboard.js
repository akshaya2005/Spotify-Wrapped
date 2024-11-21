function showPopup(title, details) {
  // Set the title and details in the modal
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalDetails').innerText = details;

      // Show the modal
      document.getElementById('popupModal').style.display = 'flex';
    }

    function closePopup() {
      // Hide the modal
      document.getElementById('popupModal').style.display = 'none';
    }


