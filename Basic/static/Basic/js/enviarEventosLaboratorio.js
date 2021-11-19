document.addEventListener('DOMContentLoaded', function () {
    // listeners para obtener los datos de la grafica
    // if (document.getElementById('relacionDiluyente')) {
    //     document.getElementById('relacionDiluyente').addEventListener('click', () =>load_data_Graficas('relacionDiluyente'));
    // }
    const selectPozo = document.querySelector('#id_pozo');
    selectPozo.addEventListener('change', (event) => {
        load_predata_Calculos(`${event.target.value}`);
    });

    // grafica default
    // if (document.getElementById('id_apiMezclaHumedo')) {
    //     load_data_Graficas('relacionDiluyente');
    //     const selectElement = document.querySelector('#selectCalculos');

    //     selectElement.addEventListener('change', (event) => {
    //         load_data_Graficas(`${event.target.value}`);
    //     });
    // }

});

// function load_data_Graficas(graphId) {
//     const aceite = document.querySelector('#id_aceite').value;
//     const apiCabeza = document.querySelector('#id_apiCabeza').value;
//     const apiDiluyente = document.querySelector('#id_apiDiluyente').value;
//     var apiMezclaHumedo = 0
//     apiMezclaHumedo = parseFloat(document.getElementById('id_apiMezclaHumedo').innerHTML);
//     const idContenedor = document.querySelector('#chartCalculos').id;
//     url = `/graficarCalculos/${graphId}`;
//     bodyJson = JSON.stringify({
//         aceite: aceite,
//         apiCabeza: apiCabeza,
//         apiDiluyente: apiDiluyente,
//         apiMezclaHumedo: apiMezclaHumedo,
//         idContenedor: idContenedor
//     });
//     enviarAJAX(url, bodyJson);

// }

function load_predata_Calculos(PozoId) {
    url = `/cargarTablaLaboratorio/${PozoId}`;
    enviarAJAX(url, "");
}

function cargarPredata(dataResponse) {
    if (!dataResponse.datos.length) {
        console.log('no existe');
        document.querySelector('#id_tabla_historico_Lab').innerHTML = '';
    }
    else {

        var values = valuesTableHTML(dataResponse);
        var innerHTML = '<hr class="my-4">' +
            '<div class="row g-4 settings-section mb-4">' +
            '<h3 class="section-title">Histórico</h3>' +
            '</div>' +
            '<div class="tab-content" id="orders-table-tab-content">' +
            '<div class="tab-pane fade active show" id="orders-all" role="tabpanel" aria-labelledby="orders-all-tab">' +
            '<div class="app-card app-card-orders-table shadow-sm mb-5">' +
            '<div class="app-card-body">' +
            '<div class="table-responsive tab-scrolling">' +
            '<table class="table app-table-hover mb-0 text-left">' +
            '<thead>' +
            '<tr>' +
            values.header +
            '</tr>' +
            '</thead>' +
            '<tbody>' +
            values.content +
            '</tbody>' +
            '</table>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>';

        document.querySelector('#id_tabla_historico_Lab').innerHTML = innerHTML;
    };

    function valuesTableHTML(dataResponse) {
        var header = "";
        var innerContent = "";
        var content = "";

        console.log(dataResponse);
        dataResponse.datos.forEach(foreachElement);

        function foreachElement(element, index, array) {
            console.log(element);
            // console.log(index);
            // console.log(arr);

            for (var field in element) {
                // console.log(field);
                // console.log(element[field].id);
                if (index === 0) {
                    header += `<th class="cell"><span>${field}</span><span class="note">` +
                        '<div class="form-check form-switch mb-3">' +
                        `<input class="form-check-input" type="checkbox" id="${element[field].id}">` +
                        `<label class="form-check-label" for="${element[field].id}">` +
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up" viewBox="0 0 16 16">' +
                        '<path fill-rule="evenodd" d="M0 0h1v15h15v1H0V0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V4.9l-3.613 4.417a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61L13.445 4H10.5a.5.5 0 0 1-.5-.5z" />' +
                        '</svg>' +
                        '</label>' +
                        '</div>' +
                        '</span></th>';
                }
                innerContent += `<td class="cell">${element[field].valor}</td>`;
            }
            content += '<tr>' + innerContent + '</tr>';
            innerContent = "";
        }
        return { header: header, content: content };

    };

}