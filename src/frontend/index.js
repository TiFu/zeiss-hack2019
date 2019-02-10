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
        console.log("row clicked?")
        window.location = $(this).data("href");
    });
});

$(document).ready(function($) {
    var trainings = [];
    $.getJSON(host + "/analysis-images/", function (data) {
        $("#loading-spinner").hide();
        $("#content").show();
        makeDisplacementOverview(data["distribution"])
        data = data["data"]
        for (var i = 0; i < data.length; i++) {
            data[i]["in_spec"] = !data[i]["in_spec"]
            row = table.row.add(generateTableRow(data[i])).draw().node();
            $(row).addClass("clickable-row");
            $(row).data("href", "./details.html?id=" + data[i]["id"])
            $(row).click(function() {
                window.location = $(this).data("href");
            })
            console.log($(row).data("href"))
        }
    });
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
            title: { "text": "Translation in Millimeter" },
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
        series: [{
        name: 'Samples',
        type: 'column',
        yAxis: 0,
        data: data[1],
        tooltip: {
            headerFormat: '',
            formatter: function () {
                return '<span style="font-weight: bold; color: {series.color}">{series.name}</span>: <b>{point.y:.0f}</b> '
            }
        }
        }]
    });
}

function submitFiles() {
    console.log("submitting files")
    var form = new FormData(); 
//    console.log($("#"))
    form.append("picture_left_before", $("#leftBefore")[0].files[0]);
    console.log("first done")
    form.append("picture_left_after", $("#leftAfter")[0].files[0]);
    console.log("first done 2")
    form.append("picture_right_before", $("#rightBefore")[0].files[0]);
    console.log("first done 3")
    form.append("picture_right_after", $("#rightAfter")[0].files[0]);
    console.log("first done 4")

    $.ajax({
        type: "POST",
        url: host + "/analysis-images/",
        data: form,
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, 
      }).done(function (data) {
        window.location = "./details.html?id=" + data["id"]
      }).fail(function() {
          console.log("failed uploading");
      });
}