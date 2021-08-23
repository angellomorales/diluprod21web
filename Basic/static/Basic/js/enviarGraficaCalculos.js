// var data = [{ x: 'Sales', series1: 1500, series2:0 }, { x: 'Purchases', series1: 500, series2:0 }, { x: 'Sales2', series1: 1500, series2:0 }]

document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    // if (document.getElementById('relacionDiluyente')) {
    //     document.getElementById('relacionDiluyente').addEventListener('click', () => load_data('relacionDiluyente'));
    // }
    // if (document.getElementById('diluyenteRequerido')) {
    //     document.getElementById('diluyenteRequerido').addEventListener('click', () => load_data('diluyenteRequerido'));
    // }
    // if (document.getElementById('limiteRestriccion')) {
    //     document.getElementById('limiteRestriccion').addEventListener('click', () => load_data('limiteRestriccion'));
    // }
    // if (document.getElementById('viscosidadBSW')) {
    //     document.getElementById('viscosidadBSW').addEventListener('click', () => load_data('viscosidadBSW'));
    // }

    // grafica default
    if (document.getElementById('id_apiMezclaHumedo')) {
        load_data('relacionDiluyente');
        const selectElement = document.querySelector('#selectCalculos');

        selectElement.addEventListener('change', (event) => {
            load_data(`${event.target.value}`);
        });
    }

});

function load_data(graphId) {
    const pozo = document.querySelector('#id_pozo').value;
    const aceite = document.querySelector('#id_aceite').value;
    const apiCabeza = document.querySelector('#id_apiCabeza').value;
    const apiDiluyente = document.querySelector('#id_apiDiluyente').value;
    var apiMezclaHumedo = 0
    apiMezclaHumedo = parseFloat(document.getElementById('id_apiMezclaHumedo').innerHTML);
    const idContenedor = document.querySelector('#chartCalculos').id;
    url = `/graficarCalculos/${graphId}`;
    bodyJson = JSON.stringify({
        pozo: pozo,
        aceite: aceite,
        apiCabeza: apiCabeza,
        apiDiluyente: apiDiluyente,
        apiMezclaHumedo: apiMezclaHumedo,
        idContenedor: idContenedor
    });
    enviarAJAX(url, bodyJson);

}