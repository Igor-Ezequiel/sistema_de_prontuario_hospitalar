CREATE TABLE pacientes (

    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
    cpf VARCHAR(14) UNIQUE NOT NULL
    data_nascimento DATE NOT NULL,
    endereco_cep VARCHAR(9),
    usuario_id INT REFERENCES usuarios(id),
    convenio_id INT REFERENCES convenios(id)
);