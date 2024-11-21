console.log("spotifyLogin.js loaded");

document.getElementById("spotify-login-btn").onclick = function () {
  fetch("/spotify/get-auth-url/") // Request authentication URL from the backend
    .then((response) => response.json())
    .then((data) => {
      if (data.url) {
        // Redirect to Spotify's authentication page
        window.location.replace(data.url);
      } else {
        alert("Failed to get Spotify authorization URL");
      }
    })
    .catch((error) => console.error("Error:", error));
};

