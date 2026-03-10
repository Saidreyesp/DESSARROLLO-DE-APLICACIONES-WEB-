-- Consultas CRUD basicas para Semana MySQL
USE comedor_alexandra;

-- =========================
-- USUARIOS
-- =========================

-- INSERTAR
INSERT INTO usuarios (nombre, mail, password)
VALUES ('Alexandra', 'alexandra@comedor.com', 'clave123');

-- CONSULTAR
SELECT * FROM usuarios;

-- ACTUALIZAR
UPDATE usuarios
SET nombre = 'Alexandra Pianda', password = 'nueva_clave'
WHERE id_usuario = 1;

-- ELIMINAR
DELETE FROM usuarios
WHERE id_usuario = 1;


-- =========================
-- PRODUCTOS
-- =========================

-- INSERTAR
INSERT INTO productos_mysql (nombre, categoria, cantidad, precio)
VALUES ('Encebollado', 'Pescados', 15, 6.75);

-- CONSULTAR
SELECT * FROM productos_mysql;

-- ACTUALIZAR
UPDATE productos_mysql
SET cantidad = 20, precio = 7.00
WHERE id_producto = 1;

-- ELIMINAR
DELETE FROM productos_mysql
WHERE id_producto = 1;


-- =========================
-- RESERVAS
-- =========================

-- INSERTAR
INSERT INTO reservas_mysql (cliente, telefono, personas, fecha_reserva)
VALUES ('Cliente Demo', '0999999999', 4, '2026-03-10 20:30:00');

-- CONSULTAR
SELECT * FROM reservas_mysql;

-- ACTUALIZAR
UPDATE reservas_mysql
SET personas = 5
WHERE id_reserva = 1;

-- ELIMINAR
DELETE FROM reservas_mysql
WHERE id_reserva = 1;
