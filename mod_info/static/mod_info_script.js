google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawDateFormatTable);

function goBack() {
    window.history.back();
}

rows = new Array();
for(i = 0; i < dates.length; i++){
    rows.push([new Date(dates[i]), scores[i]])
}

function drawDateFormatTable() {

    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Score');
    data.addRows(rows) 

    const oneDay = (1000 * 60 * 60 * 24);
    //debugger;
    let hAxisTicks = [];
    let dateRange = data.getColumnRange(0);
    for (var i = dateRange.min.getTime(); i <= dateRange.max.getTime(); i = i + oneDay) {
        hAxisTicks.push(new Date(i));
    }

    // Draw the data
    var chart = new google.visualization.LineChart(document.getElementById('score_over_time_chart'));

    var options = {
        title: 'Censorship Score Over Time',
        allowHtml: true,
        curveType: 'function',
        lineWidth: 5,
        hAxis: {
            title: 'Time',
            ticks: hAxisTicks,
            format: 'M/d/yyyy',
        },
        vAxis: {
            title: 'Post Removal Frequency',
            minValue: 0,
        },
        timeline: {
            groupByRowLabel: true
            },
        animation:{
            startup: true,
            duration: 1000,
            easing: 'out',
        },
        legend: { position: "top" },
        colors: ['#8A2BE2'] //Line color: blueviolet
    };

    chart.draw(data, options);
    function resize () {
        var chart = new google.visualization.LineChart(document.getElementById('score_over_time_chart'));
        chart.draw(data, options);
    }
    window.onload = resize;
    window.onresize = resize;
}

function animateValue(id, start, end, duration) {
    if (start === end) return;
    var range = end - start;
    var current = start;
    var increment = end > start? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);

    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = 'Current Score: ' + current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

window.onload = function() {
    var obj = document.getElementById("recent-score");
    if (most_recent_score === 0) {
        obj.innerHTML = 'Current Score: ' + most_recent_score
    }
    else {
        animateValue("recent-score", 0, most_recent_score, 600);
    }
}