document.addEventListener('DOMContentLoaded', function () {
  // alert('funciona');
  document.querySelector('#id_tipoCalculo_0').addEventListener('click', () => showLabel('Diluyente a inyectar BPD'));// Calcular API
  document.querySelector('#id_tipoCalculo_1').addEventListener('click', () => showLabel('API Seco @ 60ºF'));//Calcular Diluyente

});

function showLabel(text) {
  // alert('funciona');
  document.querySelector('label[for="id_variableACalcular"]').innerText = text;
  document.querySelector('#id_variableACalcular').value='';
}