/*######################################################################
# File: LIDS_Dashboard.js
#
# Version: [5.0]
#
# Description: JavaScript file for managing the LIDS Dashboard web application.
#
# @Author:Arturo Olmos
# Added functionality for the buttons on the left sidebar
#
# Modification History:
# [11/01/23] - [3.0] - [Lizbeth Jurado] - [File Description and Organization Set Up]
#
# Tasks:
# - [Task 1]: Get forms and define state variables
# - [Task 2]: Handle events for showing the configuration file
# - [Task 3]: Handle events for displaying alerts table
# - [Task 4]: Define functions for toggling dropdowns
# - [Task 5]: Define a function to filter alerts by level
# - [Task 6]: Define a function for sorting the alerts table
# - [Task 7]: Fetch the user's IP address and display it in the header
# - [Task 8]: Define a function to remove sorting and reload the page
# - [Task 9]: Expose necessary functions globally
#
######################################################################*/

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
configFileForm.addEventListener("submit", (event) => {
    event.preventDefault();
    alertsTableState = middleContainer.innerHTML;
    middleContainer.innerHTML = xmlConfigState;
});

// Handles event when the user wants to see alerts displayed
alertsTableFrom.addEventListener("submit", (event) => {
    event.preventDefault();
    xmlConfigState = middleContainer.innerHTML;
    middleContainer.innerHTML = alertsTableState;
});

// Function to toggle dropdown
function toggleDropdown() {
    let dropdownContent = document.getElementById("sortByDropdownContent");
    if (dropdownContent.style.display === "none" || !dropdownContent.style.display) {
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
}

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

        // Populate other columns...
        // For example:
        // const timeCell = document.createElement("td");
        // timeCell.textContent = alert.time;
        // row.appendChild(timeCell);

        // Create a cell for PCAP data
        const pcapCell = document.createElement("td");
        pcapCell.textContent = alert.pcapLink; // Replace with the actual PCAP data

        // Append all cells to the row
        row.appendChild(pcapCell);

        // Append the row to the table body
        tbody.appendChild(row);
    });
}

// Function to remove sorting and reload the page
function removeSort() {
    location.reload();
}

// Expose functions globally
window.toggleDropdown = toggleDropdown;
window.sortTable = sortTable;
window.removeSort = removeSort;
window.filterAlerts = filterAlerts;
window.toggleFilterDropdown = toggleFilterDropdown;
