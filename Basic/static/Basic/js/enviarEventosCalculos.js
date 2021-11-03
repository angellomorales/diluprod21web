document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    // if (document.getElementById('relacionDiluyente')) {
    //     document.getElementById('relacionDiluyente').addEventListener('click', () => load_data_Graficas('relacionDiluyente'));
    // }
    const selectPozo = document.querySelector('#id_pozo');
    selectPozo.addEventListener('change', (event) => {
        load_predata_Calculos(`${event.target.value}`);
    });

    // grafica default
    if (document.getElementById('id_apiMezclaHumedo')) {
        load_data_Graficas('relacionDiluyente');
        const selectElement = document.querySelector('#selectCalculos');

        selectElement.addEventListener('change', (event) => {
            load_data_Graficas(`${event.target.value}`);
        });
    }

});

function load_data_Graficas(graphId) {
    const aceite = document.querySelector('#id_aceite').value;
    const apiCabeza = document.querySelector('#id_apiCabeza').value;
    const apiDiluyente = document.querySelector('#id_apiDiluyente').value;
    var apiMezclaHumedo = 0
    apiMezclaHumedo = parseFloat(document.getElementById('id_apiMezclaHumedo').innerHTML);
    const idContenedor = document.querySelector('#chartCalculos').id;
    url = `/graficarCalculos/${graphId}`;
    bodyJson = JSON.stringify({
        aceite: aceite,
        apiCabeza: apiCabeza,
        apiDiluyente: apiDiluyente,
        apiMezclaHumedo: apiMezclaHumedo,
        idContenedor: idContenedor
    });
    enviarAJAX(url, bodyJson);

}

function load_predata_Calculos(PozoId) {
    url = `/cargarPredataCalculos/${PozoId}`;
    enviarAJAX(url, "");
}

function cargarPredata(dataResponse) {
    // console.log(dataResponse);
    if (dataResponse.pozoId != null) {
        document.querySelector('#id_aceite').value = dataResponse.data.tablas[2].contenido[0].valor;
        document.querySelector('#id_swCabeza').value = dataResponse.data.tablas[3].contenido[0].valor;
        document.querySelector('#id_apiCabeza').value = dataResponse.data.tablas[3].contenido[1].valor;
    };

}