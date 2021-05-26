// var data = [{ x: 'Sales', series1: 1500, series2:0 }, { x: 'Purchases', series1: 500, series2:0 }, { x: 'Sales2', series1: 1500, series2:0 }]

document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    if (document.getElementById('relacionDiluyente')) {
        document.getElementById('relacionDiluyente').addEventListener('click', () => load_data('relacionDiluyente'));
    }
    if (document.getElementById('diluyenteRequerido')) {
        document.getElementById('diluyenteRequerido').addEventListener('click', () => load_data('diluyenteRequerido'));
    }
    if (document.getElementById('limiteRestriccion')) {
        document.getElementById('limiteRestriccion').addEventListener('click', () => load_data('limiteRestriccion'));
    }
    // grafica default
    if (document.getElementById('id_apiMezclaHumedo')) {
        load_data('relacionDiluyente');
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
            // console.log(dataGraph);
            graficar(dataGraph);

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

function graficar(dataGraph) {
    var data = [];
    // data.splice(0, data.length);
    dataGraph.datos.forEach(element => {
        data.push(element);
    });
    // console.log(data);
    document.querySelector("#chartContent").innerHTML = '<canvas id="chart"></canvas>';
    var chart = document.getElementById('chart').getContext("2d");
    if (chart) {
        var myChart = new Chart(
            document.getElementById('chart'),
            configGraph(data, dataGraph.serieParams, dataGraph.graphParams)
        );
    }
}
function configGraph(data, serieParams, graphParams) {
    selfDataset = [];
    for (var key in data[0]) {
        if (key != 'x') {
            // console.log(params[key].label);
            dataset = {
                label: serieParams[key].label,
                backgroundColor: serieParams[key].backgroundColor,
                borderColor: serieParams[key].borderColor,
                tension: 0.4,
                fill: false,
                data: data,
                parsing: {
                    yAxisKey: key
                }
            };
            selfDataset.push(dataset);
            // console.log(selfDataset);
        }
    }
    // console.log(graphParams.titleXAxis);
    var config = {
        type: 'line',
        data: {
            datasets: selfDataset
        },
        options: {
            responsive: true,
            parsing: {
                xAxisKey: 'x'
            },
            plugins: {
                title: {
                    display: true,
                    text: graphParams.title
                }
            },
            interaction: {
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: graphParams.titleXAxis
                    }
                },
                y: {
                    display: true,
                    max: graphParams.maxYValue,
                    title: {
                        display: true,
                        text: graphParams.titleYAxis
                    }
                }
            }
        }
    };
    return config;
}