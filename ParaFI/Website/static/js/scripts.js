document.addEventListener('DOMContentLoaded', function() {
    // Initialize simple CSS-based gauges if they exist
    if (document.querySelector('.gauge')) {
        updateGauges(); // Initialize gauges with initial zero state
    }

    // Load and initialize Chart.js-based gauges if required
    if (document.querySelector('.graph')) {
        loadAndInitializeCharts();
    }
});

// Function to dynamically load Chart.js and initialize charts
function loadAndInitializeCharts() {
    var script = document.createElement('script');
    script.onload = initializeChartGauges; // Initialize charts after loading
    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
    document.head.appendChild(script);
}

// Function to initialize Chart.js gauges
function initializeChartGauges() {
    var gaugeOptions = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100], // Initial empty state
                backgroundColor: ['#007BFF', '#e9ecef'],
                borderWidth: 0
            }]
        },
        options: {
            rotation: 1 * Math.PI,
            circumference: 1 * Math.PI,
            cutout: '90%',
            responsive: true,
            animation: {
                animateRotate: true
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };

    // Initialize all gauges with empty data
    const downloadSpeedGauge = new Chart(document.getElementById('downloadSpeedGauge'), gaugeOptions);
    const pingSpeedGauge = new Chart(document.getElementById('pingSpeedGauge'), gaugeOptions);
    const uploadSpeedGauge = new Chart(document.getElementById('uploadSpeedGauge'), gaugeOptions);

    // Update gauges on button click
    document.querySelector('.speed-test').addEventListener('click', function() {
        // Simulated speed test results
        const downloadSpeed = Math.random() * 100;
        const uploadSpeed = Math.random() * 100;
        const ping = Math.random() * 100;

        downloadSpeedGauge.data.datasets[0].data = [downloadSpeed, 100 - downloadSpeed];
        pingSpeedGauge.data.datasets[0].data = [ping, 100 - ping];
        uploadSpeedGauge.data.datasets[0].data = [uploadSpeed, 100 - uploadSpeed];

        // Update the charts
        downloadSpeedGauge.update();
        pingSpeedGauge.update();
        uploadSpeedGauge.update();

        // Update last tested time
        document.getElementById('lastTested').textContent = new Date().toLocaleString();
    });
}

// Function to update simple CSS gauges
function updateGauges() {
    var now = new Date().toLocaleString();
    document.getElementById('lastTested').textContent = now;

    const downloadSpeed = Math.random() * 100;
    const uploadSpeed = Math.random() * 100;

    const downloadGauge = document.getElementById('downloadGauge').querySelector('.gauge-value');
    const uploadGauge = document.getElementById('uploadGauge').querySelector('.gauge-value');

    downloadGauge.style.width = downloadSpeed + '%';
    uploadGauge.style.width = uploadSpeed + '%';

    downloadGauge.parentNode.querySelector('span').textContent = downloadSpeed.toFixed(2) + ' Mbps';
    uploadGauge.parentNode.querySelector('span').textContent = uploadSpeed.toFixed(2) + ' Mbps';
}
