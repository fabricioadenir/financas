function mostrar_formulario(form_mostrar, form_esconder) {
    var div_mostrar = document.getElementById(form_mostrar);
    var div_esconder = document.getElementById(form_esconder);
    var botao = document.getElementById('btn-novo')

    if (div_mostrar.style.display == 'none') {
        botao.style.display = 'none';
        div_mostrar.style.display = 'block';
        div_esconder.style.display = 'none';
    } else {
        botao.style.display = '';
        div_mostrar.style.display = 'none';
        div_esconder.style.display = 'block';
    }
}