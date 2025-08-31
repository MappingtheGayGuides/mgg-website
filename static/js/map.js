// Map functionality for Mapping the Gay Guides

let map;
let markerClusterGroup;
let currentData = [];
let currentYear = 1965;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Map.js loaded, initializing...');
    
    try {
        initializeMap();
        loadData();
        setupEventListeners();
    } catch (error) {
        console.error('Error during map initialization:', error);
        document.getElementById('location-details').innerHTML = 
            '<p class="text-danger">Error initializing map. Please check console for details.</p>';
    }
});

function initializeMap() {
    console.log('Initializing map...');
    
    // Check if Leaflet is available
    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded!');
        return;
    }
    console.log('Leaflet library available:', L);
    
    // Check if map container exists
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found!');
        return;
    }
    console.log('Map container found:', mapContainer);
    
    // Initialize the map centered on the US
    map = L.map('map').setView([39.8283, -98.5795], 4);
    console.log('Map initialized:', map);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    console.log('Tiles added to map');
    
    // Initialize marker cluster group with performance optimizations
    if (typeof L.markerClusterGroup === 'undefined') {
        console.error('MarkerCluster plugin not loaded!');
        // Fallback to regular marker group
        markerClusterGroup = L.layerGroup();
    } else {
        markerClusterGroup = L.markerClusterGroup({
            chunkedLoading: true,
            maxClusterRadius: 80,
            spiderfyOnMaxZoom: false, // Disable for better performance
            showCoverageOnHover: false, // Disable for better performance
            zoomToBoundsOnClick: true,
            animate: false, // Disable animations for better performance
            animateAddingMarkers: false,
            chunkInterval: 100, // Faster chunking
            chunkDelay: 25, // Faster delays
            maxZoom: 18, // Limit max zoom for clustering
            disableClusteringAtZoom: 16 // Stop clustering at high zoom levels
        });
    }
    map.addLayer(markerClusterGroup);
    console.log('Marker cluster group added to map');
}

function loadData() {
    console.log('Loading data from /api/locations...');
    // Load locations data
    fetch('/api/locations')
        .then(response => {
            console.log('Response received:', response.status, response.ok);
            return response.json();
        })
        .then(locationsData => {
            console.log('Data loaded, locations count:', locationsData.length);
            currentData = locationsData;
            
            // Update data size info
            const dataSizeInfo = document.getElementById('data-size-info');
            dataSizeInfo.textContent = `Total locations: ${currentData.length.toLocaleString()}`;
            
            // Filter by current year and display
            const filteredData = getCachedYearData(currentYear);
            console.log('Filtered data for year', currentYear, ':', filteredData.length, 'locations');
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
    // Use a more efficient filter with early return for better performance
    const filtered = [];
    const len = locations.length;
    for (let i = 0; i < len; i++) {
        const location = locations[i];
        if (location.year === year) { // Simplified check
            filtered.push(location);
        }
    }
    return filtered;
}

// Cache filtered data by year for better performance
const yearCache = new Map();

function getCachedYearData(year) {
    if (yearCache.has(year)) {
        return yearCache.get(year);
    }
    
    const filtered = filterByYear(currentData, year);
    yearCache.set(year, filtered);
    
    // Limit cache size to prevent memory issues
    if (yearCache.size > 20) {
        const firstKey = yearCache.keys().next().value;
        yearCache.delete(firstKey);
    }
    
    return filtered;
}

function displayLocations(locations) {
    console.log('Displaying locations:', locations.length);
    
    // Only update if we have a different number of locations or if it's the first load
    const currentMarkerCount = markerClusterGroup.getLayers().length;
    if (currentMarkerCount === locations.length && currentMarkerCount > 0) {
        // Same number of locations, just update the count display
        updateLocationCount(locations.length);
        return;
    }
    
    // Batch marker operations for better performance
    const markers = [];
    const len = locations.length;
    let validCoordinates = 0;
    
    for (let i = 0; i < len; i++) {
        const location = locations[i];
        if (location.latitude && location.longitude) {
            // Ensure coordinates are numbers
            const lat = parseFloat(location.latitude);
            const lng = parseFloat(location.longitude);
            
            if (!isNaN(lat) && !isNaN(lng)) {
                const marker = L.marker([lat, lng]);
                marker.on('click', () => showLocationDetails(location));
                markers.push(marker);
                validCoordinates++;
            } else {
                console.log('Invalid coordinates for location:', location.id, 'lat:', location.latitude, 'lng:', location.longitude);
            }
        }
    }
    
    console.log('Created markers:', markers.length, 'out of', len, 'locations (valid coordinates:', validCoordinates, ')');
    
    // Clear and add all markers at once
    if (markerClusterGroup && typeof markerClusterGroup.clearLayers === 'function') {
        markerClusterGroup.clearLayers();
        markerClusterGroup.addLayers(markers);
    } else {
        console.error('Marker cluster group not properly initialized');
    }
    
    // Update location count display
    updateLocationCount(locations.length);
}

function updateLocationCount(count) {
    console.log('Updating location count to:', count);
    // This function might be missing, so let's implement it
    const dataSizeInfo = document.getElementById('data-size-info');
    if (dataSizeInfo) {
        dataSizeInfo.textContent = `Total locations: ${count.toLocaleString()}`;
    }
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
    // Populate amenity filter
    const amenityFilter = document.getElementById('amenity-filter');
    amenityFilter.innerHTML = '<option value="">All Amenities</option>';
    
    // Get unique amenities from all locations
    const allAmenities = new Set();
    currentData.forEach(location => {
        if (location.amenities && Array.isArray(location.amenities)) {
            location.amenities.forEach(amenity => allAmenities.add(amenity));
        }
    });
    
    // Sort and populate amenities
    [...allAmenities].sort().forEach(amenity => {
        const option = document.createElement('option');
        option.value = amenity;
        option.textContent = amenity;
        amenityFilter.appendChild(option);
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
    // Year slider with debouncing
    const yearSlider = document.getElementById('year-slider');
    let sliderTimeout;
    
    yearSlider.addEventListener('input', function() {
        const newYear = parseInt(this.value);
        document.getElementById('year-display').textContent = newYear;
        
        // Show loading indicator
        const loadingIndicator = document.getElementById('year-loading');
        loadingIndicator.classList.remove('hidden');
        
        // Clear previous timeout
        clearTimeout(sliderTimeout);
        
        // Debounce the actual filtering to 300ms after user stops moving (increased for better performance)
        sliderTimeout = setTimeout(() => {
            if (newYear !== currentYear) {
                currentYear = newYear;
                const filteredData = getCachedYearData(currentYear);
                displayLocations(filteredData);
            }
            // Hide loading indicator after filtering is complete
            loadingIndicator.classList.add('hidden');
        }, 300);
    });
    
    // Apply filters button
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
    
    // Reset filters button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

function applyFiltersAndGetData() {
    const amenity = document.getElementById('amenity-filter').value;
    const state = document.getElementById('state-filter').value;
    const removeUnclearAddresses = document.getElementById('clear-addresses-checkbox').checked;
    
    let filteredData = getCachedYearData(currentYear);
    
    if (amenity) {
        // Filter by amenity using the amenities array
        filteredData = filteredData.filter(loc => loc.amenities && loc.amenities.includes(amenity));
    }
    
    if (state) {
        filteredData = filteredData.filter(loc => loc.state === state);
    }
    
    if (removeUnclearAddresses) {
        // Filter out locations with unclear/unverified status
        filteredData = filteredData.filter(loc => {
            const status = loc.status ? loc.status : '';
            return status !== 'Location could not be verified. General city or location coordinates used.';
        });
    }
    
    return filteredData;
}

function applyFilters() {
    // Show loading state on button
    const applyButton = document.getElementById('apply-filters');
    const originalContent = applyButton.innerHTML;
    applyButton.innerHTML = '<span class="loading loading-spinner loading-sm"></span> Applying...';
    applyButton.disabled = true;
    
    // Use setTimeout to allow the UI to update before processing
    setTimeout(() => {
        const filteredData = applyFiltersAndGetData();
        displayLocations(filteredData);
        
        // Restore button state
        applyButton.innerHTML = originalContent;
        applyButton.disabled = false;
    }, 50);
}

function resetFilters() {
    // Show loading state on button
    const resetButton = document.getElementById('reset-filters');
    const originalContent = resetButton.innerHTML;
    resetButton.innerHTML = '<span class="loading loading-spinner loading-sm"></span> Resetting...';
    resetButton.disabled = true;
    
    // Use setTimeout to allow the UI to update before processing
    setTimeout(() => {
        // Reset year to 1965
        currentYear = 1965;
        document.getElementById('year-slider').value = currentYear;
        document.getElementById('year-display').textContent = currentYear;
        
        // Reset all filter dropdowns and checkboxes
        document.getElementById('amenity-filter').value = '';
        document.getElementById('state-filter').value = '';
        document.getElementById('clear-addresses-checkbox').checked = false;
        
        // Apply the reset filters and display results
        const filteredData = getCachedYearData(currentYear);
        displayLocations(filteredData);
        
        // Restore button state
        resetButton.innerHTML = originalContent;
        resetButton.disabled = false;
    }, 50);
}



function dismissLocationDetails() {
    // Get the current filtered data (including all filters) to show the count
    const filteredData = applyFiltersAndGetData();
    updateLocationCount(filteredData.length);
}

function updateLocationCount(count) {
    // Update the location details panel with count
    const detailsDiv = document.getElementById('location-details');
    
    // Check if any filters are currently applied
    const amenity = document.getElementById('amenity-filter').value;
    const state = document.getElementById('state-filter').value;
    const removeUnclearAddresses = document.getElementById('clear-addresses-checkbox').checked;
    const hasFilters = amenity || state || removeUnclearAddresses;
    
    if (count === 0) {
        detailsDiv.innerHTML = `
            <div class="text-center py-6">
                <svg class="w-10 h-10 mx-auto mb-3 text-base-content/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <p class="text-sm text-base-content/70">No locations found for ${currentYear}${hasFilters ? ' with current filters' : ''}</p>
            </div>
        `;
    } else {
        detailsDiv.innerHTML = `
            <div class="text-center py-4">
                <span class="text-3xl font-bold text-primary">${count.toLocaleString()}</span>
                <p class="text-sm text-base-content/70 mt-1">locations in ${currentYear}${hasFilters ? ' with current filters' : ''}</p>
                <p class="text-xs text-base-content/50 mt-3">
                    Click on a marker to see location details
                </p>
            </div>
        `;
    }
}
