var seriesId;
const seriesActivas = new Set();

document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'checkSeriesData') {
        seriesId.forEach(recorrerSeriesActivas);
        // console.log('en click');
        // console.log(seriesActivas);
        // console.log(seriesActivas.size);
        // grafica default
        if (seriesActivas.size > 0) {
            load_data('historial');
        }
    }
})



document.addEventListener('DOMContentLoaded', function () {
    seriesId = document.querySelectorAll('input.checkSeriesData')
    // seriesId.forEach(id=>{
    //     alert(id.id;
    // });
    seriesId.forEach(recorrerSeriesActivas);
    // console.log('inicio');
    // console.log(seriesActivas);

});

function recorrerSeriesActivas(serie) {
    if (serie.checked == true) {
        seriesActivas.add(serie.id);
    } else if (seriesActivas.has(serie.id)) {
        seriesActivas.delete(serie.id);
    }
}

function load_data(graphId) {
    const pozo = document.querySelector('#id_pozo').value;
    const series=Array.from(seriesActivas);
    const idContenedor=document.querySelector('#chartDataHistorica').id;
    url = `/graficarDataHistorica/${graphId}`;
    bodyJson = JSON.stringify({
        pozo: pozo,
        series:series,
        idContenedor:idContenedor
    });
    // console.log('json enviado');
    // console.log(bodyJson);
    enviarAJAX(url, bodyJson);

}