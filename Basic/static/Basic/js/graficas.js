const labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
];

const data = {
    labels: labels,
    datasets: [{
        label: 'Mi primer dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 10, 5, 2, 20, 30, 45],
    }]
};

const config = {
    type: 'line',
    data,
    options: {}
};

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('relacionDiluyente')) {
        document.getElementById('relacionDiluyente').addEventListener('click', () => load_data('relacionDiluyente'));
    }
    if (document.getElementById('chart')) {
        var myChart = new Chart(
            document.getElementById('chart'),
            config
        );
    }


});

function load_data(graphId) {
    const pozo = document.querySelector('#id_pozo').value;
    const aceite = document.querySelector('#id_aceite').value;
    const apiCabeza = document.querySelector('#id_apiCabeza').value;
    const apiDiluyente = document.querySelector('#id_apiDiluyente').value;
    const apiMezclaHumedo = document.getElementById('id_apiMezclaHumedo').innerHTML;
    fetch(`/graficas/${graphId}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            pozo: pozo,
            aceite: aceite,
            apiCabeza: apiCabeza,
            apiDiluyente: apiDiluyente,
            apiMezclaHumedo: apiMezclaHumedo
        })
    })
        .then(response => response.json())
        // .then(status)
        .then(dataGraph => {
            // Print data
            console.log(`${graphId}:`);
            console.log(dataGraph);

            // ... do something else with dataGraph ...
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