document.addEventListener("DOMContentLoaded", function () {
    const formsEliminar = document.querySelectorAll(".form-eliminar");

    formsEliminar.forEach(function (formulario) {
        formulario.addEventListener("submit", function (evento) {
            const confirmar = confirm("¿Está seguro de que desea eliminar esta idea?");
            if (!confirmar) {
                evento.preventDefault();
            }
        });
    });
});
