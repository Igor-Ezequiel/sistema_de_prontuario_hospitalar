-- ==========================================
-- 1. TABELAS INDEPENDENTES (Nível 0 - Sem chaves estrangeiras)
-- ==========================================

CREATE TABLE convenio (
    id SERIAL PRIMARY KEY,
    razao_social VARCHAR(150) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL 
);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE NOT NULL,
    cargo VARCHAR(55) NOT NULL
);

CREATE TABLE especialidade_medica (
    id SERIAL PRIMARY KEY,
    nome_especialidade VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cid (
    codigo VARCHAR(10) PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL
);

CREATE TABLE estoque_farmacia (
    id SERIAL PRIMARY KEY,
    nome_remedio VARCHAR(100) NOT NULL,
    miligramas NUMERIC(10, 2) NOT NULL,
    quantidade_atual INT NOT NULL
);

-- ==========================================
-- 2. TABELAS DE ATORES (Nível 1 - Dependem de Usuário e/ou Convênio/Especialidade)
-- ==========================================

CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    endereco_cep VARCHAR(9),           -- 'N' no diagrama (pode ser nulo)
    usuario_id INT UNIQUE REFERENCES usuario(id), -- 'N' no diagrama (nem todo paciente tem login)
    convenio_id INT REFERENCES convenio(id)       -- 'N' no diagrama (pode ser particular)
);

CREATE TABLE coordenador (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    setor_responsavel VARCHAR(100) NOT NULL,
    usuario_id INT UNIQUE REFERENCES usuario(id) NOT NULL -- Relação 1:1 obrigatória
);

CREATE TABLE enfermeiro (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    coren VARCHAR(20) UNIQUE NOT NULL,
    usuario_id INT UNIQUE REFERENCES usuario(id) NOT NULL -- Relação 1:1 obrigatória
);

CREATE TABLE medico (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade_medica_id INT REFERENCES especialidade_medica(id) NOT NULL,
    usuario_id INT UNIQUE REFERENCES usuario(id) NOT NULL -- Relação 1:1 obrigatória
);

-- ==========================================
-- 3. GESTÃO DE ATENDIMENTO E PLANTÃO (Nível 2)
-- ==========================================

CREATE TABLE plantao (
    id SERIAL PRIMARY KEY,
    setor_ala VARCHAR(100) NOT NULL,
    data_hora_inicio TIMESTAMP NOT NULL,
    data_hora_fim TIMESTAMP NOT NULL,
    medico_id INT REFERENCES medico(id) NOT NULL
);

CREATE TABLE atendimento (
    id SERIAL PRIMARY KEY,
    data_hora_entrada TIMESTAMP NOT NULL,
    data_hora_alta TIMESTAMP,          -- 'N' no diagrama
    status VARCHAR(50) NOT NULL,
    cor_risco VARCHAR(30),             -- CORRIGIDO: Removido o NOT NULL. A cor nasce nula e é preenchida após a triagem.
    paciente_id INT REFERENCES paciente(id) NOT NULL, -- Adicionado conforme a linha do diagrama
    medico_id INT REFERENCES medico(id)               -- 'N' no diagrama
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

CREATE TABLE auditoria_permissao_prontuario(
    id SERIAL PRIMARY KEY,
    acao VARCHAR(50) NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    justificativa VARCHAR(255) NOT NULL,
    medico_id INT REFERENCES medico(id),
    atendimento_id INT REFERENCES atendimento(id),
    coordenador_id INT REFERENCES coordenador(id)
);

-- ==========================================
-- 4. ROTINAS CLÍNICAS E ANEXOS (Nível 3)
-- ==========================================

CREATE TABLE triagem (
    id SERIAL PRIMARY KEY,
    pressao_arterial VARCHAR(20) NOT NULL,
    temperatura FLOAT NOT NULL,
    saturacao FLOAT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    atendimento_id INT REFERENCES atendimento(id) NOT NULL,
    enfermeiro_id INT REFERENCES enfermeiro(id) NOT NULL
);

CREATE TABLE anexo_foto (
    id SERIAL PRIMARY KEY,
    url_arquivo VARCHAR(255) NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    descricao VARCHAR(255),            -- 'N' no diagrama
    atendimento_id INT REFERENCES atendimento(id) NOT NULL,
    enfermeiro_id INT REFERENCES enfermeiro(id) NOT NULL
);

CREATE TABLE evolucao_clinica (
    id SERIAL PRIMARY KEY,
    relato_clinico_observacoes VARCHAR(1000) NOT NULL,
    dias_entubacao INT,                  -- 'N' no diagrama
    data_hora TIMESTAMP NOT NULL,
    atendimento_id INT REFERENCES atendimento(id) NOT NULL,
    medico_id INT REFERENCES medico(id) NOT NULL
);

-- ==========================================
-- 5. PRESCRIÇÃO E DIAGNÓSTICO (Nível 4)
-- ==========================================

CREATE TABLE diagnostico (
    id SERIAL PRIMARY KEY,
    evolucao_clinica_id INT REFERENCES evolucao_clinica(id) NOT NULL,
    cid_codigo VARCHAR(10) REFERENCES cid(codigo) NOT NULL
);

CREATE TABLE prescricao_medica (
    id SERIAL PRIMARY KEY,
    dose FLOAT NOT NULL,
    intervalo_em_horas INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    evolucao_clinica_id INT REFERENCES evolucao_clinica(id) NOT NULL,
    estoque_farmacia_id INT REFERENCES estoque_farmacia(id) NOT NULL
);

-- ==========================================
-- 6. ADMINISTRAÇÃO DE MEDICAMENTOS (Nível 5)
-- ==========================================

CREATE TABLE administracao_enfermagem (
    id SERIAL PRIMARY KEY,
    data_hora_aplicacao TIMESTAMP NOT NULL,
    observacao_reacao VARCHAR(255),    -- 'N' no diagrama
    prescricao_medica_id INT REFERENCES prescricao_medica(id) NOT NULL,
    enfermeiro_id INT REFERENCES enfermeiro(id) NOT NULL
);