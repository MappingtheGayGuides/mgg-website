// Amenities visualization for Mapping the Gay Guides using D3.js

let amenitiesData = [];
let currentChart = null;
let currentView = 'percentage'; // 'percentage' or 'count'
let currentAmenity = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Amenities.js loaded, initializing...');

    try {
        loadAmenitiesData();
        setupEventListeners();
    } catch (error) {
        console.error('Error during amenities initialization:', error);
        const chartContainer = document.getElementById('combined-chart');
        if (chartContainer) {
            chartContainer.innerHTML = '<p class="text-danger">Error initializing amenities visualization. Please check console for details.</p>';
        }
    }
});

function loadAmenitiesData() {
    console.log('Loading amenities data...');

    // Get current filter values
    const stateFilter = document.getElementById('state-filter');
    const state = stateFilter ? stateFilter.value : '';
    
    // Build query string with filters
    let url = '/api/amenities-trends';
    const params = new URLSearchParams();
    if (state) params.append('state', state);
    if (params.toString()) {
        url += '?' + params.toString();
    }

    // Use real API data instead of sample data
    fetch(url)
        .then(response => {
            console.log('Response received:', response.status, response.ok);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Amenities data loaded successfully');
            console.log('Data structure:', {
                hasAmenities: !!data.amenities,
                hasYears: !!data.years,
                hasTrends: !!data.trends,
                hasTotalLocations: !!data.totalLocations,
                amenitiesCount: data.amenities ? data.amenities.length : 0,
                yearsCount: data.years ? data.years.length : 0
            });

            if (data.error) {
                console.error('API returned error:', data.error);
                throw new Error(data.error);
            }

            if (!data.amenities || !data.years || !data.trends) {
                console.error('Invalid data structure:', data);
                throw new Error('Invalid data structure from API');
            }

            amenitiesData = data;
            populateAmenityDropdowns();
            // Only populate state/city dropdowns on first load
            if (!amenitiesData._stateCityPopulated) {
                populateStateCityDropdowns();
                amenitiesData._stateCityPopulated = true;
            }
            
            // Get selected amenity (preserve selection)
            const dropdown = document.getElementById('amenity-1');
            const selectedAmenity = dropdown ? dropdown.value : '';
            const checkboxContainer = document.getElementById('total-locations-checkbox-container');
            
            if (selectedAmenity) {
                // Show checkbox when an amenity is selected
                if (checkboxContainer) {
                    checkboxContainer.style.display = 'flex';
                }
                
                currentAmenity = selectedAmenity;
                const selectedAmenities = [selectedAmenity];
                
                // Create chart based on current view
                createSingleViewChart(selectedAmenity, currentView);
                
                // Create density map
                createDensityMap(selectedAmenity);
                
                currentChart = true;
                
                // Update insights
                updateInsights(selectedAmenities);
            } else {
                // Show total locations trend by default
                console.log('Calling showDefaultCharts...');
                showDefaultCharts();
                currentAmenity = null;
                // Hide checkbox when no amenity is selected
                if (checkboxContainer) {
                    checkboxContainer.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error loading amenities data:', error);
            // Fallback to sample data for development
            loadSampleData();
        });
}

function loadSampleData() {
    console.log('Loading sample data for development...');

    // Sample data structure for development using real amenity codes with total locations per year
    const totalLocationsPerYear = [120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330];
    
    // All 76 amenities from the database
    const allAmenities = [
        '($-1999-2003)', '(*-1965-2005)', '(18+-1994-2003)', '(A-1994-2003)', '(AH-1975-1993)',
        '(AYOR-1977-2005)', '(B&B-1987-1989)', '(B-1970-1989)', '(B-1990-1993)', '(B-1999-2005)',
        '(BA-1975-1989)', '(BW-1990-2003)', '(BWMT-1987-1989)', '(BYOB-1969-2003)', '(C&W)',
        '(C-1965-1989)', '(C-2003-2005)', '(CBC-1987-1989)', '(CW-1982-2003)', '(D-1965-2003)',
        '(DS-2002-2003)', '(E-1975-2003)', '(F&S-1984-1989)', '(F-1990-2003)', '(FFA-1975-1987)',
        '(G-1965-1979)', '(GF-1994-2003)', '(GO-2000-2003)', '(GS-1999-2003)', '(H-1965-1989)',
        '(H-1990-1995)', '(HIP-1973-1983)', '(HOT-1975-1979)', '(IGHC-1987-1989)', '(IGTA-1988-1997)',
        '(K-1994-2003)', '(L-1980-1989)', '(L-1990-2005)', '(LV-1990-1994)', '(M-1965-1989)',
        '(M-1996-2005)', '(MCC)', '(MO-1995-2003)', '(MR-A-1994-2003)', '(MR-AF-1994-2003)',
        '(MR-L-1994-2003)', '(MRC-1994-2003)', '(MW-1990-2003)', '(MX-1990-1993)', '(N-1988-1989)',
        '(N-1990-2005)', '(NH-1990-2005)', '(NS-1998-2005)', '(OC-1976-2005)', '(P-1965-1989)',
        '(P-1990-2002)', '(P-2003-2005)', '(PC-1990-2005)', '(PE-1965-1989)', '(PT-1977-1989)',
        '(R-1965-1989)', '(R-2003-2005)', '(RT-1965-1989)', '(S-1965-2002)', '(S-2003-2005)',
        '(SM-1965-1989)', '(SW-1990-2005)', '(TA-1998-2000)', '(TG-1997-2005)', '(V-1986-2005)',
        '(W-1972-1989)', '(W-1990-2005)', '(WC-1994-2005)', '(WE-1976-1989)', '(YC-1969-2005)',
        'Cruisy Area'
    ];
    
    amenitiesData = {
        amenities: allAmenities,
        trends: {
            '($-1999-2003)': [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
            '(*-1965-2005)': [15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(18+-1994-2003)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(A-1994-2003)': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48],
            '(AH-1975-1993)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(AYOR-1977-2005)': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
            '(B&B-1987-1989)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(B-1970-1989)': [45, 52, 58, 65, 72, 78, 85, 92, 98, 105, 112, 118, 125, 132, 138],
            '(B-1990-1993)': [12, 15, 18, 22, 25, 28, 32, 35, 38, 42, 45, 48, 52, 55, 58],
            '(B-1999-2005)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(BA-1975-1989)': [15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(BW-1990-2003)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(BWMT-1987-1989)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(BYOB-1969-2003)': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48],
            '(C&W)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(C-1965-1989)': [20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55],
            '(C-2003-2005)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(CBC-1987-1989)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(CW-1982-2003)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(D-1965-2003)': [30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65],
            '(DS-2002-2003)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20],
            '(E-1975-2003)': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
            '(F&S-1984-1989)': [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
            '(F-1990-2003)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(FFA-1975-1987)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(G-1965-1979)': [15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(GF-1994-2003)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(GO-2000-2003)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(GS-1999-2003)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(H-1965-1989)': [25, 28, 32, 35, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72],
            '(H-1990-1995)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(HIP-1973-1983)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(HOT-1975-1979)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(IGHC-1987-1989)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20],
            '(IGTA-1988-1997)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(K-1994-2003)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(L-1980-1989)': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48],
            '(L-1990-2005)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(LV-1990-1994)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(M-1965-1989)': [18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(M-1996-2005)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(MCC)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(MO-1995-2003)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(MR-A-1994-2003)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(MR-AF-1994-2003)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(MR-L-1994-2003)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(MRC-1994-2003)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20],
            '(MW-1990-2003)': [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
            '(MX-1990-1993)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(N-1988-1989)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20],
            '(N-1990-2005)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(NH-1990-2005)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(NS-1998-2005)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(OC-1976-2005)': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
            '(P-1965-1989)': [15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(P-1990-2002)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(P-2003-2005)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(PC-1990-2005)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(PE-1965-1989)': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48],
            '(PT-1977-1989)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(R-1965-1989)': [35, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82],
            '(R-2003-2005)': [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
            '(RT-1965-1989)': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
            '(S-1965-2002)': [18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            '(S-2003-2005)': [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22],
            '(SM-1965-1989)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(SW-1990-2005)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(TA-1998-2000)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20],
            '(TG-1997-2005)': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24],
            '(V-1986-2005)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(W-1972-1989)': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48],
            '(W-1990-2005)': [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            '(WC-1994-2005)': [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26],
            '(WE-1976-1989)': [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42],
            '(YC-1969-2005)': [15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            'Cruisy Area': [12, 15, 18, 20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48]
        },
        years: [1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979],
        totalLocations: totalLocationsPerYear
    };

    populateAmenityDropdowns();
    populateStateCityDropdowns();
}

function populateAmenityDropdowns() {
    const dropdown = document.getElementById('amenity-1');
    const amenities = amenitiesData.amenities || [];

    if (dropdown) {
        // Preserve selected value
        const selectedValue = dropdown.value;
        
        // Clear existing options except the first one
        dropdown.innerHTML = '<option value="">Select an amenity...</option>';

        // Add amenity options
        amenities.forEach(amenity => {
            const option = document.createElement('option');
            option.value = amenity;
            option.textContent = amenity;
            dropdown.appendChild(option);
        });
        
        // Restore selected value if it still exists in the new options
        if (selectedValue) {
            const optionExists = Array.from(dropdown.options).some(opt => opt.value === selectedValue);
            if (optionExists) {
                dropdown.value = selectedValue;
            }
        }
    }
}

function populateStateCityDropdowns() {
    // Only populate if dropdown is empty (first load)
    const stateDropdown = document.getElementById('state-filter');
    
    // Check if dropdown already has options (excluding the default "All" option)
    const stateHasOptions = stateDropdown && stateDropdown.options.length > 1;
    
    // If already has options, don't repopulate
    if (stateHasOptions) {
        return;
    }
    
    // Fetch states from API
    fetch('/api/states-cities')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Preserve selected value
            const selectedState = stateDropdown ? stateDropdown.value : '';
            
            // Populate state dropdown
            if (stateDropdown && data.states && !stateHasOptions) {
                stateDropdown.innerHTML = '<option value="">All States</option>';
                data.states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.textContent = state;
                    stateDropdown.appendChild(option);
                });
                // Restore selected value
                if (selectedState) {
                    stateDropdown.value = selectedState;
                }
            }
        })
        .catch(error => {
            console.error('Error loading states:', error);
        });
}

function setupEventListeners() {
    console.log('Setting up event listeners...');

    // Update chart button
    const updateButton = document.getElementById('update-chart');
    if (updateButton) {
        updateButton.addEventListener('click', updateChart);
    }

    // Reset button
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', resetFilters);
    }

    // No auto-update on dropdown changes - user must click "Update Chart" button

    // View toggle buttons
    const percentageButton = document.getElementById('percentage-view');
    const countButton = document.getElementById('count-view');
    
    if (percentageButton) {
        percentageButton.addEventListener('click', () => switchView('percentage'));
    }
    
    if (countButton) {
        countButton.addEventListener('click', () => switchView('count'));
    }
    
    // Total locations checkbox
    const totalLocationsCheckbox = document.getElementById('show-total-locations');
    if (totalLocationsCheckbox) {
        totalLocationsCheckbox.addEventListener('change', () => {
            // Redraw chart if an amenity is selected
            if (currentAmenity) {
                createSingleViewChart(currentAmenity, currentView);
            }
        });
    }
    
    // No longer need tab functionality
}

function updateChart() {
    console.log('Updating chart...');

    // Reload amenities data with current filters first
    // This ensures data is always in sync with filters when update is clicked
    loadAmenitiesData();
    
    // Note: The chart will be updated in the loadAmenitiesData callback
    // if an amenity is selected, or showDefaultCharts will be called if not
}

function switchView(view) {
    currentView = view;
    
    // Update button styles
    const percentageButton = document.getElementById('percentage-view');
    const countButton = document.getElementById('count-view');
    
    if (view === 'percentage') {
        percentageButton.className = 'btn btn-sm btn-primary';
        countButton.className = 'btn btn-sm btn-outline';
    } else {
        percentageButton.className = 'btn btn-sm btn-outline';
        countButton.className = 'btn btn-sm btn-primary';
    }
    
    // Redraw chart if an amenity is selected
    if (currentAmenity) {
        createSingleViewChart(currentAmenity, currentView);
    }
}

function createSingleViewChart(selectedAmenity, view) {
    // Clear previous chart
    const chartContainer = document.getElementById('combined-chart');
    chartContainer.innerHTML = '';

    // Set up dimensions
    const margin = { top: 30, right: 80, bottom: 50, left: 50 };
    const width = chartContainer.clientWidth - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select(chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    let data, yScale, yAxis, lineColor, yAxisLabel, legendText, totalData, totalYScale;

    if (view === 'percentage') {
        // Calculate percentage data
        data = amenitiesData.years.map((year, i) => ({
            year: year,
            value: amenitiesData.totalLocations[i] > 0 ? 
                (amenitiesData.trends[selectedAmenity][i] / amenitiesData.totalLocations[i] * 100) : 0
        }));
        
        // Prepare total data for reference (actual total locations count)
        totalData = amenitiesData.years.map((year, i) => ({
            year: year,
            value: amenitiesData.totalLocations[i]
        }));
        
        // Create separate scales for percentage (left axis) and total count (right axis)
        yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value) * 1.1])
            .range([height, 0]);
            
        totalYScale = d3.scaleLinear()
            .domain([0, d3.max(totalData, d => d.value) * 1.1])
            .range([height, 0]);
            
        yAxis = d3.axisLeft(yScale).tickFormat(d => d + '%');
        lineColor = '#3b82f6';
        yAxisLabel = 'Percentage of Total Locations';
        legendText = 'Percentage';
    } else {
        // Prepare count data
        data = amenitiesData.years.map((year, i) => ({
            year: year,
            value: amenitiesData.trends[selectedAmenity][i]
        }));
        
        // Prepare total data for reference
        totalData = amenitiesData.years.map((year, i) => ({
            year: year,
            value: amenitiesData.totalLocations[i]
        }));
        
        // Check if total locations checkbox is checked
        const showTotalLocations = document.getElementById('show-total-locations')?.checked || false;
        
        // Only include totalData in domain if checkbox is checked
        const domainData = showTotalLocations ? [...data, ...totalData] : data;
        
        yScale = d3.scaleLinear()
            .domain([0, d3.max(domainData, d => d.value) * 1.1])
            .range([height, 0]);
            
        totalYScale = yScale; // Same scale for count view
            
        yAxis = d3.axisLeft(yScale);
        lineColor = '#ef4444';
        yAxisLabel = 'Number of Locations';
        legendText = 'Raw Count';
    }

    // Scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(amenitiesData.years))
        .range([0, width]);

    // Line generators
    const line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.value))
        .curve(d3.curveMonotoneX);
        
    const totalLine = d3.line()
        .x(d => xScale(d.year))
        .y(d => totalYScale(d.value))
        .curve(d3.curveMonotoneX);

    // Add axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.format('d'));
    const yTotalAxis = view === 'percentage' ? d3.axisRight(totalYScale) : null;

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);

    // Check if total locations checkbox is checked
    const showTotalLocations = document.getElementById('show-total-locations')?.checked || false;

    // Add right Y-axis for total count in percentage view (only if checkbox is checked)
    if (view === 'percentage' && yTotalAxis && showTotalLocations) {
        svg.append('g')
            .attr('class', 'y-axis-right')
            .attr('transform', `translate(${width},0)`)
            .call(yTotalAxis);
    }

    // Add axis labels
    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Year');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -margin.left + 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text(yAxisLabel);

    // Add right Y-axis label for total count in percentage view (only if checkbox is checked)
    if (view === 'percentage' && showTotalLocations) {
        svg.append('text')
            .attr('class', 'axis-label')
            .attr('text-anchor', 'middle')
            .attr('transform', `rotate(90 ${width + margin.right - 20} ${height / 2})`)
            .attr('x', width + margin.right - 20)
            .attr('y', height / 2)
            .style('font-size', '12px')
            .style('fill', '#6b7280')
            .text('Total Locations');
    }

    // Add grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickSize(-height).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    svg.append('g')
        .attr('class', 'grid')
        .call(d3.axisLeft(yScale).tickSize(-width).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    // Add the total reference line (only if checkbox is checked)
    if (showTotalLocations) {
        svg.append('path')
            .datum(totalData)
            .attr('class', 'line-total-reference')
            .attr('d', totalLine)
            .style('fill', 'none')
            .style('stroke', '#10b981')
            .style('stroke-width', 2)
            .style('stroke-dasharray', '5,5')
            .style('opacity', 0.6);
    }

    // Add the main line
    svg.append('path')
        .datum(data)
        .attr('class', 'line-main')
        .attr('d', line)
        .style('fill', 'none')
        .style('stroke', lineColor)
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add dots for data points
    svg.selectAll('.dot-main')
        .data(data)
        .enter().append('circle')
        .attr('class', 'dot-main')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yScale(d.value))
        .attr('r', 4)
        .style('fill', lineColor)
        .style('opacity', 0.8);

    // Add invisible hover areas for better interaction
    svg.selectAll('.hover-area')
        .data(data)
        .enter().append('circle')
        .attr('class', 'hover-area')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yScale(d.value))
        .attr('r', 8)
        .style('fill', 'transparent')
        .style('cursor', 'pointer')
        .on('mouseover', function(event, d) {
            showTooltip(event, d, selectedAmenity, view);
        })
        .on('mouseout', function() {
            hideTooltip();
        });

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 150}, 20)`);

    // Main data legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 0)
        .attr('y2', 0)
        .style('stroke', lineColor)
        .style('stroke-width', 3);

    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 0)
        .attr('r', 3)
        .style('fill', lineColor);

    legend.append('text')
        .attr('x', 25)
        .attr('y', 4)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text(legendText);

    // Total reference legend item (only if checkbox is checked)
    if (showTotalLocations) {
        legend.append('line')
            .attr('x1', 0)
            .attr('x2', 20)
            .attr('y1', 15)
            .attr('y2', 15)
            .style('stroke', '#10b981')
            .style('stroke-width', 2)
            .style('stroke-dasharray', '5,5')
            .style('opacity', 0.6);

        legend.append('text')
            .attr('x', 25)
            .attr('y', 19)
            .style('font-size', '11px')
            .style('fill', '#374151')
            .text('Total Locations');
    }
}

// Tooltip functions
function showTooltip(event, d, selectedAmenity, view) {
    // Get the year index to find corresponding data
    const yearIndex = amenitiesData.years.indexOf(d.year);
    
    // Calculate all the values we need
    const year = d.year;
    const totalLocations = amenitiesData.totalLocations[yearIndex];
    const amenityCount = amenitiesData.trends[selectedAmenity][yearIndex];
    const percentage = totalLocations > 0 ? (amenityCount / totalLocations * 100).toFixed(1) : 0;
    
    // Create tooltip content
    let tooltipContent = `
        <div class="tooltip-content">
            <div class="tooltip-title"><strong>${year}</strong></div>
            <div class="tooltip-item">
                <span class="tooltip-label">Total Locations:</span>
                <span class="tooltip-value">${totalLocations.toLocaleString()}</span>
            </div>
            <div class="tooltip-item">
                <span class="tooltip-label">${selectedAmenity}:</span>
                <span class="tooltip-value">${amenityCount.toLocaleString()}</span>
            </div>
            <div class="tooltip-item">
                <span class="tooltip-label">Percentage:</span>
                <span class="tooltip-value">${percentage}%</span>
            </div>
        </div>
    `;
    
    // Create or update tooltip
    let tooltip = d3.select('body').select('.chart-tooltip');
    if (tooltip.empty()) {
        tooltip = d3.select('body').append('div')
            .attr('class', 'chart-tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0, 0, 0, 0.8)')
            .style('color', 'white')
            .style('padding', '8px 12px')
            .style('border-radius', '6px')
            .style('font-size', '12px')
            .style('pointer-events', 'none')
            .style('z-index', '1000')
            .style('box-shadow', '0 4px 6px rgba(0, 0, 0, 0.1)')
            .style('opacity', 0);
    }
    
    tooltip.html(tooltipContent)
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .transition()
        .duration(200)
        .style('opacity', 1);
}

function hideTooltip() {
    d3.select('.chart-tooltip')
        .transition()
        .duration(200)
        .style('opacity', 0)
        .remove();
}

function createPercentageChart(selectedAmenity) {
    // Clear previous chart
    const chartContainer = document.getElementById('percentage-chart');
    chartContainer.innerHTML = '';

    // Set up dimensions
    const margin = { top: 30, right: 40, bottom: 50, left: 50 };
    const width = chartContainer.clientWidth - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select(chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Calculate percentage data
    const percentageData = amenitiesData.years.map((year, i) => ({
        year: year,
        percentage: amenitiesData.totalLocations[i] > 0 ? 
            (amenitiesData.trends[selectedAmenity][i] / amenitiesData.totalLocations[i] * 100) : 0
    }));

    // Scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(amenitiesData.years))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(percentageData, d => d.percentage) * 1.1])
        .range([height, 0]);

    // Line generator
    const line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.percentage))
        .curve(d3.curveMonotoneX);

    // Add axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.format('d'));
    const yAxis = d3.axisLeft(yScale).tickFormat(d => d + '%');

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);

    // Add axis labels
    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Year');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -margin.left + 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Percentage');

    // Add grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickSize(-height).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    svg.append('g')
        .attr('class', 'grid')
        .call(d3.axisLeft(yScale).tickSize(-width).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    // Add the percentage line
    svg.append('path')
        .datum(percentageData)
        .attr('class', 'line')
        .attr('d', line)
        .style('fill', 'none')
        .style('stroke', '#3b82f6')
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add dots for data points
    svg.selectAll('.dot')
        .data(percentageData)
        .enter().append('circle')
        .attr('class', 'dot')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yScale(d.percentage))
        .attr('r', 4)
        .style('fill', '#3b82f6')
        .style('opacity', 0.8);
}

function createCountChart(selectedAmenity) {
    // Clear previous chart
    const chartContainer = document.getElementById('count-chart');
    chartContainer.innerHTML = '';

    // Set up dimensions
    const margin = { top: 30, right: 40, bottom: 50, left: 50 };
    const width = chartContainer.clientWidth - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select(chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data for both lines
    const amenityData = amenitiesData.years.map((year, i) => ({
        year: year,
        count: amenitiesData.trends[selectedAmenity][i]
    }));

    const totalData = amenitiesData.years.map((year, i) => ({
        year: year,
        count: amenitiesData.totalLocations[i]
    }));

    // Scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(amenitiesData.years))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max([...amenityData, ...totalData], d => d.count) * 1.1])
        .range([height, 0]);

    // Line generators
    const line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.count))
        .curve(d3.curveMonotoneX);

    // Add axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.format('d'));
    const yAxis = d3.axisLeft(yScale);

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);

    // Add axis labels
    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Year');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -margin.left + 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Number of Locations');

    // Add grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickSize(-height).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    svg.append('g')
        .attr('class', 'grid')
        .call(d3.axisLeft(yScale).tickSize(-width).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    // Add amenity line
    svg.append('path')
        .datum(amenityData)
        .attr('class', 'line-amenity')
        .attr('d', line)
        .style('fill', 'none')
        .style('stroke', '#ef4444')
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add total locations line
    svg.append('path')
        .datum(totalData)
        .attr('class', 'line-total')
        .attr('d', line)
        .style('fill', 'none')
        .style('stroke', '#10b981')
        .style('stroke-width', 2)
        .style('stroke-dasharray', '5,5')
        .style('opacity', 0.6);

    // Add dots for amenity data points
    svg.selectAll('.dot-amenity')
        .data(amenityData)
        .enter().append('circle')
        .attr('class', 'dot-amenity')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yScale(d.count))
        .attr('r', 4)
        .style('fill', '#ef4444')
        .style('opacity', 0.8);

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 120}, 20)`);

    // Amenity legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 0)
        .attr('y2', 0)
        .style('stroke', '#ef4444')
        .style('stroke-width', 3);

    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 0)
        .attr('r', 3)
        .style('fill', '#ef4444');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 4)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Amenity');

    // Total legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 15)
        .attr('y2', 15)
        .style('stroke', '#10b981')
        .style('stroke-width', 2)
        .style('stroke-dasharray', '5,5');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 19)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Total Locations');
}

function createCombinedChart(selectedAmenity) {
    // Clear previous chart
    const chartContainer = document.getElementById('combined-chart');
    chartContainer.innerHTML = '';

    // Set up dimensions
    const margin = { top: 30, right: 80, bottom: 50, left: 50 };
    const width = chartContainer.clientWidth - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select(chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Calculate percentage data
    const percentageData = amenitiesData.years.map((year, i) => ({
        year: year,
        percentage: amenitiesData.totalLocations[i] > 0 ? 
            (amenitiesData.trends[selectedAmenity][i] / amenitiesData.totalLocations[i] * 100) : 0
    }));

    // Prepare count data
    const countData = amenitiesData.years.map((year, i) => ({
        year: year,
        count: amenitiesData.trends[selectedAmenity][i]
    }));

    // Prepare total data
    const totalData = amenitiesData.years.map((year, i) => ({
        year: year,
        count: amenitiesData.totalLocations[i]
    }));

    // Scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(amenitiesData.years))
        .range([0, width]);

    const yCountScale = d3.scaleLinear()
        .domain([0, d3.max([...countData, ...totalData], d => d.count) * 1.1])
        .range([height, 0]);

    const yPercentageScale = d3.scaleLinear()
        .domain([0, d3.max(percentageData, d => d.percentage) * 1.1])
        .range([height, 0]);

    // Line generators
    const countLine = d3.line()
        .x(d => xScale(d.year))
        .y(d => yCountScale(d.count))
        .curve(d3.curveMonotoneX);

    const percentageLine = d3.line()
        .x(d => xScale(d.year))
        .y(d => yPercentageScale(d.percentage))
        .curve(d3.curveMonotoneX);

    // Add axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.format('d'));
    const yCountAxis = d3.axisLeft(yCountScale);
    const yPercentageAxis = d3.axisRight(yPercentageScale).tickFormat(d => d + '%');

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y-axis-left')
        .call(yCountAxis);

    svg.append('g')
        .attr('class', 'y-axis-right')
        .attr('transform', `translate(${width},0)`)
        .call(yPercentageAxis);

    // Add axis labels
    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Year');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -margin.left + 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Number of Locations');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(90)')
        .attr('x', height / 2)
        .attr('y', margin.right - 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Percentage of Total');

    // Add grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickSize(-height).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    svg.append('g')
        .attr('class', 'grid')
        .call(d3.axisLeft(yCountScale).tickSize(-width).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    // Add amenity count line
    svg.append('path')
        .datum(countData)
        .attr('class', 'line-amenity-count')
        .attr('d', countLine)
        .style('fill', 'none')
        .style('stroke', '#ef4444')
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add total locations line
    svg.append('path')
        .datum(totalData)
        .attr('class', 'line-total')
        .attr('d', countLine)
        .style('fill', 'none')
        .style('stroke', '#10b981')
        .style('stroke-width', 2)
        .style('stroke-dasharray', '5,5')
        .style('opacity', 0.6);

    // Add percentage line
    svg.append('path')
        .datum(percentageData)
        .attr('class', 'line-percentage')
        .attr('d', percentageLine)
        .style('fill', 'none')
        .style('stroke', '#3b82f6')
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add dots for amenity count data points
    svg.selectAll('.dot-amenity-count')
        .data(countData)
        .enter().append('circle')
        .attr('class', 'dot-amenity-count')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yCountScale(d.count))
        .attr('r', 4)
        .style('fill', '#ef4444')
        .style('opacity', 0.8);

    // Add dots for percentage data points
    svg.selectAll('.dot-percentage')
        .data(percentageData)
        .enter().append('circle')
        .attr('class', 'dot-percentage')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yPercentageScale(d.percentage))
        .attr('r', 4)
        .style('fill', '#3b82f6')
        .style('opacity', 0.8);

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 200}, 20)`);

    // Amenity count legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 0)
        .attr('y2', 0)
        .style('stroke', '#ef4444')
        .style('stroke-width', 3);

    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 0)
        .attr('r', 3)
        .style('fill', '#ef4444');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 4)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Amenity Count');

    // Total locations legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 15)
        .attr('y2', 15)
        .style('stroke', '#10b981')
        .style('stroke-width', 2)
        .style('stroke-dasharray', '5,5');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 19)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Total Locations');

    // Percentage legend item
    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 30)
        .attr('y2', 30)
        .style('stroke', '#3b82f6')
        .style('stroke-width', 3);

    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 30)
        .attr('r', 3)
        .style('fill', '#3b82f6');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 34)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Percentage');
}

function createDefaultCombinedChart() {
    console.log('createDefaultCombinedChart called');
    
    // Clear previous chart
    const chartContainer = document.getElementById('combined-chart');
    if (!chartContainer) {
        console.error('Chart container not found!');
        return;
    }
    
    console.log('Chart container found:', chartContainer);
    chartContainer.innerHTML = '';

    // Set up dimensions - optimized for vertical layout
    const margin = { top: 30, right: 40, bottom: 50, left: 50 };
    let width = chartContainer.clientWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom; // Standard height for chart
    
    // Fallback width if container doesn't have proper dimensions
    if (width <= 0 || !chartContainer.clientWidth) {
        width = 600; // Good default width for full-width chart
        console.log('Using fallback width:', width);
    }
    
    console.log('Chart dimensions:', { width, height, containerWidth: chartContainer.clientWidth });

    // Create SVG
    const svg = d3.select(chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data
    const totalData = amenitiesData.years.map((year, i) => ({
        year: year,
        count: amenitiesData.totalLocations[i]
    }));

    // Scales
    const xScale = d3.scaleLinear()
        .domain(d3.extent(amenitiesData.years))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(totalData, d => d.count) * 1.1])
        .range([height, 0]);

    // Line generator
    const line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.count))
        .curve(d3.curveMonotoneX);

    // Add axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.format('d'));
    const yAxis = d3.axisLeft(yScale);

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);

    // Add axis labels
    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Year');

    svg.append('text')
        .attr('class', 'axis-label')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -margin.left + 20)
        .style('font-size', '12px')
        .style('fill', '#6b7280')
        .text('Number of Locations');

    // Add grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickSize(-height).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    svg.append('g')
        .attr('class', 'grid')
        .call(d3.axisLeft(yScale).tickSize(-width).tickFormat('').tickSizeOuter(0))
        .style('stroke-dasharray', '3,3')
        .style('opacity', 0.3);

    // Add the total locations line
    svg.append('path')
        .datum(totalData)
        .attr('class', 'line-total')
        .attr('d', line)
        .style('fill', 'none')
        .style('stroke', '#10b981')
        .style('stroke-width', 3)
        .style('opacity', 0.8);

    // Add dots for data points
    svg.selectAll('.dot-total')
        .data(totalData)
        .enter().append('circle')
        .attr('class', 'dot-total')
        .attr('cx', d => xScale(d.year))
        .attr('cy', d => yScale(d.count))
        .attr('r', 4)
        .style('fill', '#10b981')
        .style('opacity', 0.8);

    // Add title
    svg.append('text')
        .attr('class', 'chart-title')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', -10)
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .style('fill', '#374151')
        .text('Total Locations Over Time');

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 120}, 20)`);

    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 0)
        .attr('y2', 0)
        .style('stroke', '#10b981')
        .style('stroke-width', 3);

    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 0)
        .attr('r', 3)
        .style('fill', '#10b981');

    legend.append('text')
        .attr('x', 25)
        .attr('y', 4)
        .style('font-size', '11px')
        .style('fill', '#374151')
        .text('Total Locations');
}

function showDefaultCharts() {
    console.log('showDefaultCharts called');
    console.log('amenitiesData:', amenitiesData);
    
    // Hide checkbox when showing default chart
    const checkboxContainer = document.getElementById('total-locations-checkbox-container');
    if (checkboxContainer) {
        checkboxContainer.style.display = 'none';
    }
    
    // Check if amenitiesData is loaded
    if (!amenitiesData || !amenitiesData.years || !amenitiesData.totalLocations) {
        console.log('Amenities data not yet loaded, showing loading message');
        showLoadingMessage();
        return;
    }
    
    console.log('Creating default chart...');
    // Show total locations trend by default
    createDefaultCombinedChart();
    showDefaultMap();
    updateDefaultInsights();
}

function updateDefaultInsights() {
    const insightsContainer = document.getElementById('insights');
    if (!insightsContainer || !amenitiesData || !amenitiesData.years) {
        return;
    }
    
    const startYear = amenitiesData.years[0];
    const endYear = amenitiesData.years[amenitiesData.years.length - 1];
    const startCount = amenitiesData.totalLocations[0];
    const endCount = amenitiesData.totalLocations[amenitiesData.totalLocations.length - 1];
    const growth = endCount - startCount;
    const growthPercent = startCount > 0 ? ((growth / startCount) * 100).toFixed(1) : 0;
    
    const insightsHTML = `
        <div class="card bg-base-200">
            <div class="card-body p-4">
                <h4 class="font-bold text-lg mb-2">Overall Dataset Overview</h4>
                <div class="grid grid-cols-1 gap-4 text-sm">
                    <div class="border-b pb-2">
                        <h5 class="font-semibold text-base mb-2">Total Locations</h5>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <span class="font-medium">Starting (${startYear}):</span> ${startCount} locations
                            </div>
                            <div>
                                <span class="font-medium">Ending (${endYear}):</span> ${endCount} locations
                            </div>
                        </div>
                        <div class="mt-2">
                            <span class="font-medium">Growth:</span> ${growth > 0 ? '+' : ''}${growth} locations (${growthPercent}%)
                        </div>
                    </div>
                    <div>
                        <h5 class="font-semibold text-base mb-2">Dataset Summary</h5>
                        <div class="grid grid-cols-1 gap-2">
                            <div>
                                <span class="font-medium">Time Period:</span> ${startYear} - ${endYear} (${amenitiesData.years.length} years)
                            </div>
                            <div>
                                <span class="font-medium">Total Amenities:</span> ${amenitiesData.amenities.length} different types
                            </div>
                            <div>
                                <span class="font-medium">Data Points:</span> ${amenitiesData.years.length * amenitiesData.amenities.length} total observations
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    insightsContainer.innerHTML = insightsHTML;
}

function updateInsights(selectedAmenities) {
    const insightsContainer = document.getElementById('insights');
    if (!insightsContainer) {
        return;
    }
    
    if (!selectedAmenities || selectedAmenities.length === 0) {
        updateDefaultInsights();
        return;
    }
    
    let insightsHTML = '<div class="space-y-4">';
    
    selectedAmenities.forEach(amenity => {
        if (amenitiesData.trends[amenity]) {
            const startYear = amenitiesData.years[0];
            const endYear = amenitiesData.years[amenitiesData.years.length - 1];
            const startCount = amenitiesData.trends[amenity][0];
            const endCount = amenitiesData.trends[amenity][amenitiesData.trends[amenity].length - 1];
            const growth = endCount - startCount;
            const growthPercent = startCount > 0 ? ((growth / startCount) * 100).toFixed(1) : 0;
            
            const startPercentage = amenitiesData.totalLocations[0] > 0 ? 
                (startCount / amenitiesData.totalLocations[0] * 100).toFixed(1) : 0;
            const endPercentage = amenitiesData.totalLocations[amenitiesData.totalLocations.length - 1] > 0 ? 
                (endCount / amenitiesData.totalLocations[amenitiesData.totalLocations.length - 1] * 100).toFixed(1) : 0;
            const percentageGrowth = (parseFloat(endPercentage) - parseFloat(startPercentage)).toFixed(1);

            insightsHTML += `
                <div class="card bg-base-200">
                    <div class="card-body p-4">
                        <h4 class="font-bold text-lg mb-2">${amenity}</h4>
                        <div class="grid grid-cols-1 gap-4 text-sm">
                            <div class="border-b pb-2">
                                <h5 class="font-semibold text-base mb-2">Raw Counts</h5>
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <span class="font-medium">Starting (${startYear}):</span> ${startCount} locations
                                    </div>
                                    <div>
                                        <span class="font-medium">Ending (${endYear}):</span> ${endCount} locations
                                    </div>
                                </div>
                                <div class="mt-2">
                                    <span class="font-medium">Growth:</span> ${growth > 0 ? '+' : ''}${growth} locations (${growthPercent}%)
                                </div>
                            </div>
                            <div>
                                <h5 class="font-semibold text-base mb-2">Percentage of Total Locations</h5>
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <span class="font-medium">Starting (${startYear}):</span> ${startPercentage}%
                                    </div>
                                    <div>
                                        <span class="font-medium">Ending (${endYear}):</span> ${endPercentage}%
                                    </div>
                                </div>
                                <div class="mt-2">
                                    <span class="font-medium">Percentage Change:</span> ${percentageGrowth > 0 ? '+' : ''}${percentageGrowth}%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    });

    insightsHTML += '</div>';
    insightsContainer.innerHTML = insightsHTML;
}

function resetFilters() {
    console.log('Resetting filters...');
    
    // Reset dropdown
    const dropdown = document.getElementById('amenity-1');
    if (dropdown) {
        dropdown.value = '';
    }
    
    // Reset state filter
    const stateFilter = document.getElementById('state-filter');
    if (stateFilter) {
        stateFilter.value = '';
    }
    
    // Reset total locations checkbox
    const totalLocationsCheckbox = document.getElementById('show-total-locations');
    if (totalLocationsCheckbox) {
        totalLocationsCheckbox.checked = false;
    }
    
    // Hide checkbox container
    const checkboxContainer = document.getElementById('total-locations-checkbox-container');
    if (checkboxContainer) {
        checkboxContainer.style.display = 'none';
    }
    
    // Reset view to percentage
    currentView = 'percentage';
    const percentageButton = document.getElementById('percentage-view');
    const countButton = document.getElementById('count-view');
    
    if (percentageButton) {
        percentageButton.classList.add('btn-primary');
        percentageButton.classList.remove('btn-outline');
    }
    
    if (countButton) {
        countButton.classList.add('btn-outline');
        countButton.classList.remove('btn-primary');
    }
    
    // Reset current amenity
    currentAmenity = null;
    
    // Reload data without filters
    loadAmenitiesData();
}

function showLoadingMessage() {
    const chartContainer = document.getElementById('combined-chart');
    if (chartContainer) {
        chartContainer.innerHTML = `
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <div class="loading loading-spinner loading-lg mb-4"></div>
                    <p class="text-base-content/70">Loading chart data...</p>
                </div>
            </div>
        `;
    }
}

function showDefaultMap() {
    const mapContainer = document.getElementById('density-map');
    mapContainer.innerHTML = `
        <div class="flex items-center justify-center h-full">
            <div class="text-center">
                <div class="text-6xl mb-4">🗺️</div>
                <h3 class="text-lg font-semibold mb-2">Select an Amenity</h3>
                <p class="text-base-content/70">Choose an amenity from the dropdown above to view its geographic distribution across US cities.</p>
            </div>
        </div>
    `;
}

function createDensityMap(selectedAmenity) {
    // Clear previous map
    const mapContainer = document.getElementById('density-map');
    mapContainer.innerHTML = '';

    // Set up dimensions - much larger for better map visibility
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    let width = mapContainer.clientWidth - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom; // Much taller for larger map
    
    // Fallback width if container doesn't have proper dimensions
    if (width <= 0 || !mapContainer.clientWidth) {
        width = 1000; // Much larger default width for full-width map
        console.log('Using fallback width for map:', width);
    }
    
    console.log('Map dimensions:', { width, height, containerWidth: mapContainer.clientWidth });

    // Create SVG
    const svg = d3.select(mapContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add loading state
    svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', height / 2)
        .style('font-size', '14px')
        .style('fill', '#6b7280')
        .text('Loading city data...');

    // Get current filter values
    const stateFilter = document.getElementById('state-filter');
    const state = stateFilter ? stateFilter.value : '';
    
    // Build query string with filters
    let url = `/api/amenity-city-data/${encodeURIComponent(selectedAmenity)}`;
    const params = new URLSearchParams();
    if (state) params.append('state', state);
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    // Fetch city data
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Clear loading text
            svg.selectAll('text').remove();
            
            // Create the map visualization
            createMapVisualization(svg, data, width, height);
        })
        .catch(error => {
            console.error('Error loading city data:', error);
            svg.selectAll('text').remove();
            svg.append('text')
                .attr('text-anchor', 'middle')
                .attr('x', width / 2)
                .attr('y', height / 2)
                .style('font-size', '14px')
                .style('fill', '#ef4444')
                .text('Error loading map data');
        });
}

function createMapVisualization(svg, data, width, height) {
    // Define projection for US map - much larger scale for better visibility
    // Use a much larger scale to fill the available space
    const scale = Math.min(width * 1.2, height * 1.1);
    const projection = d3.geoAlbersUsa()
        .translate([width / 2, height / 2])
        .scale(scale);

    console.log('Map projection settings:', { width, height, scale });

    // Create path generator
    const path = d3.geoPath().projection(projection);

    // Load US states GeoJSON data
    d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json")
        .then(us => {
            // Add US states background
            svg.append("path")
                .datum(topojson.feature(us, us.objects.states))
                .attr("class", "states")
                .attr("d", path)
                .style("fill", "#f8f9fa")
                .style("stroke", "#dee2e6")
                .style("stroke-width", 1);

            // Add state borders
            svg.append("path")
                .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
                .attr("class", "state-borders")
                .attr("d", path)
                .style("fill", "none")
                .style("stroke", "#adb5bd")
                .style("stroke-width", 0.5);

            // Now add the city circles on top of the map
            addCityCircles(svg, data, projection, width, height);
        })
        .catch(error => {
            console.error("Error loading US map data:", error);
            // Fallback: just show city circles without basemap
            addCityCircles(svg, data, projection, width, height);
        });
}

function addCityCircles(svg, data, projection, width, height) {
    // Create color scale based on city counts
    const maxCount = d3.max(data.cities, d => d.count);
    const colorScale = d3.scaleSequential(d3.interpolateBlues)
        .domain([0, maxCount]);

    // Create radius scale for circle sizes - larger circles for better visibility
    const radiusScale = d3.scaleSqrt()
        .domain([0, maxCount])
        .range([5, 25]); // Increased from [3, 20] to [5, 25]

    // Add circles for each city
    svg.selectAll('.city-circle')
        .data(data.cities)
        .enter().append('circle')
        .attr('class', 'city-circle')
        .attr('cx', d => {
            const coords = projection([d.longitude, d.latitude]);
            return coords ? coords[0] : null;
        })
        .attr('cy', d => {
            const coords = projection([d.longitude, d.latitude]);
            return coords ? coords[1] : null;
        })
        .attr('r', d => radiusScale(d.count))
        .style('fill', d => colorScale(d.count))
        .style('opacity', 0.8) // Increased opacity for better visibility
        .style('stroke', '#fff')
        .style('stroke-width', 2) // Thicker stroke for better visibility
        .on('mouseover', function(event, d) {
            showMapTooltip(event, d);
        })
        .on('mouseout', function() {
            hideMapTooltip();
        });

    // Add title
    svg.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', width / 2)
        .attr('y', 20)
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .style('fill', '#374151')
        .text(`${data.amenity} - ${data.total_cities} Cities`);

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 120}, ${height - 80})`);

    // Legend title
    legend.append('text')
        .attr('text-anchor', 'middle')
        .attr('x', 60)
        .attr('y', -10)
        .style('font-size', '11px')
        .style('font-weight', 'bold')
        .style('fill', '#374151')
        .text('Count');

    // Legend circles
    const legendData = [maxCount, maxCount * 0.6, maxCount * 0.3, maxCount * 0.1];
    legend.selectAll('.legend-circle')
        .data(legendData)
        .enter().append('circle')
        .attr('class', 'legend-circle')
        .attr('cx', 60)
        .attr('cy', (d, i) => i * 15)
        .attr('r', d => radiusScale(d))
        .style('fill', d => colorScale(d))
        .style('opacity', 0.7)
        .style('stroke', '#fff')
        .style('stroke-width', 1);

    // Legend labels
    legend.selectAll('.legend-label')
        .data(legendData)
        .enter().append('text')
        .attr('class', 'legend-label')
        .attr('x', 80)
        .attr('y', (d, i) => i * 15 + 4)
        .style('font-size', '10px')
        .style('fill', '#374151')
        .text(d => Math.round(d));
}

function showMapTooltip(event, d) {
    const tooltipContent = `
        <div class="tooltip-content">
            <div class="tooltip-title"><strong>${d.city}, ${d.state}</strong></div>
            <div class="tooltip-item">
                <span class="tooltip-label">Count:</span>
                <span class="tooltip-value">${d.count}</span>
            </div>
        </div>
    `;
    
    let tooltip = d3.select('body').select('.map-tooltip');
    if (tooltip.empty()) {
        tooltip = d3.select('body').append('div')
            .attr('class', 'map-tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0, 0, 0, 0.8)')
            .style('color', 'white')
            .style('padding', '8px 12px')
            .style('border-radius', '6px')
            .style('font-size', '12px')
            .style('pointer-events', 'none')
            .style('z-index', '1000')
            .style('box-shadow', '0 4px 6px rgba(0, 0, 0, 0.1)')
            .style('opacity', 0);
    }
    
    tooltip.html(tooltipContent)
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .transition()
        .duration(200)
        .style('opacity', 1);
}

function hideMapTooltip() {
    d3.select('.map-tooltip')
        .transition()
        .duration(200)
        .style('opacity', 0)
        .remove();
}

// Tab functionality removed - now using side-by-side layout
