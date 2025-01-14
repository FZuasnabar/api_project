document.addEventListener("DOMContentLoaded", function() {
    // Puedes añadir funcionalidades o interacciones aquí si es necesario
    // Ejemplo: Mostrar un mensaje o realizar una acción adicional cuando la página se carga

    const rucInfo = document.getElementById('ruc-info');
    if (rucInfo) {
        console.log("Información del RUC cargada correctamente.");
    }

    // Si deseas agregar algún comportamiento dinámico, como una acción de actualización o validación,
    // puedes hacerlo en este archivo JS.

    // Ejemplo de un botón de "volver" que redirige al usuario
    const backButton = document.querySelector(".back-btn");
    if (backButton) {
        backButton.addEventListener("click", function() {
            // Se puede agregar lógica para hacer algo antes de regresar, si es necesario
            console.log("Volver a la consulta...");
        });
    }
});
