DO $$

DECLARE
    nombres TEXT[] := ARRAY[
        'Juan','Carlos','Luis','Pedro','Jose','Miguel','Jorge','Diego','Andres','Fernando',
        'Ricardo','Raul','Oscar','Hugo','Alberto','Victor','Daniel','Marco','Pablo','Sergio',
        'Mario','Eduardo','Julio','Roberto','Manuel','Ruben','Ivan','Felipe','Guillermo','Martin',
        'Alex','Bruno','Cesar','David','Ernesto','Fabian','Gonzalo','Hector','Ismael','Javier',
        'Kevin','Leonardo','Mateo','Nicolas','Orlando','Patricio','Quintin','Rafael','Samuel','Tomas',
        'Ulises','Valentin','Walter','Xavier','Yuri','Zaid'
    ];

    apellidos TEXT[] := ARRAY[
        'Garcia','Perez','Rodriguez','Sanchez','Ramirez','Torres','Flores','Rivera','Gomez','Diaz',
        'Vargas','Castro','Rojas','Ortega','Mendoza','Silva','Herrera','Medina','Aguilar','Campos',
        'Reyes','Morales','Cruz','Ortiz','Gutierrez','Chavez','Ramos','Navarro','Luna','Salazar',
        'Paredes','Delgado','Suarez','Bravo','Espinoza','Valdez','Cabrera','Peña','Arias','Cordero',
        'Mejia','Fuentes','Carrasco','Escobar','Villanueva','Montoya','Soto','Coronel','Quispe','Huaman'
    ];

    i INT;
    nombre TEXT;
    apellido TEXT;

BEGIN

FOR i IN 1..100 LOOP

    nombre := nombres[(random()*array_length(nombres,1)+1)::int];
    apellido := apellidos[(random()*array_length(apellidos,1)+1)::int];

    INSERT INTO tcliente00 (
        nombre, apellidos, dni, correo, celular, direccion,
        departamento_id, provincia_id, distrito_id,
        usuario
    )
    VALUES (
        nombre,
        apellido,
        (10000000 + i)::TEXT, -- DNI único
        lower(nombre||apellido||i||'@mail.com'),
        '9'||(10000000 + i)::TEXT,
        'Av. Siempre Viva '||i,
        (1 + (random()*2)::int), -- departamento 1-3
        (1 + (random()*3)::int),
        (1 + (random()*5)::int),
        'demo'
    );

END LOOP;

END $$;