
$(document).ready(function() {
    $('#overview_table').DataTable({
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

$(document).ready(function() {
    var trainings = [];
    $.getJSON("http://bec160b4.ngrok.io/analysis-images/", function (data) {

        for (var i = 0; i < data.length; i++) {
            $("#overview_body").apppend($(genenrateTableRow(data[i])));
        }
    });
});


function genenrateTableRow(dataEntry) {
    print(dataEntry)
    badge = getBadgeForEntry(dataEntry["quality"])
    return "<tr class='clickable-row' data-href='./details.html?id={id}'> \
    <th scope=\"row\">1</th> \
    <td>Mark</td> \
    <td>Otto</td>  \
    <td>@mdo</td> \
    <td class=\"quality_score_col\"><span class=\"badge badge-" + badge + " quality_score\">1.0</span></td> \
  </tr>"
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