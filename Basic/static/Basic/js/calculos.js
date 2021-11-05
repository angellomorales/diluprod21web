document.addEventListener('DOMContentLoaded', function () {
  // alert('funciona');
  document.querySelector('#id_tipoCalculo_0').addEventListener('click', () => showLabel('Diluyente a inyectar BPD:', false));// Calcular API
  document.querySelector('#id_tipoCalculo_1').addEventListener('click', () => showLabel('API Seco @ 60ºF:', false));//Calcular Diluyente

});
window.addEventListener('load', function () {
  showResult();
});

function showLabel(text, isCalculado) {
  // alert('funciona');
  var getValue = document.querySelector('#id_variableACalcular').value;
  document.querySelector('label[for="id_variableACalcular"]').innerText = text;
  document.querySelector('#id_variableACalcular').value = isCalculado ? getValue : '';
}

function showResult() {
  var DiluyenteSelected = document.getElementById('id_tipoCalculo_0').checked;
  if (DiluyenteSelected) {
    showLabel('Diluyente a inyectar BPD:', true)
    document.querySelector('#id_tituloResultadoCalculo').innerText='API de Mezcla @ 60ºF';
    document.querySelector('#id_ContenidoResultadoDiluyente').style.display='none';
  } else {
    showLabel('API Seco @ 60ºF:', true)
    document.querySelector('#id_tituloResultadoCalculo').innerText='Diluyente Requerido BPD';
        document.querySelector('#id_ContenidoResultadoAPI').style.display='none';
  }
}