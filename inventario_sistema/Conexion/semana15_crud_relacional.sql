-- =====================================================
-- SEMANA 15 - SCRIPT SQL RELACIONAL
-- Proyecto: Inventario/Comedor Alexandra
-- =====================================================

CREATE DATABASE IF NOT EXISTS comedor_alexandra
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE comedor_alexandra;

-- Tabla principal de usuarios autenticados en Flask
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Entidad 1: productos
CREATE TABLE IF NOT EXISTS productos_mysql (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  categoria VARCHAR(80),
  cantidad INT NOT NULL DEFAULT 0,
  precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Entidad 2: clientes
CREATE TABLE IF NOT EXISTS clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  cedula VARCHAR(20) NOT NULL UNIQUE,
  nombres VARCHAR(120) NOT NULL,
  telefono VARCHAR(20),
  email VARCHAR(150),
  direccion VARCHAR(180)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Entidad 3: facturas (relacionada con clientes)
CREATE TABLE IF NOT EXISTS facturas (
  id_factura INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  iva DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  CONSTRAINT fk_facturas_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente)
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de detalle (relacionada con facturas y productos)
CREATE TABLE IF NOT EXISTS detalle_factura (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_factura INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  precio_unitario DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  CONSTRAINT fk_detalle_factura
    FOREIGN KEY (id_factura)
    REFERENCES facturas(id_factura)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_detalle_producto
    FOREIGN KEY (id_producto)
    REFERENCES productos_mysql(id_producto)
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DATOS DE PRUEBA
-- =====================================================

INSERT INTO productos_mysql (nombre, categoria, cantidad, precio) VALUES
('Encebollado', 'Pescados', 15, 6.75),
('Seco de Gallina', 'Tradicional', 14, 8.75),
('Gaseosa', 'Bebidas', 30, 1.50)
ON DUPLICATE KEY UPDATE
  categoria = VALUES(categoria),
  cantidad = VALUES(cantidad),
  precio = VALUES(precio);

INSERT INTO clientes (cedula, nombres, telefono, email, direccion) VALUES
('1101234567', 'Cliente Demo Uno', '0999999999', 'demo1@correo.com', 'Loja'),
('1109876543', 'Cliente Demo Dos', '0988888888', 'demo2@correo.com', 'Catamayo')
ON DUPLICATE KEY UPDATE
  nombres = VALUES(nombres),
  telefono = VALUES(telefono),
  email = VALUES(email),
  direccion = VALUES(direccion);

INSERT INTO facturas (id_cliente, subtotal, iva, total)
SELECT c.id_cliente, 10.00, 1.50, 11.50
FROM clientes c
WHERE c.cedula = '1101234567'
LIMIT 1;

INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario)
SELECT f.id_factura, p.id_producto, 1, p.precio
FROM facturas f
JOIN productos_mysql p ON p.nombre = 'Encebollado'
ORDER BY f.id_factura DESC
LIMIT 1;

-- =====================================================
-- CONSULTA DE VALIDACION DE RELACIONES
-- =====================================================
SELECT
  f.id_factura,
  c.nombres AS cliente,
  p.nombre AS producto,
  d.cantidad,
  d.precio_unitario
FROM detalle_factura d
JOIN facturas f ON f.id_factura = d.id_factura
JOIN clientes c ON c.id_cliente = f.id_cliente
JOIN productos_mysql p ON p.id_producto = d.id_producto
ORDER BY f.id_factura DESC;
