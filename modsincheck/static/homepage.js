//homepage.js

var button = document.getElementById("submit-button");
get_mod_or_subreddit = function () {
    var text = document.getElementById("search").value;
    var curr_url = window.location.href;
    index_of_home = curr_url.indexOf('/home');
    curr_url = curr_url.replace('?', '').replace('/home', '').replace('#', '');
    nametype = auto_complete_data.find(n => n.name === text);
    //console.log(nametype);
    if (nametype.mod_or_subreddit === "moderator") {
        window.open(curr_url  + 'mod_info/' + text, name='_self');
    } else if (nametype.mod_or_subreddit === "subreddit") {
        window.open(curr_url  + 'subreddit_info/' + text, name='_self')
    }
}

// Get the input field
var input = document.getElementById("search");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard

    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        get_mod_or_subreddit();
    }

    });

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawDateFormatTable);

function drawDateFormatTable() {

    function get_data_and_options(scores, dates) {
        dates = dates.split(",")
        scores = scores.split(",")
        rows = new Array();
        for (i = 0; i < dates.length; i++){
            var curr_date = dates[i].replace(/[\\\]\["\b]+/g, "").replace(" ", "");
            var curr_score = scores[i].replace(/[\\\]\[]+/g, "");
            rows.push([new Date(curr_date), Number(curr_score)])
        }
        //console.log(rows)
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
        var options = {
            title: 'Censorship Score Over Time',
            allowHtml: true,
            lineWidth: 5,
            curveType: 'function',
            hAxis: {
                title: 'Time',
                ticks: hAxisTicks,
                format: 'M/d/yyyy',
            },
            vAxis: {
                title: 'Post Removal Frequency',
                viewWindow: {
                    min: 0,
                    max: 100
                }
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

        return [data, options]
    }

    // Draw the data
    var chart1 = new google.visualization.LineChart(document.getElementById('chart1'));
    var chart2 = new google.visualization.LineChart(document.getElementById('chart2'));
    var chart3 = new google.visualization.LineChart(document.getElementById('chart3'));

    chart_content_1 = get_data_and_options(mod_1.scores, mod_1.dates)
    chart_content_2 = get_data_and_options(mod_2.scores, mod_2.dates)
    chart_content_3 = get_data_and_options(mod_3.scores, mod_3.dates)

    chart1.draw(chart_content_1[0], chart_content_1[1]);
    chart2.draw(chart_content_2[0], chart_content_2[1]);
    chart3.draw(chart_content_3[0], chart_content_3[1]);
    
    function resize () {
        chart_content_1 = get_data_and_options(mod_1.scores, mod_1.dates)
        chart_content_2 = get_data_and_options(mod_2.scores, mod_2.dates)
        chart_content_3 = get_data_and_options(mod_3.scores, mod_3.dates)

        chart1.draw(chart_content_1[0], chart_content_1[1]);
        chart2.draw(chart_content_2[0], chart_content_2[1]);
        chart3.draw(chart_content_3[0], chart_content_3[1]);
    }
    window.onload = resize;
    window.onresize = resize;
}

function animateValue(id, start, end, duration, mod) {
    if (start === end) return;
    var range = end - start;
    var current = start;
    var increment = end > start? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);
    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = '<i>'+ '<a href=' + window.location.href + 'mod_info/' + mod.name + '>' + mod.name+'</a></i>' + ' Current Score: ' + current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

window.onload = function() {
    var obj = document.getElementById("recent-score");
    var mod_lst = [mod_1, mod_2, mod_3];
    for (i = 0; i < mod_lst.length; i++) {
        if (mod_lst[i].most_recent_score === 0) {
            obj.innerHTML = mod_lst[i].name + ' Current Score: ' + mod_lst[i].most_recent_score
        }
        else {
            animateValue("animate_" + (i + 1), 0, mod_lst[i].most_recent_score, 600, mod_lst[i]);
        }
    }
}



var input = document.getElementById("search");
console.log(auto_complete_data)
autocomplete({
    input: input,
    fetch: function(text, update) {
        text = text.toLowerCase();
        // you can also use AJAX requests instead of preloaded data
        var suggestions = auto_complete_data.filter(n => n.name.toLowerCase().startsWith(text))
        console.log(suggestions);
        update(suggestions);
    },
    onSelect: function(item) {
        input.value = item.name;
    },
    minLength: 1,
})
