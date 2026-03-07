-- =====================================================
-- ENTREGA SEMANA MYSQL - COMEDOR ALEXANDRA
-- Proyecto Flask integrado con MySQL
-- =====================================================

-- 1) CREACION DE BASE DE DATOS
CREATE DATABASE IF NOT EXISTS comedor_alexandra
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE comedor_alexandra;

-- 2) CREACION DE TABLAS
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  mail VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS productos_mysql (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  categoria VARCHAR(80),
  cantidad INT NOT NULL DEFAULT 0,
  precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS reservas_mysql (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  cliente VARCHAR(120) NOT NULL,
  telefono VARCHAR(30),
  personas INT NOT NULL DEFAULT 1,
  fecha_reserva DATETIME,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3) DATOS INICIALES DE PRUEBA
INSERT INTO usuarios (nombre, mail, password)
VALUES
  ('Administrador', 'admin@comedoralexandra.com', 'admin123'),
  ('Alexandra Pianda', 'alexandra@comedoralexandra.com', 'clave_segura')
ON DUPLICATE KEY UPDATE
  nombre = VALUES(nombre),
  password = VALUES(password);

INSERT INTO productos_mysql (nombre, categoria, cantidad, precio)
VALUES
  ('Encebollado', 'Pescados', 15, 6.75),
  ('Seco de Gallina', 'Tradicional', 14, 8.75),
  ('Gaseosa', 'Bebidas', 30, 1.50),
  ('Jugo de Tamarindo', 'Bebidas', 15, 2.00)
ON DUPLICATE KEY UPDATE
  categoria = VALUES(categoria),
  cantidad = VALUES(cantidad),
  precio = VALUES(precio);

INSERT INTO reservas_mysql (cliente, telefono, personas, fecha_reserva)
VALUES
  ('Cliente Demo', '0999999999', 4, '2026-03-15 20:30:00'),
  ('Reserva Web', '0988888888', 2, '2026-03-16 22:00:00');

-- =====================================================
-- 4) CONSULTAS CRUD BASICAS (EJEMPLOS)
-- =====================================================

-- -------------------------
-- TABLA: usuarios
-- -------------------------

-- INSERTAR
INSERT INTO usuarios (nombre, mail, password)
VALUES ('Usuario Prueba', 'prueba@correo.com', '123456');

-- CONSULTAR
SELECT * FROM usuarios ORDER BY id_usuario DESC;

-- ACTUALIZAR
UPDATE usuarios
SET nombre = 'Usuario Editado', password = 'nueva_clave_789'
WHERE mail = 'prueba@correo.com';

-- ELIMINAR
DELETE FROM usuarios
WHERE mail = 'prueba@correo.com';

-- -------------------------
-- TABLA: productos_mysql
-- -------------------------

-- INSERTAR
INSERT INTO productos_mysql (nombre, categoria, cantidad, precio)
VALUES ('Botella de Agua', 'Bebidas', 40, 1.00);

-- CONSULTAR
SELECT * FROM productos_mysql ORDER BY id_producto DESC;

-- ACTUALIZAR
UPDATE productos_mysql
SET cantidad = 50, precio = 1.20
WHERE nombre = 'Botella de Agua';

-- ELIMINAR
DELETE FROM productos_mysql
WHERE nombre = 'Botella de Agua';

-- -------------------------
-- TABLA: reservas_mysql
-- -------------------------

-- INSERTAR
INSERT INTO reservas_mysql (cliente, telefono, personas, fecha_reserva)
VALUES ('Cliente SQL', '0977777777', 3, '2026-03-20 21:15:00');

-- CONSULTAR
SELECT * FROM reservas_mysql ORDER BY id_reserva DESC;

-- ACTUALIZAR
UPDATE reservas_mysql
SET personas = 5
WHERE cliente = 'Cliente SQL';

-- ELIMINAR
DELETE FROM reservas_mysql
WHERE cliente = 'Cliente SQL';

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
