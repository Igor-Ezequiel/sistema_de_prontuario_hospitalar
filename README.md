🏥 Sistema de Prontuário Hospitalar

API REST para gestão hospitalar: cadastro de equipe médica e pacientes, escala de plantões, recepção com fila de prioridade por classificação de risco (Protocolo de Manchester), triagem, evolução clínica com diagnósticos CID, prescrições médicas e prontuário completo por atendimento.

Desenvolvida em Python + FastAPI com PostgreSQL, seguindo uma arquitetura em camadas (Controller → Service → Repository).

📑 Sumário
Funcionalidades
Tecnologias
Arquitetura
Fluxo de atendimento
Regras de negócio
Modelo de dados
Instalação e execução
Endpoints
Pontos de atenção
Autor
✨ Funcionalidades
Usuários e autenticação: login por e-mail e senha, ativação/desativação de contas, senhas armazenadas com hash scrypt.
Equipe médica: CRUD de médicos (CRM, especialidade), enfermeiros (COREN) e coordenadores (setor responsável).
Pacientes: cadastro com CPF único, data de nascimento e CEP; possibilidade de vínculo com um usuário.
Plantões: alocação de médicos por setor/ala e período, com verificação de disponibilidade e conflito de horário.
Recepção e fila de prioridade: abertura de atendimento e fila ordenada por cor de risco e ordem de chegada.
Triagem: registro de pressão arterial, temperatura e saturação pelo enfermeiro, com classificação de risco.
Evolução clínica: relato do médico responsável, dias de entubação e diagnósticos vinculados ao catálogo CID.
Prescrições: prescrição pelo médico e aplicação/cancelamento com rastreio de quem administrou e quando.
Permissão extra: coordenador pode transferir um prontuário para outro médico, com motivo obrigatório registrado.
Prontuário e auditoria: consulta do prontuário completo e de uma visão voltada a auditoria.
🛠 Tecnologias
Camada	Tecnologia
Linguagem	Python 3.12
Framework web	FastAPI
Validação de dados	Pydantic
Banco de dados	PostgreSQL
Driver	psycopg2
Configuração	python-dotenv (.env)
Segurança	hashlib.scrypt + hmac.compare_digest
🧱 Arquitetura
.
├── main.py                  # Ponto de entrada da aplicação FastAPI
├── Teste_Completo.py        # Simulação de ponta a ponta com banco em memória (SQLite)
├── .env.example             # Modelo das variáveis de ambiente
├── database/
│   ├── connection.py        # Conexão com o PostgreSQL
│   └── schema.sql           # Script de criação das tabelas
└── src/
    ├── routers.py           # Agrega os routers sob o prefixo /api/v1
    ├── config.py            # Leitura das variáveis de ambiente
    ├── deps.py              # Dependência get_db (abre/fecha conexão por requisição)
    ├── exceptions.py        # Exceções de domínio
    ├── security.py          # Hash e verificação de senha
    ├── controller/          # Rotas HTTP (uma por entidade)
    ├── schemas/             # Modelos Pydantic de entrada e saída
    ├── models/Classes.py    # Entidades de domínio e enums
    ├── service/             # Regras de negócio
    └── repositori/          # Acesso ao banco (SQL)

Fluxo de uma requisição: Controller valida a entrada (Pydantic) → Service aplica as regras de negócio → Repository executa o SQL → exceções de domínio (NaoEncontradoError, RegraDeNegocioError, PermissaoNegadaError) são convertidas em respostas HTTP 404, 400 e 403.

🔄 Fluxo de atendimento
Paciente chega
      │
      ▼
POST /atendimentos            →  status: Aguardando Triagem  (risco: Cinza)
      │
      ├── Emergência ───────────────►  PATCH /atendimentos/{id}/risco  (Vermelho)
      │                                 └─ vai direto para a fila, status: Em Atendimento
      ▼
POST /triagens                →  enfermeiro registra sinais vitais e classifica o risco
      │                          status: Aguardando Médico  →  entra na fila de prioridade
      ▼
POST /atendimentos/chamar-proximo  →  médico em plantão ativo chama o próximo da fila
      │                               status: Em Atendimento
      ▼
POST /evolucoes  (+ diagnósticos CID)  →  POST /prescricoes
      │                                        └─ enfermeiro: PATCH /prescricoes/{id}/aplicar
      ▼
PATCH /atendimentos/{id}/alta →  status: Alta (somente o médico responsável)

Status do atendimento: Aguardando Triagem · Aguardando Médico · Em Atendimento · Alta · Cancelado
Status da prescrição: Pendente · Aplicada · Cancelada

📋 Regras de negócio

Fila de prioridade (Manchester)

Cor	Peso	Prioridade
🔴 Vermelho	9	Emergência
🟠 Laranja	8	Muito urgente
🟡 Amarelo	7	Urgente
🟢 Verde	6	Pouco urgente
🔵 Azul	5	Não urgente
⚪ Cinza	0	Ainda não classificado
Pacientes de maior peso são atendidos primeiro; em empate, vale a ordem de chegada.
A fila tem capacidade máxima de 500 pacientes.
Risco Vermelho não passa pela triagem comum: é classificado diretamente no atendimento.

Atendimento e médicos

Só um médico com plantão ativo no momento pode chamar o próximo paciente.
Alta só pode ser dada por quem é o médico responsável, e apenas com o atendimento em status Em Atendimento.
Um atendimento com alta não pode ser cancelado.
A triagem só é permitida com o atendimento em Aguardando Triagem.
A alocação de plantão exige que o médico esteja disponível no intervalo informado.

Evolução clínica

Só pode ser registrada com o atendimento Em Atendimento, pelo médico responsável.
O relato não pode estar vazio e todo código CID informado precisa existir no catálogo.
Apenas o médico autor pode editar, excluir ou adicionar diagnósticos; um mesmo CID não pode ser vinculado duas vezes à mesma evolução.

Prescrição

Nome do medicamento e dose são obrigatórios.
Uma prescrição já aplicada não pode ser cancelada nem aplicada novamente (evita dose duplicada).
Uma prescrição cancelada não pode ser administrada.

Permissão extra

O coordenador transfere o prontuário a outro médico informando o motivo (obrigatório); o registro fica salvo para auditoria.

Usuários

Senha com no mínimo 6 caracteres, armazenada com scrypt.
E-mail único; usuários inativos não conseguem fazer login.
🗄 Modelo de dados

Tabelas definidas em database/schema.sql:

usuario · coordenador · enfermeiro · medico · paciente · plantao · atendimento · triagem · evolucao_clinica · cid · diagnostico · prescricao · permissao_extra

Médicos, enfermeiros e coordenadores compartilham a chave primária com usuario (herança por tabela). Um atendimento pertence a um paciente e agrupa triagens, evoluções clínicas (com diagnósticos e prescrições) e permissões extras.

🚀 Instalação e execução
Pré-requisitos
Python 3.12+
PostgreSQL em execução
Passo a passo
bash
# 1. Clone o repositório
git clone https://github.com/Igor-Ezequiel/sistema_de_prontuario_hospitalar.git
cd sistema_de_prontuario_hospitalar

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install fastapi "uvicorn[standard]" psycopg2-binary python-dotenv pydantic

O repositório ainda não possui requirements.txt; os pacotes acima são os usados no código.

Configuração do banco
bash
# Crie o banco e aplique o schema
createdb nome_do_banco
psql -d nome_do_banco -f database/schema.sql

Em seguida copie o modelo de variáveis de ambiente e preencha:

bash
cp .env.example .env
env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
SECRET_SALT=uma_string_longa_e_aleatoria

⚠️ SECRET_SALT é usado no hash das senhas. Defina um valor forte e não o altere depois, ou os logins existentes deixarão de funcionar. Nunca versione o arquivo .env.

Executando
bash
uvicorn main:app --reload
API: http://localhost:8000
Documentação interativa (Swagger): http://localhost:8000/docs
Documentação alternativa (ReDoc): http://localhost:8000/redoc
Health check: GET / → {"status": "online", ...}
Teste de ponta a ponta

O arquivo Teste_Completo.py simula o fluxo completo (atendimento, triagem, fila, evolução e alta) usando um banco SQLite em memória e imprime o prontuário no terminal.

🔌 Endpoints

Todas as rotas ficam sob o prefixo /api/v1.

Usuários — /usuarios
Método	Rota	Descrição
POST	/login	Autentica com e-mail e senha
POST	/	Cria usuário
GET	/{id_usuario}	Busca usuário
PUT	/{id_usuario}/credenciais	Atualiza e-mail e/ou senha
PATCH	/{id_usuario}/desativar	Desativa usuário
PATCH	/{id_usuario}/reativar	Reativa usuário
Equipe médica — /medicos, /enfermeiros, /coordenadores
Método	Rota	Descrição
POST	/	Cadastra
GET	/{id}	Busca por ID
PUT	/{id}	Atualiza
DELETE	/{id}	Remove
GET	/medicos/disponiveis	Lista médicos disponíveis
Pacientes — /pacientes
Método	Rota	Descrição
POST	/	Cadastra paciente
GET	/{id_paciente}	Busca paciente
PUT	/{id_paciente}	Atualiza
DELETE	/{id_paciente}	Remove
Plantões — /plantoes
Método	Rota	Descrição
POST	/	Aloca médico em um plantão
GET	/{id_plantao}	Busca plantão
GET	/{id_plantao}/detalhes	Plantão com dados de médico e coordenador
PUT	/{id_plantao}	Atualiza
DELETE	/{id_plantao}	Cancela
Atendimentos — /atendimentos
Método	Rota	Descrição
POST	/	Abre atendimento (aguardando triagem)
GET	/fila/status	Situação da fila de prioridade
POST	/chamar-proximo	Médico chama o próximo paciente
GET	/{id}	Dados simples do atendimento
GET	/{id}/prontuario	Prontuário completo
GET	/{id}/auditoria	Prontuário para auditoria
PATCH	/{id}/risco	Reclassifica o risco
PATCH	/{id}/alta	Registra a alta
POST	/{id}/permissao-extra	Concede permissão extra a outro médico
DELETE	/{id}	Cancela atendimento
Triagens — /triagens
Método	Rota	Descrição
POST	/	Registra triagem
GET	/{id_triagem}	Busca triagem
GET	/atendimento/{atendimento_id}	Histórico de triagens do atendimento
PUT	/{triagem_id}	Corrige sinais vitais
DELETE	/{triagem_id}	Exclui triagem inválida
Evoluções clínicas — /evolucoes
Método	Rota	Descrição
POST	/	Registra evolução (com CIDs opcionais)
POST	/{id_evolucao}/diagnosticos	Vincula novo diagnóstico CID
GET	/{id_evolucao}	Busca evolução com diagnósticos e prescrições
GET	/atendimento/{atendimento_id}	Histórico de evoluções
PUT	/{id_evolucao}	Edita relato
DELETE	/{id_evolucao}	Exclui evolução
Prescrições — /prescricoes
Método	Rota	Descrição
POST	/	Prescreve medicamento
PATCH	/{id_prescricao}/aplicar	Enfermeiro registra a aplicação
PATCH	/{id_prescricao}/cancelar	Médico cancela
GET	/{id_prescricao}/detalhes	Detalhes, incluindo quem aplicou
⚠️ Pontos de atenção

Itens identificados no código que valem ser tratados antes de uso real:

Autenticação: o login valida as credenciais, mas não emite token (JWT/sessão); as demais rotas não exigem autenticação nem verificam o cargo do chamador.
Fila em memória: a fila de prioridade vive na memória do processo; é perdida ao reiniciar o servidor e não é compartilhada entre múltiplos workers.
Dependências: falta um requirements.txt com versões fixadas.
Dados sensíveis: prontuários são dados de saúde protegidos pela LGPD; a produção exige controle de acesso, criptografia e trilha de auditoria.

👤 Autores

Desenvolvido por Igor Ezequiel — @Igor-Ezequiel
Regras de Negócio por Binha Dauma - @binhadauma
