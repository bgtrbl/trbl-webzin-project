'use strict';
var csrfcookie = function () {
    var cookieValue, name, cookies, cookie;
    cookieValue = null;
    name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrfSafeMethod = function (method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
