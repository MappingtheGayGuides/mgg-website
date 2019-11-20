var settings = getSettings();

function detectIE() {
  var ua = window.navigator.userAgent;

  var msie = ua.indexOf('MSIE ');
  if (msie > 0) {
    // IE 10 or older => return version number
    return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
  }

  var trident = ua.indexOf('Trident/');
  if (trident > 0) {
    // IE 11 => return version number
    var rv = ua.indexOf('rv:');
    return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
  }

  var edge = ua.indexOf('Edge/');
  if (edge > 0) {
    // Edge (IE 12+) => return version number
    return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
  }

  // other browser
  return false;
}

function getSettings() {
    var app_url = window.location.pathname;

    // remove trailing slash if any
    if (app_url.charAt(app_url.length - 1) == '/')
      app_url = app_url.substr(0, app_url.length - 1);

    // get settings url
    app_url += '/__settings__/';

    var xhr = $.ajax({
        dataType: "json",
        url: app_url,
        async: false
    });
    if (xhr.status == 200) {
        return JSON.parse(xhr.responseText)
    }
}

function showToolbar() {

}

function hideToolbar() {

}

$(document).ready(function () {
    $("<link/>", {
        rel: "stylesheet",
        type: "text/css",
        href: "/__static__/frontend/css/shinyapps.css"
    }).appendTo("head");
});
