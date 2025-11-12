// Map functionality for Mapping the Gay Guides using Mapbox GL JS

// Mapbox access token - replace with your token
const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYWVyZWdhbiIsImEiOiJjbWh3NmE5ZWswM2xrMmlvY2wzYjhuOWVmIn0.KhOofH1fXHn87-utlCGD8g';

let map;
let currentData = [];
let currentYear = 1965;
let locationsSource = null;

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
    console.log('Initializing Mapbox map...');
    
    // Check if Mapbox GL is available
    if (typeof mapboxgl === 'undefined') {
        console.error('Mapbox GL library not loaded!');
        return;
    }
    
    // Check if map container exists
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found!');
        return;
    }
    
    // Set Mapbox access token
    mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
    
    if (MAPBOX_ACCESS_TOKEN === 'YOUR_MAPBOX_ACCESS_TOKEN_HERE') {
        console.error('Mapbox access token not set!');
        mapContainer.innerHTML = '<div class="flex items-center justify-center h-full"><p class="text-error">Please set your Mapbox access token in map.js</p></div>';
        return;
    }
    
    // Initialize the map centered on the US
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v11',
        center: [-98.5795, 39.8283], // [lng, lat] for Mapbox
        zoom: 4
    });
    
    console.log('Map initialized');
    
    // Wait for map to load before adding sources and layers
    map.on('load', () => {
        console.log('Map loaded, adding data source...');
        
        // Add empty GeoJSON source for locations (NO CLUSTERING)
        map.addSource('locations', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: []
            }
            // Removed: cluster: true, clusterMaxZoom, clusterRadius
        });
        
        locationsSource = map.getSource('locations');
        
        // Add single circle layer for all points (no clustering)
        map.addLayer({
            id: 'locations-points',
            type: 'circle',
            source: 'locations',
            paint: {
                'circle-color': '#3b82f6',
                // Circle size varies with zoom level for better legibility
                'circle-radius': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    2,  3,  // At zoom 2, radius 3px
                    4,  4,  // At zoom 4 (default), radius 4px - visible!
                    6,  5,  // At zoom 6, radius 5px
                    8,  6,  // At zoom 8, radius 6px
                    10, 7,  // At zoom 10, radius 7px
                    12, 8,  // At zoom 12, radius 8px
                    14, 9,  // At zoom 14, radius 9px
                    16, 10  // At zoom 16+, radius 10px
                ],
                // Opacity varies with zoom - more transparent when zoomed out
                'circle-opacity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    2,  0.5,  // At zoom 2, 50% opacity
                    4,  0.7,  // At zoom 4 (default), 70% opacity - visible!
                    6,  0.8,  // At zoom 6, 80% opacity
                    8,  0.9,  // At zoom 8, 90% opacity
                    10, 1.0,  // At zoom 10+, 100% opacity (fully opaque)
                    12, 1.0,
                    14, 1.0,
                    16, 1.0
                ],
                'circle-stroke-width': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    2,  0.5,  // Thinner stroke when zoomed out
                    4,  1,    // Normal stroke at default zoom
                    8,  1.5,  // Thicker stroke at mid zoom
                    12, 2     // Thicker stroke when zoomed in
                ],
                'circle-stroke-color': '#fff'
                // Removed circle-sort-key as it might cause issues if 'id' doesn't exist
            }
        });
        
        // Add click handler for points
        map.on('click', 'locations-points', function(e) {
            const coordinates = e.features[0].geometry.coordinates.slice();
            const location = e.features[0].properties;
            
            // Show location details
            showLocationDetails(location);
            
            // Create popup
            const popup = new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(`
                    <div class="text-sm">
                        <strong>${location.title || 'Untitled'}</strong><br/>
                        ${location.city || ''}${location.state ? ', ' + location.state : ''}
                    </div>
                `)
                .addTo(map);
        });
        
        // Change cursor on hover
        map.on('mouseenter', 'locations-points', function() {
            map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'locations-points', function() {
            map.getCanvas().style.cursor = '';
        });
        
        console.log('Map layers and handlers added');
    });
}

function loadData() {
    console.log(`Loading data for year ${currentYear} from /api/locations...`);
    // Load locations data for current year only
    loadYearData(currentYear)
        .then(locationsData => {
            console.log('Data loaded, locations count:', locationsData.length);
            currentData = locationsData;
            
            // Update data size info
            const dataSizeInfo = document.getElementById('data-size-info');
            dataSizeInfo.textContent = `Total locations: ${currentData.length.toLocaleString()}`;
            
            // Display the data (already filtered by year from API)
            displayLocations(currentData);
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

// Cache data by year for better performance
const yearCache = new Map();

function loadYearData(year) {
    // Check cache first
    if (yearCache.has(year)) {
        console.log(`Using cached data for year ${year}`);
        return Promise.resolve(yearCache.get(year));
    }
    
    // Show loading indicator
    const loadingIndicator = document.getElementById('year-loading');
    if (loadingIndicator) {
        loadingIndicator.classList.remove('hidden');
    }
    
    // Fetch from API
    console.log(`Fetching data for year ${year} from API...`);
    return fetch(`/api/locations?year=${year}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Data fetched for year ${year}:`, data.length, 'locations');
            yearCache.set(year, data);
            
            // Limit cache size to prevent memory issues
            if (yearCache.size > 20) {
                const firstKey = yearCache.keys().next().value;
                yearCache.delete(firstKey);
                console.log(`Removed year ${firstKey} from cache`);
            }
            
            // Hide loading indicator
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
            
            return data;
        })
        .catch(error => {
            console.error(`Error loading data for year ${year}:`, error);
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
            throw error;
        });
}

function displayLocations(locations) {
    console.log('Displaying locations:', locations.length);
    
    if (!map) {
        console.error('Map not initialized');
        return;
    }
    
    // Ensure map is loaded before trying to update source
    if (!map.loaded()) {
        console.log('Map not loaded yet, waiting...');
        map.once('load', () => {
            displayLocations(locations);
        });
        return;
    }
    
    // Get or create the source
    if (!locationsSource) {
        if (map.getSource('locations')) {
            locationsSource = map.getSource('locations');
        } else {
            console.error('Locations source not found');
            return;
        }
    }
    
    // Convert locations to GeoJSON features
    const features = [];
    let validCoordinates = 0;
    
    for (let i = 0; i < locations.length; i++) {
        const location = locations[i];
        if (location.latitude && location.longitude) {
            // Ensure coordinates are numbers
            const lat = parseFloat(location.latitude);
            const lng = parseFloat(location.longitude);
            
            if (!isNaN(lat) && !isNaN(lng)) {
                // Filter out invalid coordinates (outside reasonable bounds)
                if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
                    features.push({
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: [lng, lat] // Mapbox uses [lng, lat]
                        },
                        properties: {
                            id: location.id || i,
                            title: location.title || 'Untitled',
                            street_address: location.street_address || '',
                            city: location.city || '',
                            state: location.state || '',
                            year: location.year || '',
                            types: location.types || [],
                            amenities: location.amenities || [],
                            status: location.status || '',
                            description: location.description || '',
                            notes: location.notes || ''
                        }
                    });
                validCoordinates++;
                }
            }
        }
    }
    
    console.log('Created features:', features.length, 'out of', locations.length, 'locations (valid coordinates:', validCoordinates, ')');
    console.log('Sample feature:', features[0]);
    
    // Update the GeoJSON source
    try {
        locationsSource.setData({
            type: 'FeatureCollection',
            features: features
        });
        console.log('Source data updated successfully');
    } catch (error) {
        console.error('Error updating source data:', error);
    }
    
    // Fit map to bounds if we have features
    if (features.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        features.forEach(feature => {
            bounds.extend(feature.geometry.coordinates);
        });
        
        // Only fit bounds if we have a reasonable number of features
        // For large datasets, just ensure the map is visible
        if (features.length < 10000) {
            map.fitBounds(bounds, {
                padding: 50,
                maxZoom: 10
            });
        }
    }
    
    // Update location count display
    updateLocationCount(locations.length);
}

function updateLocationCount(count) {
    console.log('Updating location count to:', count);
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
        
        // Clear previous timeout
        clearTimeout(sliderTimeout);
        
        // Debounce the actual fetching to 300ms after user stops moving
        sliderTimeout = setTimeout(() => {
            if (newYear !== currentYear) {
                currentYear = newYear;
                
                // Load data for the new year
                loadYearData(currentYear)
                    .then(locationsData => {
                        console.log('Loaded data for year', currentYear, ':', locationsData.length, 'locations');
                        currentData = locationsData;
                        
                        // Update data size info
                        const dataSizeInfo = document.getElementById('data-size-info');
                        dataSizeInfo.textContent = `Total locations: ${currentData.length.toLocaleString()}`;
                        
                        // Display the new data
                        displayLocations(currentData);
                        
                        // Update filters
                        populateFilters();
                    })
                    .catch(error => {
                        console.error('Error loading year data:', error);
                    });
            }
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
    
    let filteredData = currentData;  // Use currentData directly
    
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
        
        // Load data for the reset year and display results
        loadYearData(currentYear)
            .then(locationsData => {
                currentData = locationsData;
                
                // Update data size info
                const dataSizeInfo = document.getElementById('data-size-info');
                dataSizeInfo.textContent = `Total locations: ${currentData.length.toLocaleString()}`;
                
                // Display the data
                displayLocations(currentData);
                populateFilters();
                
                // Restore button state
                resetButton.innerHTML = originalContent;
                resetButton.disabled = false;
            })
            .catch(error => {
                console.error('Error loading reset data:', error);
                resetButton.innerHTML = originalContent;
                resetButton.disabled = false;
            });
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
