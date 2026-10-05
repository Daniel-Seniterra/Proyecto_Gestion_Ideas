CREATE TABLE IF NOT EXISTS usuarios (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    rol VARCHAR(30) NOT NULL DEFAULT 'usuario'
);

CREATE TABLE IF NOT EXISTS productos (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(80) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    usuario_id VARCHAR(36) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_producto_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clientes (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    empresa VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL,
    telefono VARCHAR(30) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proveedores (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    servicio VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL,
    telefono VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS facturacion (
    id VARCHAR(36) PRIMARY KEY,
    cliente_id VARCHAR(36) NOT NULL,
    concepto VARCHAR(200) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
);