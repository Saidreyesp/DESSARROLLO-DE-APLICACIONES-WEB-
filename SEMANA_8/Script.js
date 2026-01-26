// PROYECTO: Mi Tienda Online - JavaScript

function mostrarAlerta() {
    alert("Gracias por tu interes! Pronto tendremos mas novedades.");
}

document.addEventListener('DOMContentLoaded', function() {
    
    const formulario = document.getElementById('formularioContacto');
    
    formulario.addEventListener('submit', function(evento) {
        evento.preventDefault();
        
        const nombre = document.getElementById('nombre').value;
        const email = document.getElementById('email').value;
        const mensaje = document.getElementById('mensaje').value;
        
        let formularioValido = true;
        
        if (nombre.trim() === '') {
            marcarCampoInvalido('nombre', 'Por favor ingresa tu nombre');
            formularioValido = false;
        } else if (nombre.trim().length < 3) {
            marcarCampoInvalido('nombre', 'El nombre debe tener al menos 3 caracteres');
            formularioValido = false;
        } else {
            marcarCampoValido('nombre');
        }
        
        if (email.trim() === '') {
            marcarCampoInvalido('email', 'Por favor ingresa tu correo electronico');
            formularioValido = false;
        } else if (!validarEmail(email)) {
            marcarCampoInvalido('email', 'Por favor ingresa un correo valido');
            formularioValido = false;
        } else {
            marcarCampoValido('email');
        }
        
        if (mensaje.trim() === '') {
            marcarCampoInvalido('mensaje', 'Por favor escribe tu mensaje');
            formularioValido = false;
        } else if (mensaje.trim().length < 10) {
            marcarCampoInvalido('mensaje', 'El mensaje debe tener al menos 10 caracteres');
            formularioValido = false;
        } else {
            marcarCampoValido('mensaje');
        }
        
        if (formularioValido) {
            alert('Mensaje enviado con exito!\n\nNombre: ' + nombre + '\nEmail: ' + email + '\nMensaje: ' + mensaje);
            
            formulario.reset();
            
            document.getElementById('nombre').classList.remove('is-valid', 'is-invalid');
            document.getElementById('email').classList.remove('is-valid', 'is-invalid');
            document.getElementById('mensaje').classList.remove('is-valid', 'is-invalid');
            
            console.log('Formulario enviado correctamente');
            console.log('Nombre:', nombre);
            console.log('Email:', email);
            console.log('Mensaje:', mensaje);
        } else {
            alert('Por favor corrige los errores en el formulario');
        }
    });
    
    document.getElementById('nombre').addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            validarCampoNombre();
        }
    });
    
    document.getElementById('email').addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            validarCampoEmail();
        }
    });
    
    document.getElementById('mensaje').addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
            validarCampoMensaje();
        }
    });
});

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function marcarCampoInvalido(campoId, mensajeError) {
    const campo = document.getElementById(campoId);
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    const feedbackDiv = campo.nextElementSibling;
    if (feedbackDiv && feedbackDiv.classList.contains('invalid-feedback')) {
        feedbackDiv.textContent = mensajeError;
    }
}

function marcarCampoValido(campoId) {
    const campo = document.getElementById(campoId);
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
}

function validarCampoNombre() {
    const nombre = document.getElementById('nombre').value;
    if (nombre.trim() === '') {
        marcarCampoInvalido('nombre', 'Por favor ingresa tu nombre');
        return false;
    } else if (nombre.trim().length < 3) {
        marcarCampoInvalido('nombre', 'El nombre debe tener al menos 3 caracteres');
        return false;
    } else {
        marcarCampoValido('nombre');
        return true;
    }
}

function validarCampoEmail() {
    const email = document.getElementById('email').value;
    if (email.trim() === '') {
        marcarCampoInvalido('email', 'Por favor ingresa tu correo electronico');
        return false;
    } else if (!validarEmail(email)) {
        marcarCampoInvalido('email', 'Por favor ingresa un correo valido');
        return false;
    } else {
        marcarCampoValido('email');
        return true;
    }
}

function validarCampoMensaje() {
    const mensaje = document.getElementById('mensaje').value;
    if (mensaje.trim() === '') {
        marcarCampoInvalido('mensaje', 'Por favor escribe tu mensaje');
        return false;
    } else if (mensaje.trim().length < 10) {
        marcarCampoInvalido('mensaje', 'El mensaje debe tener al menos 10 caracteres');
        return false;
    } else {
        marcarCampoValido('mensaje');
        return true;
    }
}

console.log('Pagina cargada correctamente');
console.log('Proyecto: Mi Tienda Online con Bootstrap y JavaScript');