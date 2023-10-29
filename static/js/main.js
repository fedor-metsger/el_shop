
function getToken(url, data, element) {
    $.ajax({
        url: url,
        method: "POST",
        data: data,
        dataType: "json",
        success: (data) => {
            console.log(data["access"]);
            element.value = JSON.stringify(data, null, 4);
            element.style.height = (getTokenForm.elements["tokenPost"].scrollHeight) + "px"
        },
        error: (error) => {
            console.log(error);
            element.value = error;
            element.style.height = (getTokenForm.elements["tokenPost"].scrollHeight) + "px"
        }
    });
}