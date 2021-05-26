// var data = [{ x: 'Sales', series1: 1500, series2:0 }, { x: 'Purchases', series1: 500, series2:0 }, { x: 'Sales2', series1: 1500, series2:0 }]

document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    if (document.getElementById('relacionDiluyente')) {
        document.getElementById('relacionDiluyente').addEventListener('click', () => load_data('relacionDiluyente'));
    }
    // grafica default
    load_data('relacionDiluyente');


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
            // console.log(dataGraph);
            graficar(dataGraph.datos, dataGraph.params);

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

function graficar(dataValue, params) {
    var data = [];
    // data.splice(0, data.length);
    dataValue.forEach(element => {
        data.push(element);
    });
    // console.log(data);
    document.querySelector("#chartContent").innerHTML = '<canvas id="chart"></canvas>';
    var chart = document.getElementById('chart').getContext("2d");
    if (chart) {
        var myChart = new Chart(
            document.getElementById('chart'),
            configGraph(data, params)
        );
    }
}
function configGraph(data, params) {
    selfDataset = [];
    for (var key in data[0]) {
        if (key != 'x') {
            // console.log(params[key].label);
            dataset = {
                label: params[key].label,
                backgroundColor: params[key].backgroundColor,
                borderColor: params[key].borderColor,
                data: data,
                parsing: {
                    yAxisKey: key
                }
            };
            selfDataset.push(dataset);
            // console.log(selfDataset);
        }
    }
    var config = {
        type: 'line',
        data: {
            datasets: selfDataset
        },
        options: {
            parsing: {
                xAxisKey: 'x'
            }
            //configurar titulos y demas
        }
    };
    return config;
}