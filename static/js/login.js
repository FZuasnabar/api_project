document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Previene que se recargue la página y que el formulario se envíe como GET

    const user_ruc = document.getElementById("user_ruc").value;
    const password = document.getElementById("password").value;

    // Usamos fetch para enviar la solicitud POST
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: user_ruc, password: password })  // Enviamos las credenciales como JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // Si recibimos el token, lo guardamos en localStorage y redirigimos a /consulta
            localStorage.setItem("token", data.token);
            window.location.href = "/consulta"; // Redirigir a /consulta
        } else {
            // Si hay un error, mostramos el mensaje
            document.getElementById("login-error").textContent = data.error || "Error desconocido.";
        }
    })
    .catch(error => {
        // Si hay un error en la conexión, mostramos el mensaje
        document.getElementById("login-error").textContent = "Error al conectar con el servidor.";
    });
});
