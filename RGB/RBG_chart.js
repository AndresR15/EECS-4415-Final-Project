<canvas id="myChart" width="400" height="400"></canvas>
<script>
var ctx = document.getElementById("myChart").getContext('2d');
var mydoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["black", "blue", "brown", "green", "grey", "orange", "purple", "red", "white", "yellow"],
        datasets: [{
            label: 'Most Common Thumbnail colors',
            data: [10388, 5113, 1295, 1079, 12000, 60, 1180, 289, 3129, 801],
            backgroundColor: [
                'rgba(0, 0, 0)',
                'rgba(0, 0, 235)',
                'rgba(133, 87, 35)',
                'rgba(57, 255, 20)',
                'rgba(213, 213, 213)', 
                'rgba(253, 106, 106)', 
                'rgba(149, 33, 246)',
                'rgba(237, 41, 157)',
                'rgba(255, 255, 255)',
                'rgba(255, 255, 0)'
            ]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>