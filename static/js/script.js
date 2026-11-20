
// Start Testing button

const startButton = document.getElementById("startButton");

startButton.addEventListener("click", function () {

    document.getElementById("modules").scrollIntoView({
        behavior: "smooth"
    });

    alert("Welcome to the Security Testing Modules!");

});


// Sidebar active navigation

const navigationLinks = document.querySelectorAll(".sidebar nav a");

navigationLinks.forEach(function(link) {

    link.addEventListener("click", function() {

        navigationLinks.forEach(function(item) {
            item.classList.remove("active");
        });

        this.classList.add("active");

    });

});
