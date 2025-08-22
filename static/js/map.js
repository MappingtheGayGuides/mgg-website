// Map functionality for Mapping the Gay Guides

let map;
let markerClusterGroup;
let currentData = [];
let locationTypes = [];
let currentYear = 1965;

document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadData();
    setupEventListeners();
});

function initializeMap() {
    // Initialize the map centered on the US
    map = L.map('map').setView([39.8283, -98.5795], 4);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Initialize marker cluster group
    markerClusterGroup = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 60,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: true,
        zoomToBoundsOnClick: true,
        animate: true,
        animateAddingMarkers: true,
        chunkInterval: 200,
        chunkDelay: 50
    });
    map.addLayer(markerClusterGroup);
}

function loadData() {
    // Load locations and types in parallel
    Promise.all([
        fetch('/api/locations').then(response => response.json()),
        fetch('/api/location-types').then(response => response.json())
    ])
    .then(([locationsData, typesData]) => {
        currentData = locationsData;
        locationTypes = typesData;
        
        // Filter by current year and display
        const filteredData = filterByYear(currentData, currentYear);
        displayLocations(filteredData);
        populateFilters();
        
        // Update year display
        document.getElementById('year-display').textContent = currentYear;
    })
    .catch(error => {
        console.error('Error loading data:', error);
        document.getElementById('location-details').innerHTML = 
            '<p class="text-danger">Error loading map data. Please try again later.</p>';
    });
}

function filterByYear(locations, year) {
    return locations.filter(location => {
        if (!location.year) return false;
        return location.year === year;
    });
}

function displayLocations(locations) {
    // Clear existing markers from cluster group
    markerClusterGroup.clearLayers();
    
    // Add new markers to cluster group
    locations.forEach(location => {
                if (location.latitude && location.longitude) {
            const marker = L.marker([location.latitude, location.longitude]);

            marker.on('click', () => showLocationDetails(location));
            markerClusterGroup.addLayer(marker);
        }
    });
    
    
    
    // Update location count display
    updateLocationCount(locations.length);
}



function showLocationDetails(location) {
    const detailsDiv = document.getElementById('location-details');
    const typesText = location.types && location.types.length > 0 ? location.types.join(', ') : 'N/A';
    const amenitiesText = location.amenities && location.amenities.length > 0 ? location.amenities.join(', ') : 'N/A';

    detailsDiv.innerHTML = `
        <div class="flex justify-between items-start mb-3">
            <h6 class="text-lg font-bold">${location.title || 'Untitled'}</h6>
            <button class="btn btn-sm btn-ghost text-base-content/70 hover:text-base-content" onclick="dismissLocationDetails()">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
        <div class="space-y-2 text-sm">
            <p><strong>Address:</strong> ${location.street_address || 'N/A'}</p>
            <p><strong>City:</strong> ${location.city || 'N/A'}</p>
            <p><strong>State:</strong> ${location.state || 'N/A'}</p>
            <p><strong>Year:</strong> ${location.year || 'N/A'}</p>
            <p><strong>Types:</strong> ${typesText}</p>
            <p><strong>Amenities:</strong> ${amenitiesText}</p>
            <p><strong>Status:</strong> ${location.status || 'N/A'}</p>
            ${location.description ? `<p><strong>Description:</strong> ${location.description}</p>` : ''}
            ${location.notes ? `<p><strong>Notes:</strong> ${location.notes}</p>` : ''}
        </div>
    `;
}

function populateFilters() {
    // Populate type filter
    const typeFilter = document.getElementById('type-filter');
    typeFilter.innerHTML = '<option value="">All Types</option>';
    
    locationTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type.name;
        option.textContent = type.name;
        typeFilter.appendChild(option);
    });
    
    // Populate state filter
    const states = [...new Set(currentData.map(loc => loc.state).filter(Boolean))].sort();
    const stateFilter = document.getElementById('state-filter');
    stateFilter.innerHTML = '<option value="">All States</option>';
    
    states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateFilter.appendChild(option);
    });
}

function setupEventListeners() {
    // Year slider
    const yearSlider = document.getElementById('year-slider');
    yearSlider.addEventListener('input', function() {
        currentYear = parseInt(this.value);
        document.getElementById('year-display').textContent = currentYear;
        
        // Auto-filter by year
        const filteredData = filterByYear(currentData, currentYear);
        displayLocations(filteredData);
    });
    
    // Apply filters button
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
}

function applyFilters() {
    const type = document.getElementById('type-filter').value;
    const state = document.getElementById('state-filter').value;
    
    let filteredData = filterByYear(currentData, currentYear);
    
    if (type) {
        // Filter by type using the types array
        filteredData = filteredData.filter(loc => loc.types && loc.types.includes(type));
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



function dismissLocationDetails() {
    // Get the current filtered data to show the count
    const filteredData = filterByYear(currentData, currentYear);
    updateLocationCount(filteredData.length);
}

function updateLocationCount(count) {
    // Update the location details panel with count
    const detailsDiv = document.getElementById('location-details');
    if (count === 0) {
        detailsDiv.innerHTML = `
            <div class="text-center py-6">
                <svg class="w-10 h-10 mx-auto mb-3 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <p class="text-sm text-base-content/70">No locations found for ${currentYear}</p>
            </div>
        `;
    } else {
        detailsDiv.innerHTML = `
            <div class="text-center py-4">
                <span class="text-3xl font-bold text-primary">${count.toLocaleString()}</span>
                <p class="text-sm text-base-content/70 mt-1">locations in ${currentYear}</p>
                <p class="text-xs text-base-content/50 mt-3">
                    Click on a marker to see location details
                </p>
            </div>
        `;
    }
}
