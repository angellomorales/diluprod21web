function enviarAJAX(url, bodyJson) {
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: bodyJson
    })
        .then(response => response.json())
        // .then(status)
        .then(dataResponse => {
            // Print data
            // console.log(dataGraph);
            if (url.includes("graficar")) {
                dataGraph=dataResponse;
                graficar(dataGraph);
            }
            else{
                cargarPredata(dataResponse)
            }

        })
        .catch(err => console.log(err));
}

//funcion propia sugerida por django https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax para sacar el csrf de las cookies cuando ya estaba presente
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}