// Dashboard JavaScript functionality
let attackChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    startRealTimeUpdates();
});

// Initialize attack chart
function initializeChart() {
    const ctx = document.getElementById('attackChart');
    if (!ctx) return;
    
    // Get chart data from template
    const hourlyData = window.hourlyData || [];
    
    attackChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hourlyData.map(item => item.hour),
            datasets: [{
                label: 'Attack Attempts',
                data: hourlyData.map(item => item.count),
                borderColor: 'rgb(255, 107, 107)',
                backgroundColor: 'rgba(255, 107, 107, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Start real-time updates
function startRealTimeUpdates() {
    // Update statistics every 30 seconds
    setInterval(updateStats, 30000);
    
    // Update chart every 60 seconds
    setInterval(updateChart, 60000);
}

// Update dashboard statistics
function updateStats() {
    fetch('/api/stats/')
        .then(response => response.json())
        .then(data => {
            updateStatCard('total-attacks', data.total_attacks);
            updateStatCard('unique-ips', data.unique_ips);
            updateStatCard('recent-attacks', data.recent_attacks);
        })
        .catch(error => console.error('Error updating stats:', error));
}

// Update individual stat card
function updateStatCard(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
        element.classList.add('text-success');
        setTimeout(() => {
            element.classList.remove('text-success');
        }, 1000);
    }
}

// Update chart data
function updateChart() {
    // This would fetch new chart data from the server
    // For now, we'll just reload the page
    location.reload();
}
