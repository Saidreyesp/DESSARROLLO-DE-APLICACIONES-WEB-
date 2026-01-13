// Obtener elementos del DOM
const form = document.getElementById('registroForm');
const btnEnviar = document.getElementById('btnEnviar');
const btnReiniciar = document.getElementById('btnReiniciar');
const successMessage = document.getElementById('successMessage');

// Obtener campos del formulario
const nombre = document.getElementById('nombre');
const email = document.getElementById('email');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');
const edad = document.getElementById('edad');

// Obtener elementos de error
const errorNombre = document.getElementById('errorNombre');
const errorEmail = document.getElementById('errorEmail');
const errorPassword = document.getElementById('errorPassword');
const errorConfirmPassword = document.getElementById('errorConfirmPassword');
const errorEdad = document.getElementById('errorEdad');

// Estado de validación de cada campo
const validacionEstado = {
    nombre: false,
    email: false,
    password: false,
    confirmPassword: false,
    edad: false
};

// Expresiones regulares para validación
const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const regexPassword = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;

// Función para validar el nombre
function validarNombre() {
    const valor = nombre.value.trim();
    
    if (valor === '') {
        mostrarError(nombre, errorNombre, 'El nombre es obligatorio');
        validacionEstado.nombre = false;
    } else if (valor.length < 3) {
        mostrarError(nombre, errorNombre, 'El nombre debe tener al menos 3 caracteres');
        validacionEstado.nombre = false;
    } else {
        mostrarExito(nombre, errorNombre);
        validacionEstado.nombre = true;
    }
    
    verificarFormularioCompleto();
}

// Función para validar el email
function validarEmail() {
    const valor = email.value.trim();
    
    if (valor === '') {
        mostrarError(email, errorEmail, 'El correo electrónico es obligatorio');
        validacionEstado.email = false;
    } else if (!regexEmail.test(valor)) {
        mostrarError(email, errorEmail, 'Ingrese un correo electrónico válido');
        validacionEstado.email = false;
    } else {
        mostrarExito(email, errorEmail);
        validacionEstado.email = true;
    }
    
    verificarFormularioCompleto();
}

// Función para validar la contraseña
function validarPassword() {
    const valor = password.value;
    
    if (valor === '') {
        mostrarError(password, errorPassword, 'La contraseña es obligatoria');
        validacionEstado.password = false;
    } else if (valor.length < 8) {
        mostrarError(password, errorPassword, 'La contraseña debe tener al menos 8 caracteres');
        validacionEstado.password = false;
    } else if (!regexPassword.test(valor)) {
        mostrarError(password, errorPassword, 'Debe incluir al menos un número y un carácter especial (!@#$%^&*)');
        validacionEstado.password = false;
    } else {
        mostrarExito(password, errorPassword);
        validacionEstado.password = true;
    }
    
    // Revalidar confirmación de contraseña si ya tiene contenido
    if (confirmPassword.value !== '') {
        validarConfirmPassword();
    }
    
    verificarFormularioCompleto();
}

// Función para validar la confirmación de contraseña
function validarConfirmPassword() {
    const valor = confirmPassword.value;
    const valorPassword = password.value;
    
    if (valor === '') {
        mostrarError(confirmPassword, errorConfirmPassword, 'Debe confirmar su contraseña');
        validacionEstado.confirmPassword = false;
    } else if (valor !== valorPassword) {
        mostrarError(confirmPassword, errorConfirmPassword, 'Las contraseñas no coinciden');
        validacionEstado.confirmPassword = false;
    } else {
        mostrarExito(confirmPassword, errorConfirmPassword);
        validacionEstado.confirmPassword = true;
    }
    
    verificarFormularioCompleto();
}

// Función para validar la edad
function validarEdad() {
    const valor = edad.value;
    const edadNum = parseInt(valor);
    
    if (valor === '') {
        mostrarError(edad, errorEdad, 'La edad es obligatoria');
        validacionEstado.edad = false;
    } else if (isNaN(edadNum)) {
        mostrarError(edad, errorEdad, 'Ingrese un número válido');
        validacionEstado.edad = false;
    } else if (edadNum < 18) {
        mostrarError(edad, errorEdad, 'Debe ser mayor de 18 años');
        validacionEstado.edad = false;
    } else if (edadNum > 120) {
        mostrarError(edad, errorEdad, 'Ingrese una edad válida');
        validacionEstado.edad = false;
    } else {
        mostrarExito(edad, errorEdad);
        validacionEstado.edad = true;
    }
    
    verificarFormularioCompleto();
}

// Función para mostrar error
function mostrarError(input, errorElement, mensaje) {
    input.classList.remove('valid');
    input.classList.add('invalid');
    errorElement.textContent = mensaje;
}

// Función para mostrar éxito
function mostrarExito(input, errorElement) {
    input.classList.remove('invalid');
    input.classList.add('valid');
    errorElement.textContent = '';
}

// Función para verificar si el formulario está completo y válido
function verificarFormularioCompleto() {
    const todoValido = Object.values(validacionEstado).every(estado => estado === true);
    
    if (todoValido) {
        btnEnviar.disabled = false;
    } else {
        btnEnviar.disabled = true;
    }
}

// Event listeners para validación en tiempo real
nombre.addEventListener('input', validarNombre);
nombre.addEventListener('blur', validarNombre);

email.addEventListener('input', validarEmail);
email.addEventListener('blur', validarEmail);

password.addEventListener('input', validarPassword);
password.addEventListener('blur', validarPassword);

confirmPassword.addEventListener('input', validarConfirmPassword);
confirmPassword.addEventListener('blur', validarConfirmPassword);

edad.addEventListener('input', validarEdad);
edad.addEventListener('blur', validarEdad);

// Manejador del envío del formulario
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validar todos los campos nuevamente
    validarNombre();
    validarEmail();
    validarPassword();
    validarConfirmPassword();
    validarEdad();
    
    // Verificar si todos son válidos
    const todoValido = Object.values(validacionEstado).every(estado => estado === true);
    
    if (todoValido) {
        // Mostrar mensaje de éxito
        successMessage.classList.add('show');
        
        // Ocultar el formulario temporalmente
        form.style.opacity = '0.5';
        btnEnviar.disabled = true;
        btnReiniciar.disabled = true;
        
        // Simular envío y resetear después de 3 segundos
        setTimeout(() => {
            successMessage.classList.remove('show');
            form.style.opacity = '1';
            btnReiniciar.disabled = false;
        }, 3000);
        
        // Log de datos (en producción aquí se enviarían al servidor)
        console.log('Formulario enviado con éxito:');
        console.log({
            nombre: nombre.value,
            email: email.value,
            edad: edad.value
        });
    }
});

// Manejador del botón reiniciar
btnReiniciar.addEventListener('click', function() {
    // Resetear el formulario
    form.reset();
    
    // Remover clases de validación
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('valid', 'invalid');
    });
    
    // Limpiar mensajes de error
    document.querySelectorAll('.error-message').forEach(error => {
        error.textContent = '';
    });
    
    // Resetear estado de validación
    Object.keys(validacionEstado).forEach(key => {
        validacionEstado[key] = false;
    });
    
    // Deshabilitar botón de envío
    btnEnviar.disabled = true;
    
    // Ocultar mensaje de éxito si está visible
    successMessage.classList.remove('show');
    
    // Enfocar el primer campo
    nombre.focus();
});