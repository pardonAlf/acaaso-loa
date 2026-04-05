
-- =====================================
-- TABLAS UBIGEO PERÚ
-- =====================================

CREATE TABLE departamento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE provincia (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT REFERENCES departamento(id)
);

CREATE TABLE distrito (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT REFERENCES provincia(id)
);

-- =====================================
-- INSERTS DE EJEMPLO (PUEDES AMPLIAR)
-- =====================================

-- DEPARTAMENTOS
INSERT INTO departamento (nombre) VALUES
('Lima'),
('Arequipa'),
('Cusco');

-- PROVINCIAS
INSERT INTO provincia (nombre, departamento_id) VALUES
('Lima', 1),
('Huaral', 1),
('Arequipa', 2),
('Cusco', 3);

-- DISTRITOS
INSERT INTO distrito (nombre, provincia_id) VALUES
('Miraflores', 1),
('San Isidro', 1),
('Barranco', 1),
('Chancay', 2),
('Aucallama', 2),
('Cercado', 3),
('Yanahuara', 3),
('Wanchaq', 4),
('San Sebastián', 4);
