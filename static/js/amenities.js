// Amenities visualization for Mapping the Gay Guides using D3.js

let amenitiesData = [];
let currentChart = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Amenities.js loaded, initializing...');

    try {
        loadAmenitiesData();
        setupEventListeners();
    } catch (error) {
        console.error('Error during amenities initialization:', error);
        document.getElementById('percentage-chart').innerHTML =
            '<p class="text-danger">Error initializing amenities visualization. Please check console for details.</p>';
    }
});

function loadAmenitiesData() {
    console.log('Loading amenities data...');

    // For now, use sample data directly to get the visualization working
    // TODO: Uncomment the API call when the endpoint is working
    /*
    fetch('/api/amenities-trends')
        .then(response => {
            console.log('Response received:', response.status, response.ok);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Amenities data loaded:', data);

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
        })
        .catch(error => {
            console.error('Error loading amenities data:', error);
            // Fallback to sample data for development
            loadSampleData();
        });
    */

    // Use sample data for now
    loadSampleData();
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
}

function populateAmenityDropdowns() {
    console.log('Populating amenity dropdowns...');

    const dropdown = document.getElementById('amenity-1');
    const amenities = amenitiesData.amenities || [];

    if (dropdown) {
        // Clear existing options except the first one
        dropdown.innerHTML = '<option value="">Select an amenity...</option>';

        // Add amenity options
        amenities.forEach(amenity => {
            const option = document.createElement('option');
            option.value = amenity;
            option.textContent = amenity;
            dropdown.appendChild(option);
        });
    }
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

    // Auto-update on dropdown change
    const dropdown = document.getElementById('amenity-1');
    if (dropdown) {
        dropdown.addEventListener('change', updateChart);
    }
}

function updateChart() {
    console.log('Updating chart...');

    const dropdown = document.getElementById('amenity-1');
    const selectedAmenity = dropdown ? dropdown.value : '';

    if (!selectedAmenity) {
        showLoadingMessage();
        return;
    }

    const selectedAmenities = [selectedAmenity];

    // Create both charts
    createPercentageChart(selectedAmenity);
    createCountChart(selectedAmenity);

    currentChart = true;

    // Update insights
    updateInsights(selectedAmenities);
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

function showLoadingMessage() {
    const percentageContainer = document.getElementById('percentage-chart');
    const countContainer = document.getElementById('count-chart');
    
    percentageContainer.innerHTML = `
        <div class="loading">
            <div class="text-center">
                <div class="loading loading-spinner loading-lg mb-4"></div>
                <p class="text-base-content/70">Select an amenity to view percentage trends</p>
            </div>
        </div>
    `;
    
    countContainer.innerHTML = `
        <div class="loading">
            <div class="text-center">
                <div class="loading loading-spinner loading-lg mb-4"></div>
                <p class="text-base-content/70">Select an amenity to view count trends</p>
            </div>
        </div>
    `;
}

function showNoDataMessage() {
    const percentageContainer = document.getElementById('percentage-chart');
    const countContainer = document.getElementById('count-chart');
    
    percentageContainer.innerHTML = `
        <div class="loading">
            <div class="text-center">
                <div class="text-6xl mb-4">📊</div>
                <p class="text-base-content/70">No data available for selected amenity</p>
            </div>
        </div>
    `;
    
    countContainer.innerHTML = `
        <div class="loading">
            <div class="text-center">
                <div class="text-6xl mb-4">📊</div>
                <p class="text-base-content/70">No data available for selected amenity</p>
            </div>
        </div>
    `;
}

function resetFilters() {
    console.log('Resetting filters...');

    const dropdown = document.getElementById('amenity-1');
    if (dropdown) {
        dropdown.value = '';
    }

    showLoadingMessage();
    updateInsights([]);
}

function updateInsights(selectedAmenities) {
    const insightsContainer = document.getElementById('insights');

    if (selectedAmenities.length === 0) {
        insightsContainer.innerHTML = '<p>Select amenities to see insights about their historical trends and patterns.</p>';
        return;
    }

    let insightsHTML = '<div class="space-y-4">';

    selectedAmenities.forEach(amenity => {
        if (amenitiesData.trends && amenitiesData.trends[amenity]) {
            const trend = amenitiesData.trends[amenity];
            const startCount = trend[0];
            const endCount = trend[trend.length - 1];
            const growth = endCount - startCount;
            const growthPercent = startCount > 0 ? ((growth / startCount) * 100).toFixed(1) : 0;

            // Calculate percentage statistics
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
                                        <span class="font-medium">Starting (1965):</span> ${startCount} locations
                                    </div>
                                    <div>
                                        <span class="font-medium">Ending (1979):</span> ${endCount} locations
                                    </div>
                                    <div>
                                        <span class="font-medium">Growth:</span> ${growth > 0 ? '+' : ''}${growth} locations
                                    </div>
                                    <div>
                                        <span class="font-medium">Growth Rate:</span> ${growthPercent}%
                                    </div>
                                </div>
                            </div>
                            <div>
                                <h5 class="font-semibold text-base mb-2">Relative Percentages</h5>
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <span class="font-medium">Starting (1965):</span> ${startPercentage}% of total
                                    </div>
                                    <div>
                                        <span class="font-medium">Ending (1979):</span> ${endPercentage}% of total
                                    </div>
                                    <div>
                                        <span class="font-medium">Change:</span> ${percentageGrowth > 0 ? '+' : ''}${percentageGrowth}%
                                    </div>
                                    <div>
                                        <span class="font-medium">Total Locations (1979):</span> ${amenitiesData.totalLocations[amenitiesData.totalLocations.length - 1]}
                                    </div>
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
