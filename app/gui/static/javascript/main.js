// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const searchButton = document.getElementById("search_button");
    const clearButton = document.getElementById("clear_button");
    const table = document.querySelector("table");
    const rows = table.querySelectorAll("tbody tr");

    // Add event listener to the search input
    searchButton.addEventListener("click", () => {
        const query = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            const rowText = Array.from(cells).map(cell => cell.textContent.toLowerCase()).join(" ");
            
            if (rowText.includes(query)) {
                row.style.display = ""; // Show the row
                row.style.backgroundColor = "#fffeaa"; // Highlight the row
            } 
            else {
                row.style.backgroundColor = ""; // Hide the row
            }
        });
    });

    clearButton.addEventListener("click", () => {
        searchInput.value = "";
        rows.forEach((row) => {
            row.style.display = "";
            row.style.backgroundColor = "";
        });
    });
});

