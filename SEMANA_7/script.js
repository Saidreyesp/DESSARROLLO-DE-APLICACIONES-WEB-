// Arreglo inicial de productos
const productos = [
    {
        nombre: "Laptop HP Pavilion",
        precio: 899.99,
        descripcion: "Laptop de alto rendimiento con procesador Intel Core i7, 16GB RAM y SSD de 512GB."
    },
    {
        nombre: "Mouse Inalámbrico Logitech",
        precio: 29.99,
        descripcion: "Mouse ergonómico inalámbrico con tecnología Bluetooth y batería de larga duración."
    },
    {
        nombre: "Teclado Mecánico RGB",
        precio: 79.99,
        descripcion: "Teclado mecánico con switches blue, retroiluminación RGB personalizable."
    },
    {
        nombre: "Monitor 27 pulgadas",
        precio: 249.99,
        descripcion: "Monitor Full HD de 27 pulgadas con panel IPS y frecuencia de 75Hz."
    }
];

// Función para renderizar la lista de productos
function renderizarProductos() {
    const lista = document.getElementById('listaProductos');
    lista.innerHTML = '';

    productos.forEach((producto) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            Precio: $${producto.precio.toFixed(2)}<br>
            ${producto.descripcion}
        `;
        lista.appendChild(li);
    });
}

// Función para agregar un nuevo producto
function agregarProducto() {
    const nombresEjemplo = [
        "Auriculares Bluetooth",
        "Webcam HD 1080p",
        "Disco Duro Externo 1TB",
        "Hub USB-C",
        "Alfombrilla Gaming"
    ];

    const descripciones = [
        "Producto de alta calidad con excelentes características.",
        "Diseño moderno y funcional para uso diario.",
        "Tecnología avanzada que mejora tu productividad.",
        "Compatible con múltiples dispositivos.",
        "Excelente relación calidad-precio."
    ];

    const nombre = nombresEjemplo[Math.floor(Math.random() * nombresEjemplo.length)];
    const precio = (Math.random() * 200 + 10).toFixed(2);
    const descripcion = descripciones[Math.floor(Math.random() * descripciones.length)];

    const nuevoProducto = {
        nombre: nombre,
        precio: parseFloat(precio),
        descripcion: descripcion
    };

    productos.push(nuevoProducto);
    renderizarProductos();
}

// Event listener para el botón
document.getElementById('btnAgregar').addEventListener('click', agregarProducto);

// Renderizar productos al cargar la página
renderizarProductos();