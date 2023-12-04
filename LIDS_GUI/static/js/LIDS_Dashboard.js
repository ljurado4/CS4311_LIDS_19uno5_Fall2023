/*
# File: LIDS_Dashboard.js
#
# Description: JavaScript file for managing the LIDS Dashboard web application.
#
# @ Author:Arturo Olmos
# Added functionality for the buttons on the left sidebar
# @ Author:Lizbeth Jurado
# Sorting functionality
#*/

// Get forms for event listeners
const middleContainer = document.getElementById("middleContainer");
const configFileForm = document.querySelector("#configFileForm");
const alertsTableFrom = document.querySelector("#alertsTableForm");
const disconnectForm = document.querySelector("#disconnectButtonForm");

// State variables for HTML
let alertsTableState = middleContainer.innerHTML;
// Formatting XML file output

let xmlConfigState = "<textarea class = \"xmlFileTextArea\">File Name: " + window.localStorage.getItem("xmlFileName") + "\n" + window.localStorage.getItem("xmlFile") + "</textarea>";
// Forms for event listeners

// Handles event when the user wants to see the config file
function viewXML(event){
    event.preventDefault();
    console.log("hello")
    window.location = "LIDS_XML_View"
}

// Handles event when the user wants to see alerts displayed
function viewAlerts(event) {
    event.preventDefault();
    window.location = "LIDS_Dashboard"
};

// Function to toggle dropdown
function toggleDropdown() {
    let dropdownContent = document.getElementById("sortByDropdownContent");
    if (dropdownContent.style.display === "none" || !dropdownContent.style.display) {
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
}
// @ Author:Lizbeth Jurado
// Function to filter alerts by level
function filterAlerts(filters) {
    let table = document.getElementById("alertBoxTable");
    let rows = Array.from(table.rows).slice(3); // skip the header

    rows.forEach(row => {
        let matchesFilter = true;

        // Filter by Level
        if (filters.level !== undefined && filters.level !== 5) {
            const alertLevel = parseInt(row.cells[2].textContent.trim());
            if (alertLevel > filters.level) {
                matchesFilter = false;
            }
        }

        // Filter by Source IP
        if (filters.sourceIP && row.cells[3].textContent.trim() !== filters.sourceIP) {
            matchesFilter = false;
        }

        // Filter by Source Port
        if (filters.sourcePort && row.cells[4].textContent.trim() !== filters.sourcePort) {
            matchesFilter = false;
        }

        // Filter by Destination IP
        if (filters.destinationIP && row.cells[5].textContent.trim() !== filters.destinationIP) {
            matchesFilter = false;
        }

        // Filter by Destination Port
        if (filters.destinationPort && row.cells[6].textContent.trim() !== filters.destinationPort) {
            matchesFilter = false;
        }

        // Filter by Alert Type
        if (filters.alertType && row.cells[7].textContent.trim() !== filters.alertType) {
            matchesFilter = false;
        }

        row.style.display = matchesFilter ? "" : "none";
    });
}
// @ modified:Lizbeth Jurado
// Function to toggle filter dropdown
function toggleFilterDropdown() {
    let dropdownContent = document.getElementById("filterByDropdownContent");
    if (dropdownContent.style.display === "none" || !dropdownContent.style.display) {
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
}

// Function to sort the alerts table
function sortTable(n) {
    let table = document.getElementById("alertBoxTable");
    let rows = Array.from(table.rows).slice(1); // skip the header
    rows.sort((r1, r2) => r1.cells[n].textContent.localeCompare(r2.cells[n].textContent));
    rows.forEach(row => table.tBodies[0].appendChild(row));
}

// Fetch the IP of the user when the document is ready
$(document).ready(() => {
    $.getJSON("https://api.ipify.org?format=json", (data) => {
        $("#headerTitle").text((i, originalText) => originalText + " " + data.ip);
    });

    // Simulated example data for alerts with PCAP links
    const exampleAlerts = [
        {
            // Populate other alert properties...
            pcapLink: "https://example.com/pcap1.pcap", // Replace with actual PCAP link
        },
        {
            // Populate other alert properties...
            pcapLink: "https://example.com/pcap2.pcap", // Replace with actual PCAP link
        },
        // Add more alerts as needed...
    ];

    // Populate the table with example alerts (replace with your data retrieval logic)
    populateTableWithData(exampleAlerts);
});

// Function to populate the alerts table with data, including PCAP links
function populateTableWithData(alerts) {
    const table = document.getElementById("alertBoxTable");
    const tbody = table.querySelector("tbody");

    // Clear existing rows
    tbody.innerHTML = "";

    // Iterate through alerts and populate rows
    alerts.forEach((alert) => {
        const row = document.createElement("tr");

        // Create a cell for PCAP data
        const pcapCell = document.createElement("td");
        pcapCell.textContent = alert.pcapLink; // Replace with the actual PCAP data

        // Append all cells to the row
        row.appendChild(pcapCell);

        // Append the row to the table body
        tbody.appendChild(row);
    });
}
// @ Author:Lizbeth Jurado
// Function to remove sorting and reload the page
function removeSort() {
    location.reload();
}

// @ Modifier: Lizbeth Jurado
// Expose functions globally
window.toggleDropdown = toggleDropdown;
window.sortTable = sortTable;
window.removeSort = removeSort;
window.filterAlerts = filterAlerts;
window.toggleFilterDropdown = toggleFilterDropdown;
