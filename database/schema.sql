
CREATE TABLE cid (
    codigo VARCHAR(10) PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL
);



CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE NOT NULL,
    cargo VARCHAR(55) NOT NULL
);

CREATE TABLE coordenador (
    id INT PRIMARY KEY REFERENCES usuario(id),
    nome VARCHAR(150) NOT NULL,
    setor_responsavel VARCHAR(100) NOT NULL
);

CREATE TABLE enfermeiro (
    id INT PRIMARY KEY REFERENCES usuario(id),
    nome VARCHAR(150) NOT NULL,
    coren VARCHAR(20) UNIQUE NOT NULL
);


CREATE TABLE medico (
    id INT PRIMARY KEY REFERENCES usuario(id),
    nome VARCHAR(150) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade_medica_id VARCHAR(100)
);


CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    endereco_cep VARCHAR(9),
    ativo BOOLEAN DEFAULT TRUE,      
    usuario_id INT UNIQUE REFERENCES usuario(id), 
         
);

CREATE TABLE plantao (
    id SERIAL PRIMARY KEY,
    setor_ala VARCHAR(100) NOT NULL,
    data_hora_inicio TIMESTAMP NOT NULL,
    data_hora_fim TIMESTAMP NOT NULL,
    medico_id INT REFERENCES medico(id) NOT NULL,
    coordenador_id INT REFERENCES coordenador(id) NOT NULL
);

CREATE TABLE atendimento (
    id SERIAL PRIMARY KEY,
    data_hora_entrada TIMESTAMP NOT NULL,
    data_hora_alta TIMESTAMP,          
    status VARCHAR(50) NOT NULL,
    cor_risco VARCHAR(30),             
    paciente_id INT REFERENCES paciente(id) NOT NULL, 
    medico_id INT REFERENCES medico(id)               
);



CREATE TABLE triagem (
    id SERIAL PRIMARY KEY,
    pressao_arterial VARCHAR(20) NOT NULL,
    temperatura FLOAT NOT NULL,
    saturacao INT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    atendimento_id INT REFERENCES atendimento(id) NOT NULL,
    enfermeiro_id INT REFERENCES enfermeiro(id) NOT NULL
);

CREATE TABLE evolucao_clinica (
    id SERIAL PRIMARY KEY,
    relato_clinico_observacoes VARCHAR(1000) NOT NULL,
    dias_entubacao INT,                    
    data_hora TIMESTAMP NOT NULL,
    atendimento_id INT REFERENCES atendimento(id) NOT NULL,
    medico_id INT REFERENCES medico(id) NOT NULL
);


CREATE TABLE diagnostico (
    id SERIAL PRIMARY KEY,
    Evolucao_Clinicaid INT REFERENCES evolucao_clinica(id) NOT NULL,
    CIDcodigo VARCHAR(10) REFERENCES cid(codigo) NOT NULL
);


CREATE TABLE prescricao (
    id SERIAL PRIMARY KEY,
    nome_medicamento VARCHAR(150) NOT NULL,
    dose VARCHAR(50) NOT NULL,
    intervalo_horas INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    evolucao_id INT REFERENCES evolucao_clinica(id) NOT NULL,
    enfermeiro_id INT REFERENCES enfermeiro(id),
    data_hora_aplicacao TIMESTAMP
);



CREATE TABLE permissao_extra (
    id SERIAL PRIMARY KEY,
    data_hora_liberacao TIMESTAMP NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    validade TIMESTAMP NOT NULL,
    medico_id INT REFERENCES medico(id),
    atendimento_id INT REFERENCES atendimento(id),
    coordenador_id INT REFERENCES coordenador(id)
);

