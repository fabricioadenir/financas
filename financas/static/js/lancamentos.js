function get_mes_lancamento_default() {
    data = new Date();
    alert(data.getMonth())
    document.getElementById("mes_calculo").setAttribute('value', data.getMonth());
}