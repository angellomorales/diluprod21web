var seriesId;
const seriesActivas = new Set();

document.addEventListener('click', event => {
    const element = event.target;
    if ((element.className === 'form-check-input') || (element.id == "selectTipoMuestra")) {
        seriesActivas.clear();
        seriesId.forEach(recorrerSeriesActivas);
        // console.log(seriesActivas);
        // console.log(seriesActivas.size);
        document.querySelector('#id_separador_grafica').innerHTML = '<h3 class="section-title">Gráfica</h3>';
        if (seriesActivas.size > 0) {
            load_data_Graficas('historial');
        }
        else {
            document.querySelector('#chartDataHistorica').innerHTML = "";
        }
    }
})

document.addEventListener('DOMContentLoaded', function () {
    const selectPozo = document.querySelector('#id_pozo');
    selectPozo.addEventListener('change', (event) => {
        load_predata_Laboratorio(`${event.target.value}`);
    });

    // datos x default
    if (selectPozo.value != "") {
        load_predata_Laboratorio(selectPozo.value);
    }

});

function load_data_Graficas(graphId) {
    const pozo = document.querySelector('#id_pozo').value;
    const series = Array.from(seriesActivas);
    const tipo = document.querySelector('#selectTipoMuestra').value;
    const idContenedor = document.querySelector('#chartDataHistorica').id;
    url = `/graficarTablaLaboratorio/${graphId}`;
    bodyJson = JSON.stringify({
        pozo: pozo,
        series,
        tipo: tipo,
        idContenedor: idContenedor
    });
    // console.log('json enviado');
    // console.log(bodyJson);
    enviarAJAX(url, bodyJson);

}

function recorrerSeriesActivas(serie) {
    if (serie.checked == true) {
        seriesActivas.add({
            'id': serie.id,
            'label': document.querySelector(`#${serie.id}_label`).value,
            'color': document.querySelector(`#${serie.id}_color`).value,
            'unidades': document.querySelector(`#${serie.id}_unidades`).value
        });

    }
}

function load_predata_Laboratorio(PozoId) {
    if (PozoId != "") {
        url = `/cargarTablaLaboratorio/${PozoId}`;
        enviarAJAX(url, "");
    }
}

function cargarPredata(dataResponse) {
    if (!dataResponse.datos.length) {
        console.log('no existe');
        document.querySelector('#id_tabla_historico_Lab').innerHTML = '';
        document.querySelector('#chartDataHistorica').innerHTML = "";
    }
    else {

        let values = valuesTableHTML(dataResponse);
        let innerHTML = '<hr class="my-4">' +
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
        seriesId = document.querySelectorAll('input.form-check-input');//para seleccionar el id de todas las series dsps de cargar la pag
    };

    function valuesTableHTML(dataResponse) {
        let header = "";
        let innerContent = "";
        let content = "";

        // console.log(dataResponse);
        dataResponse.datos.forEach(foreachElement);

        function foreachElement(element, index, array) {
            // console.log(element);
            // console.log(index);
            // console.log(arr);

            for (var field in element) {
                // console.log(field);
                // console.log(element[field].id);
                if (index === 0) {
                    header += `<th class="cell"><span>${field}</span><span class="note">`;
                    if ('color' in element[field]) {
                        header += '<div class="form-check form-switch mb-3">' +
                            `<input class="form-check-input" type="checkbox" id="${element[field].id}">` +
                            `<label class="form-check-label" for="${element[field].id}">` +
                            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up" viewBox="0 0 16 16">' +
                            '<path fill-rule="evenodd" d="M0 0h1v15h15v1H0V0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V4.9l-3.613 4.417a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61L13.445 4H10.5a.5.5 0 0 1-.5-.5z" />' +
                            '</svg>' +
                            '</label>' +
                            `<input type="hidden" id="${element[field].id}_label" value="${field}">` +
                            `<input type="hidden" id="${element[field].id}_color" value="${element[field].color}">` +
                            `<input type="hidden" id="${element[field].id}_unidades" value="${element[field].unidades}"></input>` +
                            '</div>';
                    };
                    if ('dropdown' in element[field]) {
                        header += '<select class="form-select form-select-sm ms-auto d-inline-flex w-auto" id="selectTipoMuestra">';
                        element[field].dropdown.forEach(element => {
                            header += `<option value="${element}">${element}</option>`;
                        });
                        header += '</select>';
                    };
                    header += '</span></th>';
                }
                innerContent += `<td class="cell">${element[field].valor}</td>`;
            }
            content += '<tr>' + innerContent + '</tr>';
            innerContent = "";
        }
        return { header: header, content: content };

    };

}