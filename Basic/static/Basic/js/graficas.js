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
    document.querySelector(dataGraph.contenedor).innerHTML = '<canvas id="chart"></canvas>';
    var ctx = document.getElementById('chart').getContext("2d");
    if (chart) {
        var myChart = new Chart(ctx,
            configGraph(data, dataGraph.serieParams, dataGraph.graphParams)
        );
    }
}
function configGraph(data, serieParams, graphParams) {
    selfDataset = [];
    for (var key in data[0]) {
        if (key != 'x') {
            // console.log(serieParams[key]);
            dataset = {
                label: serieParams[key].label,
                backgroundColor: serieParams[key].backgroundColor,
                borderColor: serieParams[key].borderColor,
                tension: 0.4,
                fill: false,
                data: data,
                pointStyle: serieParams[key].pointStyle,
                pointRadius: serieParams[key].pointRadius,
                pointBorderColor: 'rgb(125, 125, 125)',
                parsing: {
                    yAxisKey: key
                },
                animations: {
                    y: {
                        duration: 500,
                        delay: 50
                    }
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
                    text: graphParams.title,
                    font: {
                        size: 20,
                    }
                },
                zoom: {
                    zoom: {
                        drag: {
                            enabled: true,
                        },
                        wheel: {
                            enabled: true,
                        },
                        mode: 'xy'
                    }
                },
                tooltip: {
                    position: 'nearest'
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
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
                    suggestedMin: 0,
                    title: {
                        display: true,
                        text: graphParams.titleYAxis
                    }
                }
            },
            animations: {
                y: {
                    easing: 'linear',
                }
            }
        }
    };
    return config;
}