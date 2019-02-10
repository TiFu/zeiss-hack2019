table = null;

$(document).ready(function() {
    table = $('#overview_table').DataTable({
        "searching": false,
        "ordering": true,
        "lengthChange": false
    });
} );

$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

$(document).ready(function($) {
    var trainings = [];
    $.getJSON("http://bec160b4.ngrok.io/analysis-images/", function (data) {

        for (var i = 0; i < data.length; i++) {
            row = table.row.add(generateTableRow(data[i])).draw().node();
            $(row).addClass("clickable-row");
            $(row).data("href", "./details.html?id=" + data[i]["id"])
        }
    });
});

$(document).ready(function($) {
    makeDisplacementOverview([
        [0, 1, 2, 3, 4, 5, 6],
        [10, 20, 30, 20, 10, 0, 5]
    ])
});


function generateTableRow(dataEntry) {
    console.log(dataEntry)
    badge = getBadgeForEntry(dataEntry["quality"])
    return [
        dataEntry["picture_id"].toString(),
        dateFormat(dataEntry["date_after"]),
        formatSpec(dataEntry),
        (dataEntry["defect"] == null ? "" : formatDefect(dataEntry["defect"])),
        "<span class=\"badge badge-" + badge + " quality_score\">" + numberFormat(dataEntry["quality"]) + "</span>"
    ]
}

function formatSpec(dataEntry) {
    if (dataEntry["in_spec"]) {
        return "<i class=\"font_increase text-success fas fa-check-square\"></i>"
    } else {
        return "<i class=\"font_increase text-danger fas fa-times-circle\"></i>"
    }
}

function formatDefect(type) {
    if (type == "position") {
        return "Position out of spec."
    } else if (type == "surface") {
        return "Surface was damaged."
    } else {
        return "Unknown defect."
    }
}

function numberFormat(number) {
    if (number == null) {
        return (0).toFixed(2);
    }
    return Number.parseFloat(number).toFixed(2);
}

function dateFormat(dateString) {
    if (dateString == null) {
        return "";
    }
    const m = new Date(dateString)
    let formatted = (m.getUTCDate()) +"."+ (m.getUTCMonth()+1) +"."+ m.getUTCFullYear() + " " + m.getUTCHours() + ":" + m.getUTCMinutes() + ":" + m.getUTCSeconds();
    return formatted;
}

function getBadgeForEntry(quality) {
    if (quality >= 1) {
        return "success"
    } else if (quality >= 0) {
        return "warning"
    } else {
        return "danger"
    }
}


function makeDisplacementOverview(data) {
    Highcharts.chart('chart_container', {
        credits: {
            enabled: false
        },
        chart: {
        zoomType: 'xy'
        },
        title: {
        text: 'Distribution of Translation in Millimeter between first and second image'
        },
        xAxis: [{
        categories: data[0]
        }],
        yAxis: [{ // Primary yAxis
        labels: {
            format: '{value}',
            style: {
            color: Highcharts.getOptions().colors[1]
            }
        },
        title: {
            text: 'Number of Samples',
            style: {
            color: Highcharts.getOptions().colors[1]
            }
        }
        }],
    
        tooltip: {
        shared: true
        },
    
        series: [{
        name: 'Displacement in Millimeter',
        type: 'column',
        yAxis: 0,
        data: data[1],
        tooltip: {
            pointFormat: '<span style="font-weight: bold; color: {series.color}">{series.name}</span>: <b>{point.y:.2f} mm</b> '
        }
        }]
    });
}