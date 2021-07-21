var seriesId;
const seriesActivas = new Set();

document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'checkSeriesData') {
        seriesActivas.clear();
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
    // let serieparameters = {};//opcion para crear un json
    if (serie.checked == true) {

        //opcion para crear un json
        // Object.defineProperty(serieparameters, 'id', {
        //     value: serie.id,
        // });

        // Object.defineProperty(serieparameters, 'color', {
        //     value: document.querySelector(`#${serie.id}_color`).value,
        // });
        // Object.defineProperty(serieparameters, 'unidades', {
        //     value: document.querySelector(`#${serie.id}_unidades`).value,
        // });

        seriesActivas.add(serie.id);

    }
}

function load_data(graphId) {
    const pozo = document.querySelector('#id_pozo').value;
    const series=Array.from(seriesActivas);
    // let mapIdSeries = series.map((serie) => serie.id);//opcion para crear un json
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