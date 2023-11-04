
function run_request(type, url, data_in, el_status, callback) {
    $.ajax({
        url: url,
        method: type,
        data: data_in,
        dataType: "json",
        beforeSend(xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + inputToken.value);
        },
        success: (data) => {
            el_status.value = JSON.stringify(data, null, 4);
            el_status.style.height = (el_status.scrollHeight) + "px";
            if (typeof callback == "function") {
                callback(data);
            }
        },
        error: function (jqXHR, e) {
            console.log("status: " + jqXHR.status + " (" + jqXHR.statusText + ")");
            console.log(jqXHR.responseJSON);
            el_status.value = "status: " + jqXHR.status + " (" + jqXHR.statusText + ")\n";
            el_status.value += JSON.stringify(jqXHR.responseJSON, null, 4);
            el_status.style.height = el_status.scrollHeight + "px"
        }
    });
}