const host = "https://cbc51386.ngrok.io"

function dateFormat(dateString) {
    if (dateString == null) {
        return "";
    }
    const m = new Date(dateString)
    let formatted = (makeTwoDigit(m.getUTCDate())) +"."+ (makeTwoDigit(m.getUTCMonth()+1)) +"."+ m.getUTCFullYear() + " " + makeTwoDigit(m.getUTCHours()) + ":" + makeTwoDigit(m.getUTCMinutes()) + ":" + makeTwoDigit(m.getUTCSeconds());
    return formatted;
}

function makeTwoDigit(number) {
    if (number >= 10) {
        return number;
    } else {
        return "0" + number.toString()
    }
}

let formatDate = dateFormat;

function getBadgeForEntry(quality) {
    if (quality >= 1) {
        return "success"
    } else if (quality > 0) {
        return "warning"
    } else {
        return "danger"
    }
}

function numberFormat(number) {
    if (number == null) {
        return (0).toFixed(2);
    }
    return Number.parseFloat(number).toFixed(2);
}

function angleFormat(number) {
    if (number == null) {
        return (0).toFixed(2) + "°";
    } else {
        return (Number.parseFloat(number) * 180.0 / Math.PI).toFixed(2) + "°"
    }
}
