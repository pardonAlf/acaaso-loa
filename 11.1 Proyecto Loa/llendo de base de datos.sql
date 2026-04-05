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
('Lurigancho', 1),
('San Isidro', 1),
('Barranco', 1),
('Chancay', 2),
('Aucallama', 2),
('Cercado', 3),
('Yanahuara', 3),
('Wanchaq', 4),
('San Sebastián', 4);

CREATE TABLE tcliente00 (

    id_cliente        SERIAL PRIMARY KEY,

    nombre            VARCHAR(100),
    apellidos         VARCHAR(100),
    dni               VARCHAR(15),
    correo            VARCHAR(150),
    celular           VARCHAR(20),
    direccion         VARCHAR(200),

    departamento_id   INT,
    provincia_id      INT,
    distrito_id       INT,

    usuario           VARCHAR(50),

	    fecha_registro    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	    fecha_modificacion TIMESTAMP,
	
	    estado            VARCHAR(20) DEFAULT 'nuevo',
    origen            VARCHAR(50) DEFAULT 'web',

    observaciones     TEXT

);

ALTER TABLE tcliente00 ADD CONSTRAINT unique_dni UNIQUE (dni);
ALTER TABLE tcliente00 ADD CONSTRAINT unique_correo UNIQUE (correo);
ALTER TABLE tcliente00 ADD CONSTRAINT unique_celular UNIQUE (celular);


SELECT * FROM TCLIENTE00

CREATE TABLE tplanes00 (

    idplan           SERIAL PRIMARY KEY,
    nombre           VARCHAR(100),
    velocidad        VARCHAR(50),   -- ejemplo: 1000 Mbps
    precio           NUMERIC(10,2),

    precio_oferta    NUMERIC(10,2),
    descripcion      TEXT,

    estado           VARCHAR(20) DEFAULT 'activo',

    fcreacion        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fmodificacion    TIMESTAMP,

    usuario          VARCHAR(50)

);
drop table tplaxcli00
CREATE TABLE tplaxcli00 (

    idplacli        SERIAL PRIMARY KEY,
    idcliente       INT,
    codplan         INT,

    fcreacion       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fmodificacion   TIMESTAMP,

    usuario         VARCHAR(50),

    estado          char(1) DEFAULT 'N'

);

select * from tplaxcli00
select * from distrito
select * from tcliente00


create table testado00
(idestado SERIAL PRIMARY KEY,
 cestado char(1),
 destado varchar(25),
 fcreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 fmodificacion TIMESTAMP,
 estado char(1) default 'N')

INSERT INTO testado00 (cestado, destado, fmodificacion )
VALUES
('N', 'Nuevo', NOW() ),
('P', 'Pendiente', NOW() ),
('T', 'Contactado', NOW() ),
('C', 'Pagado', NOW() );

select * from tplaxcli00

SELECT 
            c.id_cliente,
            c.nombre,
            c.apellidos,
            c.dni,
            c.correo,
            c.celular,
            c.direccion,

            d.nombre as departamento,
            p.nombre as provincia,
            di.nombre as distrito,

            pl.codplan,
            te.destado,
            c.usuario

        FROM tcliente00 c

        LEFT JOIN tplaxcli00 pl ON c.id_cliente = pl.idcliente
        LEFT JOIN departamento d ON c.departamento_id = d.id
        LEFT JOIN provincia p ON c.provincia_id = p.id
        LEFT JOIN distrito di ON c.distrito_id = di.id
        LEFT JOIN testado00 te ON te.cestado=pl.estado

        ORDER BY c.id_cliente DESC

delete from tplaxcli00
where idcliente=121 and idplacli<10

select * from tusuario00

CREATE TABLE tusuario00 (
    idusuario SERIAL PRIMARY KEY,

    dni VARCHAR(20),
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    correo VARCHAR(150),
    celular VARCHAR(20),

    usuario VARCHAR(50) UNIQUE,
    password VARCHAR(100),

    direccion VARCHAR(200),
    departamento_id INT,
    provincia_id INT,
    distrito_id INT,

    rol VARCHAR(20) DEFAULT 'Usuario',

    fcreacion TIMESTAMP,
    fmodificacion TIMESTAMP,

    estado CHAR(1) DEFAULT 'A'
);

INSERT INTO tusuario00 (
    dni, nombre, apellidos, correo, celular,
    usuario, password,
    direccion,
    departamento_id, provincia_id, distrito_id,
    rol, fcreacion, fmodificacion, estado
)
VALUES (
    '00000000', 'Admin', 'Sistema', 'admin@loa.com', '999999999',
    'admin', '123',
    'Sistema',
    1, 1, 1,
    'Admin', NOW(), NOW(), 'A'
);


select * from tplaxcli00
insert into tplaxcli00(idcliente,codplan,fcreacion,usuario,estado)
select id_cliente,1,fecha_registro,'web','N'
from tcliente00
where id_cliente not in (3,105,120,121)

select * from testado00
select * from tusuario00

