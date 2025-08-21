// Map functionality for Mapping the Gay Guides

let map;
let markers = [];
let currentData = [];

document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadLocations();
    setupEventListeners();
});

function initializeMap() {
    // Initialize the map centered on the US
    map = L.map('map').setView([39.8283, -98.5795], 4);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function loadLocations() {
    // Fetch locations from the API
    fetch('/api/locations')
        .then(response => response.json())
        .then(data => {
            currentData = data;
            displayLocations(data);
            populateFilters(data);
        })
        .catch(error => {
            console.error('Error loading locations:', error);
            document.getElementById('location-details').innerHTML = 
                '<p class="text-danger">Error loading map data. Please try again later.</p>';
        });
}

function displayLocations(locations) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Add new markers
    locations.forEach(location => {
        if (location.latitude && location.longitude) {
            const marker = L.marker([location.latitude, location.longitude])
                .bindPopup(createPopupContent(location))
                .addTo(map);
            
            marker.on('click', () => showLocationDetails(location));
            markers.push(marker);
        }
    });
}

function createPopupContent(location) {
    return `
        <div class="popup-content">
            <h6>${location.name}</h6>
            <p><strong>Category:</strong> ${location.category || 'N/A'}</p>
            <p><strong>Year:</strong> ${location.year_listed || 'N/A'}</p>
            <p><strong>Location:</strong> ${location.city}, ${location.state}</p>
        </div>
    `;
}

function showLocationDetails(location) {
    const detailsDiv = document.getElementById('location-details');
    detailsDiv.innerHTML = `
        <h6>${location.name}</h6>
        <p><strong>Address:</strong> ${location.address || 'N/A'}</p>
        <p><strong>City:</strong> ${location.city || 'N/A'}</p>
        <p><strong>State:</strong> ${location.state || 'N/A'}</p>
        <p><strong>Category:</strong> ${location.category || 'N/A'}</p>
        <p><strong>Year Listed:</strong> ${location.year_listed || 'N/A'}</p>
        <p><strong>Guide Edition:</strong> ${location.guide_edition || 'N/A'}</p>
        ${location.description ? `<p><strong>Description:</strong> ${location.description}</p>` : ''}
        ${location.notes ? `<p><strong>Notes:</strong> ${location.notes}</p>` : ''}
    `;
}

function populateFilters(data) {
    // Populate state filter
    const states = [...new Set(data.map(loc => loc.state).filter(Boolean))].sort();
    const stateFilter = document.getElementById('state-filter');
    
    states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateFilter.appendChild(option);
    });
}

function setupEventListeners() {
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
}

function applyFilters() {
    const category = document.getElementById('category-filter').value;
    const year = document.getElementById('year-filter').value;
    const state = document.getElementById('state-filter').value;
    
    let filteredData = currentData;
    
    if (category) {
        filteredData = filteredData.filter(loc => loc.category === category);
    }
    
    if (year) {
        const decade = parseInt(year.replace('s', ''));
        filteredData = filteredData.filter(loc => {
            if (!loc.year_listed) return false;
            return loc.year_listed >= decade && loc.year_listed < decade + 10;
        });
    }
    
    if (state) {
        filteredData = filteredData.filter(loc => loc.state === state);
    }
    
    displayLocations(filteredData);
    
    // Update location details if no locations found
    if (filteredData.length === 0) {
        document.getElementById('location-details').innerHTML = 
            '<p class="text-muted">No locations match the selected filters</p>';
    }
}
