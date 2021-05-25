var data = [{ x: 'Sales', y1: 1500, y2: 2000 }, { x: 'Purchases', y1: 500, y2: 1500 }, { x: 'Sales2', y1: 1500, y2: 1000 }]

const config = {
    type: 'line',
    data: {
        datasets: [{
            label: 'y1 dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: data,
            parsing: {
                yAxisKey: 'y1'
            }
        }, 
        //un dataset por cada serie que desee agregar
        {
            label: 'y2 dataset',
            backgroundColor: 'rgb(180, 99, 200)',
            borderColor: 'rgb(180, 99, 200)',
            data: data,
            parsing: {
                yAxisKey: 'y2'
            }
        }]
    },
    options: {
        parsing: {
            xAxisKey: 'x'
        }
    }
};

document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    if (document.getElementById('relacionDiluyente')) {
        document.getElementById('relacionDiluyente').addEventListener('click', () => load_data('relacionDiluyente'));
    }
    // grafica
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
            console.log(`${graphId}:`);
            console.log(dataGraph);
            graficar(dataGraph)

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

function graficar(dataValue) {
    // countValue = 0;
    // dataValue.series1.forEach(element => {
    //     data.labels =countValue;
    //     countValue++;
    // });
    var chart = document.getElementById('chart').getContext("2d");
    if (chart) {
        // chart.remove;
        var myChart = new Chart(
            document.getElementById('chart'),
            config
        );
        // myChart.destroy;//para agregar una nueva serie
    }
}