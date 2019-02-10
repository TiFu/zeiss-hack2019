function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};



$(document).ready(function() {
    $.getJSON(host + "/analysis-images/" + getUrlParameter("id"), function (data) {
        data["in_spec"] = !data["in_spec"]
        
        $("#id-header").html("Sample " + data["picture_id"]);

        $("#overlay_left").attr("src", data["overlay_left"].replace("http://localhost:8765", host));
        $("#overlay_right").attr("src", data["overlay_right"].replace("http://localhost:8765", host))

        $("#left_before").attr("src", data["picture_left_before"].replace(".tif", ".png"))
        $("#left_after").attr("src", data["picture_left_after"].replace(".tif", ".png"))
        $("#right_before").attr("src", data["picture_right_before"].replace(".tif", ".png"))
        $("#right_after").attr("src", data["picture_right_after"].replace(".tif", ".png"))
        $("#time").html("<b>Date:</b> " + dateFormat(data["date_before"]) + " - " + dateFormat(data["date_after"]))
        console.log(data)
        $("#transform_left").html("(" + numberFormat(data["translation_val_left_x"]) + " mm, " + numberFormat(data["translation_val_left_y"]) + " mm)")
        $("#transform_right").html("(" + numberFormat(data["translation_val_right_x"]) + " mm, " + numberFormat(data["translation_val_right_y"]) + " mm)")
        $("#rotation_left").html(angleFormat(data["rotation_val_left"]))
        $("#rotation_right").html(angleFormat(data["rotation_val_right"]))

        badge = getBadgeForEntry(data["quality"])
        $("#quality_score").html("<b>Quality Score:</b> <span style=\"margin-left: 5px\" class=\"badge badge-" + badge + " quality_score\">" + numberFormat(data["quality"]) + "</span>")
        console.log("received data", data)
        $("#loading-spinner").hide();
        $("#content").show();

    }); 
})

