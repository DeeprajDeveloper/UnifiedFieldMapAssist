// Pagination Functionality
let ROWS_PER_PAGE;

fetch("/api/v1/getConfig?searchParameter=rowCountPerPage", { method: "GET" })
    .then((response) => response.json()) // Parse the JSON response
    .then((configResponse) => {
        ROWS_PER_PAGE = configResponse["dataExtract"]["configParameterValue"];
    })
    .then(() => {
        let table = document.querySelector("table[id='content-table']");
        let rows = table.querySelectorAll("tbody tr");
        let currentPage = 1;
        let totalPages = Math.ceil(rows.length / ROWS_PER_PAGE);
        let paginationContainer = document.getElementById("pagination-container");

        // Hide all rows initially when the page loads
        function showPage(page) {
            // Hide all rows
            rows.forEach((row, idx) => {
                if (idx >= (page - 1) * ROWS_PER_PAGE && idx < page * ROWS_PER_PAGE) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
                row.style.backgroundColor = ""; // Remove highlight
            });
            updatePaginationControls();
        }

        function updatePaginationControls() {
            let pagination = document.getElementById("pagination");

            if (!pagination) {
                pagination = document.createElement("div");
                pagination.id = "pagination";
                table.parentNode.insertBefore(pagination, table.nextSibling);
            }
            pagination.innerHTML = "";
            // Previous button
            const prevBtn = document.createElement("button");
            prevBtn.textContent = "←";
            prevBtn.setAttribute("id", "page-button");

            prevBtn.disabled = currentPage === 1;

            prevBtn.onclick = () => {
                if (currentPage > 1) {
                    currentPage--;
                    showPage(currentPage);
                }
            };
            pagination.appendChild(prevBtn);

            // Page numbers logic
            const maxPageButtons = 5;
            let pageButtons = [];
            if (totalPages <= 10) {
                for (let i = 1; i <= totalPages; i++) {
                    pageButtons.push(i);
                }
            } else {
                // Always show first 5
                for (let i = 1; i <= maxPageButtons; i++) {
                    pageButtons.push(i);
                }
                // Show ... if needed
                if (currentPage >= maxPageButtons) {
                    pageButtons.push("...");
                }
                // Show 5 around current page if not near start/end
                let start = Math.max(6, currentPage - 1);
                let end = Math.min(totalPages - 4, currentPage + 1);

                console.log('--------------------------------------------');
                console.log(`Curr Page: ${currentPage}`);
                console.log(`Total Page: ${totalPages}`);
                console.log(`Start (min of ${currentPage}-2 / 6): ${start}`);
                console.log(`End (max of ${totalPages}-5 / ${currentPage}+3): ${end}`);
                console.log(`Displaying ${end - start + 1} buttons`);

                if (currentPage > 4 && currentPage < totalPages - 7) {
                    for (let i = start; i <= end; i++) pageButtons.push(i);
                    if (end < totalPages - 5) pageButtons.push("...");
                } else if (currentPage >= totalPages - 5) {
                    pageButtons.push("...");
                }
                // Always show last 5
                for (let i = totalPages - 4; i <= totalPages; i++) {
                    if (i > 5) pageButtons.push(i);
                }
            }
            // Render page buttons
            pageButtons.forEach((i) => {
                if (i === "...") {
                    const ellipsis = document.createElement("span");
                    ellipsis.textContent = "...";
                    ellipsis.style.margin = "0 4px";
                    pagination.appendChild(ellipsis);
                } else {
                    const pageBtn = document.createElement("button");
                    pageBtn.textContent = i;
                    if (i === currentPage) {
                        pageBtn.disabled = true;
                        pageBtn.setAttribute("id", "page-number-current");
                    } else {
                        pageBtn.setAttribute("id", "page-number");
                    }
                    pageBtn.onclick = () => {
                        currentPage = i;
                        showPage(currentPage);
                    };
                    pagination.appendChild(pageBtn);
                }
            });
            // Next button
            const nextBtn = document.createElement("button");
            nextBtn.textContent = "→";
            nextBtn.setAttribute("id", "page-button");

            nextBtn.disabled = currentPage === totalPages;

            nextBtn.onclick = () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    showPage(currentPage);
                }
            };
            pagination.appendChild(nextBtn);
            paginationContainer.appendChild(pagination);
        }

        // Initial pagination setup
        showPage(currentPage);

        function updatePaginationForFilteredRows(filteredRows) {
            let pagination = document.getElementById("pagination");
            if (!pagination) return;
            pagination.innerHTML = "";
            // Previous button
            const prevBtn = document.createElement("button");
            prevBtn.textContent = "PREVIOUS";
            prevBtn.setAttribute("id", "page-button");
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => {
                if (currentPage > 1) {
                    currentPage--;
                    showFilteredPage(filteredRows, currentPage);
                }
            };
            pagination.appendChild(prevBtn);
            // Page numbers
            for (let i = 1; i <= totalPages; i++) {
                const pageBtn = document.createElement("button");
                pageBtn.textContent = i;
                pageBtn.setAttribute("id", "page-number");
                if (i === currentPage) pageBtn.disabled = true;
                pageBtn.onclick = () => {
                    currentPage = i;
                    showFilteredPage(filteredRows, currentPage);
                };
                pagination.appendChild(pageBtn);
            }
            // Next button
            const nextBtn = document.createElement("button");
            nextBtn.textContent = "NEXT";
            nextBtn.setAttribute("id", "page-button");
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    showFilteredPage(filteredRows, currentPage);
                }
            };
            pagination.appendChild(nextBtn);
        }

        function showFilteredPage(filteredRows, page) {
            filteredRows.forEach((row, idx) => {
                if (
                    idx >= (page - 1) * ROWS_PER_PAGE &&
                    idx < page * ROWS_PER_PAGE
                ) {
                    row.style.display = "";
                    row.style.backgroundColor = "#fffeaa";
                } else {
                    row.style.display = "none";
                    row.style.backgroundColor = "";
                }
            });
            updatePaginationForFilteredRows(filteredRows);
        }
    })
    .catch((error) => {
        console.error("Error fetching config:", error);
        ROWS_PER_PAGE = 10;
    });

// Update pagination after search/clear
searchButton.addEventListener("click", () => {
    const query = searchInput.value.toLowerCase();
    let visibleRows = [];
    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        const rowText = Array.from(cells)
            .map((cell) => cell.textContent.toLowerCase())
            .join(" ");
        if (rowText.includes(query)) {
            visibleRows.push(row);
        }
    });
    // Only show filtered rows with pagination
    totalPages = Math.ceil(visibleRows.length / ROWS_PER_PAGE) || 1;
    currentPage = 1;
    rows.forEach((row) => (row.style.display = "none"));
    visibleRows.forEach((row, idx) => {
        if (idx < ROWS_PER_PAGE) row.style.display = "";
        else row.style.display = "none";
        row.style.backgroundColor = idx < ROWS_PER_PAGE ? "#fffeaa" : "";
    });
    updatePaginationControls();
    // Update pagination click to work with filtered rows
    updatePaginationForFilteredRows(visibleRows);
});

clearButton.addEventListener("click", () => {
    searchInput.value = "";
    totalPages = Math.ceil(rows.length / ROWS_PER_PAGE);
    currentPage = 1;
    showPage(currentPage);
});
