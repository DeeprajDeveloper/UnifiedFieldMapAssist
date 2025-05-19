// Table filter Functionality
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const searchButton = document.getElementById("search_button");
    const clearButton = document.getElementById("clear_button");
    const table = document.querySelector("table[id='content-table']");
    const rows = table.querySelectorAll("tbody tr");

    // Add event listener to the search input
    searchButton.addEventListener("click", () => {
        const query = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const cells = row.querySelectorAll("td");
            const rowText = Array.from(cells).map(cell => cell.textContent.toLowerCase()).join(" ");
            
            if (rowText.includes(query)) {
                row.style.display = ""; // Show the row
                // row.style.backgroundColor = "#fffeaa"; // Highlight the row
            } 
            else {
                row.style.display = "none";
                // row.style.backgroundColor = ""; // Hide the row
            }
        });
    });

    clearButton.addEventListener("click", () => {
        searchInput.value = "";
        rows.forEach((row) => {
            row.style.display = "";
        });
        showPage(1);
    });
});

// Pagination Functionality
let ROWS_PER_PAGE;
let MAX_PAGE_BUTTONS = 3;
let startPage = 1;
fetch("/api/v1/getConfig?searchParameter=rowCountPerPage", { method: "GET" })
    .then((response) => response.json()) // Parse the JSON response
    .then((configResponse) => {
        console.log("[API] Fetching GUI Config ...");
        ROWS_PER_PAGE = configResponse["dataExtract"]["configParameterValue"];
    })
    .then(() => {
        showPage(1); // Show the first page
    })
    .catch((error) => {
        console.error("[ERR] Error fetching config:", error);
        ROWS_PER_PAGE = 10;
    });


// Download Functionality
function downloadTemplate() {
    const a = document.createElement("a");
    a.href = "/gui/file/template"; // adjust for blueprint prefix
    a.download = ""; // needed for some browsers
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Add query param to refresh page with flash
    setTimeout(() => {
        window.location.href = "/gui/admin?download=true";
    }, 1000); // enough time to start download
}

// Hide all rows initially when the page loads
function showPage(page) {
    let table = document.querySelector("table[id='content-table']");
    let rows = table.querySelectorAll("tbody tr");
    let pageRowIdxStart = (page - 1) * ROWS_PER_PAGE;
    let pageRowIdxEnd = page * ROWS_PER_PAGE;
    // Hide all rows
    rows.forEach((row, idx) => {
        if (idx >= pageRowIdxStart && idx < pageRowIdxEnd) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
        row.style.backgroundColor = ""; // Remove highlight
    });
    displayPaginationControls(page, table, rows);
}

// Function to display pagination controls
function displayPaginationControls(activePageNumber, tableElement, tableRows) {
    let totalPages = Math.ceil(tableRows.length / ROWS_PER_PAGE);
    let paginationContainer = document.getElementById("pagination-container");
    let pagination = document.getElementById("pagination");

    if (!pagination) {
        pagination = document.createElement("div");
        pagination.id = "pagination";
        tableElement.parentNode.insertBefore(
            pagination,
            tableElement.nextSibling
        );
    }
    pagination.innerHTML = "";

    // Previous button
    const prevBtn = createButtonElement("Prev", "id", "page-button");
    prevBtn.disabled = startPage === 1;

    prevBtn.onclick = () => {
        if (startPage > 1) {
            startPage--;
            showPage(startPage);
        }
    };
    pagination.appendChild(prevBtn);

    // Calculate 5 buttons:
    let startPageNumber = activePageNumber;
    let endPageNumber = activePageNumber + (MAX_PAGE_BUTTONS - 1);
    let displayPageButtons = [];
    if (endPageNumber > totalPages) {
        endPageNumber = totalPages;
        startPageNumber = Math.max(1, endPageNumber - (MAX_PAGE_BUTTONS - 1));
    }
    for (let i = startPageNumber; i <= endPageNumber; i++) {
        displayPageButtons.push(i);
    }
    console.log(`[LOG] Curr. Page: ${activePageNumber} | Pagination: ${displayPageButtons}`);
    // Render page buttons
    displayPageButtons.forEach((i) => {
        const pageBtn = document.createElement("button");
        pageBtn.textContent = i;
        if (i === startPage) {
            pageBtn.disabled = true;
            pageBtn.setAttribute("id", "page-number-current");
        } else {
            pageBtn.setAttribute("id", "page-number");
        }
        pageBtn.onclick = () => {
            startPage = i;
            showPage(startPage);
        };
        pagination.appendChild(pageBtn);
    });
    // Next button
    const nextBtn = createButtonElement("Next", "id", "page-button");
    nextBtn.disabled = startPage === totalPages;

    nextBtn.onclick = () => {
        if (startPage < totalPages) {
            startPage++;
            showPage(startPage);
        }
    };
    pagination.appendChild(nextBtn);

    const pageInfo = document.createElement("span");
    pageInfo.textContent = `Page: ${startPage} of ${totalPages}`;
    pagination.appendChild(pageInfo);
    // Add pagination to the container
    paginationContainer.appendChild(pagination);
}

function updatePaginationForFilteredRows(filteredRows) {
    let pagination = document.getElementById("pagination");
    if (!pagination) return;
    pagination.innerHTML = "";
    // Previous button
    const prevBtn = document.createElement("button");
    prevBtn.textContent = "PREVIOUS";
    prevBtn.setAttribute("id", "page-button");
    prevBtn.disabled = startPage === 1;
    prevBtn.onclick = () => {
        if (startPage > 1) {
            startPage--;
            showFilteredPage(filteredRows, startPage);
        }
    };
    pagination.appendChild(prevBtn);
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        const pageBtn = document.createElement("button");
        pageBtn.textContent = i;
        pageBtn.setAttribute("id", "page-number");
        if (i === startPage) pageBtn.disabled = true;
        pageBtn.onclick = () => {
            startPage = i;
            showFilteredPage(filteredRows, startPage);
        };
        pagination.appendChild(pageBtn);
    }
    // Next button
    const nextBtn = document.createElement("button");
    nextBtn.textContent = "NEXT";
    nextBtn.setAttribute("id", "page-button");
    nextBtn.disabled = startPage === totalPages;
    nextBtn.onclick = () => {
        if (startPage < totalPages) {
            startPage++;
            showFilteredPage(filteredRows, startPage);
        }
    };
    pagination.appendChild(nextBtn);
}

function showFilteredPage(filteredRows, page) {
    filteredRows.forEach((row, idx) => {
        if (idx >= (page - 1) * ROWS_PER_PAGE && idx < page * ROWS_PER_PAGE) {
            row.style.display = "";
            row.style.backgroundColor = "#fffeaa";
        } else {
            row.style.display = "none";
            row.style.backgroundColor = "";
        }
    });
    updatePaginationForFilteredRows(filteredRows);
}

// Reusable function to create action control buttons for pagination.
function createButtonElement(buttonText, setterAttribute, attributeName) {
    let elementBtn = document.createElement("button");
    elementBtn.textContent = buttonText;
    elementBtn.setAttribute(setterAttribute, attributeName);
    return elementBtn;
}

