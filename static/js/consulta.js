document.getElementById("consulta-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const ruc = document.getElementById("ruc").value.trim();  // Eliminar espacios innecesarios
    const token = localStorage.getItem("token");

    if (!ruc || !token) {
        document.getElementById("consulta-error").textContent = "Por favor, ingrese un RUC y asegúrese de haber iniciado sesión.";
        return;
    }

    fetch("/ruc-info", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"  // Asegúrate de enviar como JSON
        },
        body: JSON.stringify({ ruc: ruc })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("consulta-error").textContent = data.error;
        } else {
            window.location.href = `/ruc-info?ruc=${data.RUC}`;  // Redirigir a la página de ruc-info
        }
    })
    .catch(error => {
        document.getElementById("consulta-error").textContent = "Error al conectar con el servidor.";
    });
});
