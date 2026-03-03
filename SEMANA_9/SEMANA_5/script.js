// Selección de elementos del DOM
const imageUrlInput = document.getElementById('imageUrl');
const addImageBtn = document.getElementById('addImageBtn');
const deleteImageBtn = document.getElementById('deleteImageBtn');
const gallery = document.getElementById('gallery');
const infoMessage = document.getElementById('infoMessage');

// Variable para almacenar la imagen seleccionada
let selectedImage = null;

// Imágenes por defecto para inicializar la galería
const defaultImages = [
    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500',
    'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=500',
    'https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=500'
];

// Función para agregar una imagen a la galería
function addImageToGallery(url) {
    // Crear el contenedor de la imagen
    const galleryItem = document.createElement('div');
    galleryItem.className = 'gallery-item';

    // Crear el elemento de imagen
    const img = document.createElement('img');
    img.src = url;
    img.alt = 'Imagen de galería';

    // Manejar error de carga de imagen
    img.onerror = function() {
        alert('Error al cargar la imagen. Verifica la URL.');
        galleryItem.remove();
        updateInfoMessage();
    };

    // Agregar evento de clic para seleccionar la imagen
    galleryItem.addEventListener('click', function() {
        selectImage(galleryItem);
    });

    // Agregar la imagen al contenedor
    galleryItem.appendChild(img);

    // Agregar el contenedor a la galería
    gallery.appendChild(galleryItem);

    // Actualizar mensaje informativo
    updateInfoMessage();
}

// Función para seleccionar una imagen
function selectImage(imageElement) {
    // Si hay una imagen seleccionada previamente, deseleccionarla
    if (selectedImage) {
        selectedImage.classList.remove('selected');
    }

    // Seleccionar la nueva imagen
    selectedImage = imageElement;
    selectedImage.classList.add('selected');

    // Habilitar el botón de eliminar
    deleteImageBtn.disabled = false;
}

// Función para eliminar la imagen seleccionada
function deleteSelectedImage() {
    if (selectedImage) {
        // Agregar clase de animación de eliminación
        selectedImage.classList.add('removing');

        // Esperar a que termine la animación antes de eliminar
        setTimeout(function() {
            selectedImage.remove();
            selectedImage = null;
            
            // Deshabilitar el botón de eliminar
            deleteImageBtn.disabled = true;
            
            // Actualizar mensaje informativo
            updateInfoMessage();
        }, 400);
    }
}

// Función para actualizar el mensaje informativo
function updateInfoMessage() {
    const imageCount = gallery.children.length;
    
    if (imageCount === 0) {
        infoMessage.innerHTML = '<p>Ingresa una URL de imagen y haz clic en Agregar Imagen para comenzar</p>';
        infoMessage.style.display = 'block';
    } else {
        if (imageCount === 1) {
            infoMessage.innerHTML = '<p>Tienes 1 imagen en la galería</p>';
        } else {
            infoMessage.innerHTML = '<p>Tienes ' + imageCount + ' imágenes en la galería</p>';
        }
    }
}

// Función para validar URL de imagen
function isValidImageUrl(url) {
    if (url.indexOf('http://') === 0 || url.indexOf('https://') === 0) {
        return true;
    }
    return false;
}

// Evento: Agregar imagen al hacer clic en el botón
addImageBtn.addEventListener('click', function() {
    const url = imageUrlInput.value.trim();

    if (url === '') {
        alert('Por favor, ingresa una URL de imagen.');
        return;
    }

    if (!isValidImageUrl(url)) {
        alert('Por favor, ingresa una URL válida (debe comenzar con http:// o https://).');
        return;
    }

    // Agregar la imagen a la galería
    addImageToGallery(url);

    // Limpiar el campo de entrada
    imageUrlInput.value = '';
    imageUrlInput.focus();
});

// Evento: Agregar imagen al presionar Enter en el campo de entrada
imageUrlInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        addImageBtn.click();
    }
});

// Evento: Eliminar imagen seleccionada
deleteImageBtn.addEventListener('click', deleteSelectedImage);

// Evento: Eliminar imagen con la tecla Delete o Backspace
document.addEventListener('keydown', function(event) {
    if ((event.key === 'Delete' || event.key === 'Backspace') && selectedImage) {
        event.preventDefault();
        deleteSelectedImage();
    }
});

// Inicializar la galería al cargar la página
window.addEventListener('load', function() {
    // Agregar imágenes por defecto
    for (let i = 0; i < defaultImages.length; i++) {
        addImageToGallery(defaultImages[i]);
    }
    updateInfoMessage();
});