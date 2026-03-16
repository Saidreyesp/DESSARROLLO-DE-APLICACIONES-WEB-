-- Esquema MySQL para COMEDOR ALEXANDRA
-- Semana de integracion Flask + MySQL

CREATE DATABASE IF NOT EXISTS comedor_alexandra
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE comedor_alexandra;

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
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

-- Datos iniciales opcionales
INSERT INTO usuarios (nombre, email, password)
SELECT 'Administrador', 'admin@comedoralexandra.com', 'admin123'
WHERE NOT EXISTS (
  SELECT 1 FROM usuarios WHERE email = 'admin@comedoralexandra.com'
);
