from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Sistema Pão de Queijo")

templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")


# ==========================================
# CONEXÃO COM O BANCO DE DADOS
# ==========================================

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="empresa_pao_de_queijo"
    )


# ==========================================
# CRIAR TABELA DE CLIENTES
# ==========================================
# =========================================================
# CRIAR TABELA DE CLIENTES
# =========================================================

def criar_tabela_clientes():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            telefone VARCHAR(30),
            endereco VARCHAR(255)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()


# =========================================================
# API - LISTAR CLIENTES
# =========================================================

@app.get("/api/clientes")
def listar_clientes():
    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            telefone,
            endereco
        FROM clientes
        ORDER BY nome
    """)

    clientes = cursor.fetchall()
    cursor.close()
    banco.close()

    return clientes
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            telefone VARCHAR(30),
            endereco VARCHAR(255),
            email VARCHAR(150)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()
# ==========================================
# CRIAR TABELA DE PAGAMENTOS
# ==========================================

def criar_tabela_pagamentos():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            colaborador_id INT NOT NULL,
            valor DECIMAL(10,2) NOT NULL,
            data_pagamento DATE NOT NULL,
            forma_pagamento VARCHAR(30) DEFAULT 'PIX',
            observacao VARCHAR(255),
            FOREIGN KEY (colaborador_id) REFERENCES colaboradores(id)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()


# ==========================================
# CRIAR TABELA DE PEDIDOS
# ==========================================

def criar_tabela_pedidos():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            data_pedido DATE NOT NULL,
            valor_total DECIMAL(10,2) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'Recebido'
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()

    
# ==========================================
# CRIAR TABELA DE ITENS DO PEDIDO
# ==========================================

def criar_tabela_itens_pedido():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pedido_id INT NOT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL,
            preco_unitario DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()


# ==========================================
# CRIAR TABELA DE MOVIMENTAÇÕES DO ESTOQUE
# ==========================================

def criar_tabela_movimentacoes_estoque():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produto_id INT NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            quantidade INT NOT NULL,
            data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            observacao VARCHAR(255),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()

# ==========================================
# CRIAR TABELA DE PEDIDOS
# ==========================================

def criar_tabela_pedidos():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            data_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            valor_total DECIMAL(10,2) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'Recebido',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()
# =========================================================
# CRIAR TABELA DE COLABORADORES
# =========================================================

def criar_tabela_colaboradores():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            cpf VARCHAR(14),
            telefone VARCHAR(30),
            email VARCHAR(150),
            chave_pix VARCHAR(255),
            situacao VARCHAR(20) NOT NULL DEFAULT 'Ativo',
            data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()


# ==========================================
# CRIAR TABELA DE INDICAÇÕES
# ==========================================

def criar_tabela_indicacoes():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            colaborador_id INT NOT NULL,
            cliente_id INT,
            produto_id INT,
            data_indicacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            situacao VARCHAR(30) NOT NULL DEFAULT 'Pendente',
            valor_indicacao DECIMAL(10,2),
            observacao TEXT
        )
    """)

    banco.commit()
    cursor.close()
    banco.close()


# =========================================================
# INICIALIZAÇÃO DAS TABELAS
# =========================================================

criar_tabela_clientes()
criar_tabela_pedidos()
criar_tabela_itens_pedido()
criar_tabela_movimentacoes_estoque()
criar_tabela_colaboradores()
criar_tabela_indicacoes()
criar_tabela_pagamentos()
# =========================================================
# INICIALIZAÇÃO DAS TABELAS
# =========================================================
criar_tabela_clientes()
criar_tabela_pedidos()
criar_tabela_itens_pedido()
criar_tabela_movimentacoes_estoque()
criar_tabela_colaboradores()
criar_tabela_indicacoes()
criar_tabela_pagamentos()
# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.get("/")
def inicio():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(valor_total), 0) FROM pedidos WHERE status != 'Cancelado'")
    total_vendas = cursor.fetchone()[0]

    cursor.close()
    banco.close()

    return FileResponse("templates/index.html")

# ==========================================
# PÁGINA DE CLIENTES
# ==========================================

@app.get("/clientes")
def pagina_clientes():
    return FileResponse("templates/clientes.html")

# ==========================================
# PÁGINA DE COLABORADORES
# ==========================================
@app.get("/colaboradores")
def pagina_colaboradores():
    return FileResponse("templates/colaboradores.html")
# ==========================================
# API - LISTAR COLABORADORES
# ==========================================

@app.get("/api/colaboradores")
def listar_colaboradores():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            cpf,
            telefone,
            email,
            chave_pix,
            situacao,
            data_cadastro
        FROM colaboradores
        ORDER BY nome
    """)

    colaboradores = cursor.fetchall()

    cursor.close()
    banco.close()

    return colaboradores

# ==========================================
# PÁGINA - NOVO COLABORADOR
# ==========================================
@app.get("/novo_colaborador")
def pagina_novo_colaborador():
    return FileResponse("templates/novo_colaborador.html")

# ==========================================
# PÁGINA - EDITAR COLABORADOR
# ==========================================

@app.get("/editar_colaborador/{colaborador_id}")
def pagina_editar_colaborador(colaborador_id: int):
    return FileResponse("templates/editar_colaborador.html")

@app.post("/editar_colaborador/{colaborador_id}")
def atualizar_colaborador(
    colaborador_id: int,
    nome: str = Form(...),
    cpf: str = Form(""),
    telefone: str = Form(""),
    email: str = Form(""),
    chave_pix: str = Form(""),
    situacao: str = Form("Ativo")
):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE colaboradores
        SET nome = %s,
            cpf = %s,
            telefone = %s,
            email = %s,
            chave_pix = %s,
            situacao = %s
        WHERE id = %s
    """, (
        nome,
        cpf,
        telefone,
        email,
        chave_pix,
        situacao,
        colaborador_id
    ))

    banco.commit()
    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/colaboradores",
        status_code=303
    )
# ==========================================
# ATIVAR / INATIVAR COLABORADOR
# ==========================================

@app.post("/colaborador/{colaborador_id}/alterar_situacao")
def alterar_situacao_colaborador(colaborador_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE colaboradores
        SET situacao = CASE
            WHEN situacao = 'Ativo' THEN 'Inativo'
            ELSE 'Ativo'
        END
        WHERE id = %s
    """, (colaborador_id,))

    banco.commit()
    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/colaboradores",
        status_code=303
    )
# ==========================================
# API - BUSCAR COLABORADOR PARA EDIÇÃO
# ==========================================

@app.get("/api/colaboradores/{colaborador_id}")
def buscar_colaborador(colaborador_id: int):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            cpf,
            telefone,
            email,
            chave_pix,
            situacao
        FROM colaboradores
        WHERE id = %s
    """, (colaborador_id,))

    colaborador = cursor.fetchone()

    cursor.close()
    banco.close()

    if not colaborador:
        return {"erro": "Colaborador não encontrado."}

    return colaborador

# ==========================================
# CADASTRAR NOVO COLABORADOR
# ==========================================

@app.post("/novo_colaborador")
async def cadastrar_colaborador(request: Request):

    dados = await request.form()

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    email = dados.get("email")
    chave_pix = dados.get("chave_pix")
    situacao = dados.get("situacao")

    if not nome:
        return {"erro": "O nome do colaborador é obrigatório."}

    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            INSERT INTO colaboradores
            (nome, cpf, telefone, email, chave_pix, situacao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nome,
            cpf,
            telefone,
            email,
            chave_pix,
            situacao
        ))

        banco.commit()

        return RedirectResponse(
            url="/colaboradores",
            status_code=303
        )

    except Exception as erro:
        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:
        cursor.close()
        banco.close()

# ==========================================
# PÁGINA - NOVO CLIENTE
# ==========================================

@app.get("/novo_cliente")
def pagina_novo_cliente():
    return FileResponse("templates/novo_cliente.html")

# ==========================================
# PÁGINA - EDITAR CLIENTE
# ==========================================

@app.get("/editar_cliente/{cliente_id}")
def pagina_editar_cliente(cliente_id: int):
    return FileResponse("templates/editar_cliente.html")

# ==========================================
# API - OBTER CLIENTE
# ==========================================

@app.get("/api/clientes/{cliente_id}")
def obter_cliente(cliente_id: int):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, telefone, endereco
        FROM clientes
        WHERE id = %s
    """, (cliente_id,))

    cliente = cursor.fetchone()

    cursor.close()
    banco.close()

    if not cliente:
        return {"erro": "Cliente não encontrado."}

    return cliente


# ==========================================
# API - ATUALIZAR CLIENTE
# ==========================================

@app.put("/api/clientes/{cliente_id}")
async def atualizar_cliente(cliente_id: int, request: Request):

    dados = await request.json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    endereco = dados.get("endereco")

    if not nome:
        return {"erro": "O nome do cliente é obrigatório."}

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nome = %s,
            telefone = %s,
            endereco = %s
        WHERE id = %s
    """, (nome, telefone, endereco, cliente_id))

    banco.commit()

    cursor.close()
    banco.close()

    return {"mensagem": "Cliente atualizado com sucesso!"}


@app.post("/novo_cliente")
async def cadastrar_cliente(request: Request):
    dados = await request.form()

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    endereco = dados.get("endereco")

    if not nome:
        return {"erro": "O nome do cliente é obrigatório."}

    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, endereco)
            VALUES (%s, %s, %s)
        """, (
            nome,
            telefone,
            endereco
        ))

        banco.commit()

        return RedirectResponse(
            url="/clientes",
            status_code=303
        )

    except Exception as erro:
        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:
        cursor.close()
        banco.close()


@app.get("/api/dashboard")
def dados_dashboard(periodo: str = "todos"):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    filtro_data = ""

    if periodo == "hoje":
        filtro_data = "AND DATE(data_pedido) = CURDATE()"

    elif periodo == "7dias":
        filtro_data = "AND data_pedido >= DATE_SUB(NOW(), INTERVAL 7 DAY)"

    elif periodo == "mes":
        filtro_data = """
            AND MONTH(data_pedido) = MONTH(CURDATE())
            AND YEAR(data_pedido) = YEAR(CURDATE())
        """

    cursor.execute(f"""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status != 'Cancelado'
        {filtro_data}
    """)

    total_pedidos = cursor.fetchone()[0]

    cursor.execute(f"""
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE status != 'Cancelado'
        {filtro_data}
    """)

    total_vendas = cursor.fetchone()[0]

    cursor.close()
    banco.close()

    return {
        "total_produtos": total_produtos,
        "total_pedidos": total_pedidos,
        "total_clientes": total_clientes,
        "total_vendas": float(total_vendas)
    }
@app.get("/api/relatorios/produtos-mais-vendidos")
def produtos_mais_vendidos(periodo: str = "todos"):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        filtro_data = ""

        if periodo == "hoje":
            filtro_data = """
                AND DATE(pe.data_pedido) = CURDATE()
            """

        elif periodo == "7dias":
            filtro_data = """
                AND pe.data_pedido >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            """

        elif periodo == "mes":
            filtro_data = """
                AND YEAR(pe.data_pedido) = YEAR(CURDATE())
                AND MONTH(pe.data_pedido) = MONTH(CURDATE())
            """

        cursor.execute(f"""
            SELECT
                p.nome AS produto,
                SUM(ip.quantidade) AS quantidade_vendida
            FROM itens_pedido ip
            INNER JOIN produtos p
                ON p.id = ip.produto_id
            INNER JOIN pedidos pe
                ON pe.id = ip.pedido_id
            WHERE pe.status != 'Cancelado'
            {filtro_data}
            GROUP BY p.id, p.nome
            ORDER BY quantidade_vendida DESC
        """)

        dados = cursor.fetchall()

        return dados

    except Exception as erro:

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()
def dados_dashboard():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE status != 'Cancelado'
    """)
    total_vendas = cursor.fetchone()[0]

    cursor.close()
    banco.close()

    return {
        "total_produtos": total_produtos,
        "total_pedidos": total_pedidos,
        "total_clientes": total_clientes,
        "total_vendas": float(total_vendas)
    }
# ==========================================
# API - RELATÓRIO DE PEDIDOS
# ==========================================

@app.get("/api/relatorios/pedidos")
def relatorio_pedidos(periodo: str = "todos"):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        filtro_data = ""

        if periodo == "hoje":
            filtro_data = """
                AND DATE(data_pedido) = CURDATE()
            """

        elif periodo == "7dias":
            filtro_data = """
                AND data_pedido >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            """

        elif periodo == "mes":
            filtro_data = """
                AND YEAR(data_pedido) = YEAR(CURDATE())
                AND MONTH(data_pedido) = MONTH(CURDATE())
            """

        cursor.execute(f"""
            SELECT
                status,
                COUNT(*) AS quantidade
            FROM pedidos
            WHERE 1 = 1
            {filtro_data}
            GROUP BY status
            ORDER BY quantidade DESC
        """)

        dados = cursor.fetchall()

        return dados

    except Exception as erro:

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()
# ==========================================
# PÁGINA DE PRODUTOS
# ==========================================

@app.get("/produtos")
def pagina_produtos():
    return FileResponse("templates/produtos.html")

# ==========================================
# PÁGINA - INDICAÇÕES
# ==========================================

@app.get("/indicacoes")
def pagina_indicacoes():
    return FileResponse("templates/indicacoes.html")


# ==========================================
# PÁGINA - PAGAMENTOS
# ==========================================

@app.get("/pagamentos")
def pagina_pagamentos():
    return FileResponse("templates/pagamentos.html")
# ==========================================
# PÁGINA - NOVO PAGAMENTO
# ==========================================

@app.get("/novo_pagamento")
def pagina_novo_pagamento():
    return FileResponse("templates/novo_pagamento.html")

# ==========================================
# CADASTRAR NOVO PAGAMENTO
# ==========================================

@app.post("/novo_pagamento")
def cadastrar_pagamento(
    colaborador_id: int = Form(...),
    valor: float = Form(...),
    data_pagamento: str = Form(...),
    forma_pagamento: str = Form("PIX"),
    observacao: str = Form("")
):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        INSERT INTO pagamentos (
            colaborador_id,
            valor,
            data_pagamento,
            forma_pagamento,
            observacao
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        colaborador_id,
        valor,
        data_pagamento,
        forma_pagamento,
        observacao
    ))

    banco.commit()
    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/pagamentos",
        status_code=303
    )

# ==========================================
# PÁGINA - NOVA INDICAÇÃO
# ==========================================

@app.get("/nova_indicacao")
def pagina_nova_indicacao():
    return FileResponse("templates/nova_indicacao.html")

# ==========================================
# CADASTRAR NOVA INDICAÇÃO
# ==========================================

@app.post("/nova_indicacao")
def cadastrar_indicacao(
    colaborador_id: int = Form(...),
    cliente_id: str = Form(""),
    produto_id: str = Form(""),
    data_indicacao: str = Form(...),
    situacao: str = Form("Pendente"),
    valor_indicacao: str = Form(""),
    observacao: str = Form("")
):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        INSERT INTO indicacoes (
            colaborador_id,
            cliente_id,
            produto_id,
            data_indicacao,
            situacao,
            valor_indicacao,
            observacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        colaborador_id,
        cliente_id if cliente_id else None,
        produto_id if produto_id else None,
        data_indicacao,
        situacao,
        valor_indicacao if valor_indicacao else None,
        observacao
    ))

    banco.commit()
    cursor.close()
    

    return RedirectResponse(
        url="/indicacoes",
        status_code=303
    )


# ==========================================
# API - LISTAR INDICAÇÕES
# ==========================================

# ==========================================
# API - LISTAR INDICAÇÕES
# ==========================================

@app.get("/api/indicacoes")
def listar_indicacoes():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            i.id,
            c.nome AS colaborador,
            cl.nome AS cliente,
            p.nome AS produto,
            DATE_FORMAT(i.data_indicacao, '%d/%m/%Y') AS data_indicacao,
            i.situacao,
            i.valor_indicacao
        FROM indicacoes i
        LEFT JOIN colaboradores c
            ON i.colaborador_id = c.id
        LEFT JOIN clientes cl
            ON i.cliente_id = cl.id
        LEFT JOIN produtos p
            ON i.produto_id = p.id
        ORDER BY i.id DESC
    """)

    indicacoes = cursor.fetchall()

    cursor.close()
    banco.close()

    return indicacoes

# ==========================================
# EXCLUIR INDICAÇÃO
# ==========================================

@app.post("/excluir_indicacao/{indicacao_id}")
def excluir_indicacao(indicacao_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM indicacoes WHERE id = %s",
        (indicacao_id,)
    )

    banco.commit()

    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/indicacoes",
        status_code=303
    )

# ==========================================
# PÁGINA - EDITAR INDICAÇÃO
# ==========================================

@app.get("/editar_indicacao/{indicacao_id}")
def editar_indicacao(request: Request, indicacao_id: int):
    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            colaborador_id,
            cliente_id,
            produto_id,
            data_indicacao,
            situacao,
            valor_indicacao,
            observacao
        FROM indicacoes
        WHERE id = %s
    """, (indicacao_id,))

    indicacao = cursor.fetchone()

    cursor.execute("""
        SELECT id, nome
        FROM colaboradores
        WHERE situacao = 'Ativo'
        ORDER BY nome
    """)

    colaboradores = cursor.fetchall()

    cursor.execute("""
        SELECT id, nome
        FROM clientes
        ORDER BY nome
    """)

    clientes = cursor.fetchall()

    cursor.execute("""
        SELECT id, nome
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    cursor.close()
    banco.close()

    if indicacao is None:
        return RedirectResponse(
            url="/indicacoes",
            status_code=303
        )

    return templates.TemplateResponse(
    request=request,
    name="editar_indicacao.html",
    context={
        "request": request,
        "indicacao": indicacao,
        "colaboradores": colaboradores,
        "clientes": clientes,
        "produtos": produtos
    }
)
# ==========================================
# ATUALIZAR INDICAÇÃO
# ==========================================

@app.post("/editar_indicacao/{indicacao_id}")
def atualizar_indicacao(
    indicacao_id: int,
    colaborador_id: int = Form(...),
    cliente_id: str = Form(""),
    produto_id: str = Form(""),
    data_indicacao: str = Form(...),
    situacao: str = Form("Pendente"),
    valor_indicacao: str = Form(""),
    observacao: str = Form("")
):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE indicacoes
        SET
            colaborador_id = %s,
            cliente_id = %s,
            produto_id = %s,
            data_indicacao = %s,
            situacao = %s,
            valor_indicacao = %s,
            observacao = %s
        WHERE id = %s
    """, (
        colaborador_id,
        cliente_id if cliente_id else None,
        produto_id if produto_id else None,
        data_indicacao,
        situacao,
        valor_indicacao if valor_indicacao else None,
        observacao,
        indicacao_id
    ))

    banco.commit()

    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/indicacoes",
        status_code=303
    )
# ==========================================
# API - LISTAR PAGAMENTOS
# ==========================================

@app.get("/api/pagamentos")
def listar_pagamentos():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id,
            c.nome AS colaborador,
            p.valor,
            p.data_pagamento,
            p.forma_pagamento,
            p.observacao
        FROM pagamentos p
        INNER JOIN colaboradores c
            ON c.id = p.colaborador_id
        ORDER BY p.id DESC
    """)

    pagamentos = cursor.fetchall()

    cursor.close()
    banco.close()

    for pagamento in pagamentos:

        if pagamento["data_pagamento"]:
            pagamento["data_pagamento"] = pagamento["data_pagamento"].strftime("%d/%m/%Y")

        if pagamento["valor"] is not None:
            pagamento["valor"] = float(pagamento["valor"])

    return pagamentos


# ==========================================
# EXCLUIR PAGAMENTO
# ==========================================

@app.post("/excluir_pagamento/{pagamento_id}")


# ==========================================
# PÁGINA - EDITAR PAGAMENTO
# ==========================================

@app.get("/editar_pagamento/{pagamento_id}")
def editar_pagamento(pagamento_id: int, request: Request):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            colaborador_id,
            valor,
            data_pagamento,
            forma_pagamento,
            observacao
        FROM pagamentos
        WHERE id = %s
    """, (pagamento_id,))

    pagamento = cursor.fetchone()

    cursor.execute("""
        SELECT id, nome
        FROM colaboradores
        WHERE situacao = 'Ativo'
        ORDER BY nome
    """)

    colaboradores = cursor.fetchall()

    cursor.close()
    banco.close()

    if pagamento is None:
        return RedirectResponse(
            url="/pagamentos",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="editar_pagamento.html",
        context={
            "request": request,
            "pagamento": pagamento,
            "colaboradores": colaboradores
        }
    )


@app.post("/editar_pagamento/{pagamento_id}")
async def atualizar_pagamento(
    pagamento_id: int,
    colaborador_id: int = Form(...),
    valor: float = Form(...),
    data_pagamento: str = Form(...),
    forma_pagamento: str = Form(...),
    observacao: str = Form("")
):

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        UPDATE pagamentos
        SET
            colaborador_id = %s,
            valor = %s,
            data_pagamento = %s,
            forma_pagamento = %s,
            observacao = %s
        WHERE id = %s
    """, (
        colaborador_id,
        valor,
        data_pagamento,
        forma_pagamento,
        observacao,
        pagamento_id
    ))

    banco.commit()

    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/pagamentos",
        status_code=303
    )


# ==========================================
# PÁGINA - NOVO PRODUTO
# ==========================================
@app.get("/produtos/novo")
def novo_produto():
    return FileResponse("templates/novo_produto.html")
@app.post("/produtos/novo")
async def cadastrar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...)
):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        """
        INSERT INTO produtos (nome, descricao, preco, estoque)
        VALUES (%s, %s, %s, %s)
        """,
        (nome, descricao, preco, estoque)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return RedirectResponse(
        url="/produtos",
        status_code=303
    )
# ==========================================
# PÁGINA - EDITAR PRODUTO
# ==========================================

@app.get("/produtos/editar/{produto_id}")
def editar_produto(produto_id: int):
    return FileResponse("templates/editar_produto.html")

# ==========================================
# API - LISTAR TODOS OS PRODUTOS
# ==========================================

@app.get("/api/produtos")
def listar_produtos():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            descricao,
            preco,
            estoque
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    cursor.close()
    banco.close()

    return produtos
# ==========================================
# API - LISTAR TODOS OS PRODUTOS
# ==========================================

# ==========================================
# API - ATUALIZAR PRODUTO
# ==========================================
# ==========================================
# API - BUSCAR UM PRODUTO PELO ID
# ==========================================

@app.get("/api/produtos/{produto_id}")
def buscar_produto(produto_id: int):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            descricao,
            preco,
            estoque
        FROM produtos
        WHERE id = %s
    """, (produto_id,))

    produto = cursor.fetchone()

    cursor.close()
    banco.close()

    if not produto:
        return {"erro": "Produto não encontrado"}

    return produto


# ==========================================
# API - ATUALIZAR PRODUTO
# ==========================================
# ==========================================
# API - BUSCAR UM PRODUTO PELO ID
# ==========================================

@app.get("/api/produtos/{produto_id}")
def buscar_produto(produto_id: int):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            descricao,
            preco,
            estoque
        FROM produtos
        WHERE id = %s
    """, (produto_id,))

    produto = cursor.fetchone()

    cursor.close()
    banco.close()

    if not produto:
        return {"erro": "Produto não encontrado"}

    return produto


# ==========================================
# API - ATUALIZAR PRODUTO
# ==========================================

@app.put("/api/produtos/{produto_id}")
async def atualizar_produto(produto_id: int, request: Request):
    dados = await request.json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")
    preco = dados.get("preco")
    estoque = dados.get("estoque")

    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        """
        UPDATE produtos
        SET nome = %s,
            descricao = %s,
            preco = %s,
            estoque = %s
        WHERE id = %s
        """,
        (nome, descricao, preco, estoque, produto_id)
    )

    banco.commit()

    cursor.close()
    banco.close()

    return {
        "mensagem": "Produto atualizado com sucesso!"
    }
        
# ============================================
# API - EXCLUIR PRODUTO
# ============================================

@app.delete("/api/produtos/{produto_id}")
def excluir_produto(produto_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute(
            "DELETE FROM produtos WHERE id = %s",
            (produto_id,)
        )

        banco.commit()

        return {
            "mensagem": "Produto excluído com sucesso!"
        }

    except mysql.connector.Error as erro:

        banco.rollback()

        if erro.errno == 1451:

            return {
                "erro": "Este produto não pode ser excluído porque está vinculado a um ou mais pedidos. O histórico de vendas será preservado."
            }

        return {
            "erro": "Não foi possível excluir o produto."
        }

    finally:

        cursor.close()
        banco.close()
      
# ==========================================
# PÁGINA - NOVO PRODUTO

# ==========================================

# ==========================================
# API - CRIAR NOVO PEDIDO
# ==========================================
# ==========================================
# API - LISTAR PEDIDOS
# ==========================================

@app.get("/api/pedidos")
def listar_pedidos():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                p.id,
                c.nome AS cliente,
                p.data_pedido,
                p.valor_total,
                p.status
            FROM pedidos p
            INNER JOIN clientes c
                ON c.id = p.cliente_id
            ORDER BY p.id DESC
        """)

        pedidos = cursor.fetchall()

        for pedido in pedidos:
            if pedido["valor_total"] is not None:
                pedido["valor_total"] = float(pedido["valor_total"])

        return pedidos

    finally:
        cursor.close()
        banco.close()
@app.post("/api/pedidos")
async def criar_pedido(request: Request):

    dados = await request.json()

    cliente_id = dados.get("cliente_id")
    itens = dados.get("itens")

    if not cliente_id:
        return {
            "erro": "Selecione um cliente."
        }

    if not itens or len(itens) == 0:
        return {
            "erro": "Adicione pelo menos um produto ao pedido."
        }

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        # ------------------------------------------
        # VERIFICAR CLIENTE
        # ------------------------------------------

        cursor.execute("""
            SELECT id
            FROM clientes
            WHERE id = %s
        """, (cliente_id,))

        cliente = cursor.fetchone()

        if not cliente:
            raise Exception("Cliente não encontrado.")

        # ------------------------------------------
        # CALCULAR TOTAL E VERIFICAR ESTOQUE
        # ------------------------------------------

        valor_total = 0

        for item in itens:

            produto_id = int(item["produto_id"])
            quantidade = int(item["quantidade"])

            if quantidade < 1:
                raise Exception("Quantidade inválida.")

            cursor.execute("""
                SELECT preco, estoque
                FROM produtos
                WHERE id = %s
            """, (produto_id,))

            produto = cursor.fetchone()

            if not produto:
                raise Exception(
                    f"Produto {produto_id} não encontrado."
                )

            preco = float(produto[0])
            estoque = produto[1] or 0

            if quantidade > estoque:
                raise Exception(
                    f"Estoque insuficiente para o produto {produto_id}."
                )

            valor_total += preco * quantidade

        # ------------------------------------------
        # CADASTRAR PEDIDO
        # ------------------------------------------

        cursor.execute("""
            INSERT INTO pedidos
            (
                cliente_id,
                data_pedido,
                valor_total,
                status
            )
            VALUES
            (
                %s,
                NOW(),
                %s,
                'Recebido'
            )
        """, (
            cliente_id,
            valor_total
        ))

        pedido_id = cursor.lastrowid

        # ------------------------------------------
        # CADASTRAR ITENS E BAIXAR ESTOQUE
        # ------------------------------------------

        for item in itens:

            produto_id = int(item["produto_id"])
            quantidade = int(item["quantidade"])

            cursor.execute("""
                SELECT preco
                FROM produtos
                WHERE id = %s
            """, (produto_id,))

            produto = cursor.fetchone()

            preco = float(produto[0])

            # Cadastrar item
            cursor.execute("""
                INSERT INTO itens_pedido
                (
                    pedido_id,
                    produto_id,
                    quantidade,
                    preco_unitario
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                pedido_id,
                produto_id,
                quantidade,
                preco
            ))

            # Baixar estoque
            cursor.execute("""
                UPDATE produtos
                SET estoque = estoque + %s
                WHERE id = %s
            """, (
                quantidade,
                produto_id
            ))

            # Registrar movimentação
            cursor.execute("""
                INSERT INTO movimentacoes_estoque
                (
                    produto_id,
                    tipo,
                    quantidade,
                    observacao
                )
                VALUES
                (
                    %s,
                    'Entrada',
                    %s,
                    %s
                )
            """, (
                produto_id,
                quantidade,
                f"Pedido #{pedido_id}"
            ))

        # ------------------------------------------
        # CONFIRMAR TRANSAÇÃO
        # ------------------------------------------

        banco.commit()

        return {
            "mensagem": "Pedido criado com sucesso.",
            "pedido_id": pedido_id,
            "valor_total": valor_total,
            "status": "Recebido"
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()
# ==========================================
# PÁGINA - FINANCEIRO
# ==========================================

@app.get("/financeiro")
def pagina_financeiro():
    return FileResponse("templates/financeiro.html")

@app.get("/relatorios")
def pagina_relatorios():
    return FileResponse("templates/relatorios.html")


@app.get("/nova_saida")
def pagina_nova_saida():
    return FileResponse("templates/nova_saida.html")
# ==========================================
# API - FINANCEIRO
# ==========================================


@app.get("/api/financeiro")
def dados_financeiro(periodo: str = "todos"):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        filtro_pedidos = ""
        filtro_movimentacoes = ""

        if periodo == "hoje":
            filtro_pedidos = """
                AND DATE(data_pedido) = CURDATE()
            """
            filtro_movimentacoes = """
                AND DATE(data_movimentacao) = CURDATE()
            """

        elif periodo == "7dias":
            filtro_pedidos = """
                AND data_pedido >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            """
            filtro_movimentacoes = """
                AND data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            """

        elif periodo == "mes":
            filtro_pedidos = """
                AND YEAR(data_pedido) = YEAR(CURDATE())
                AND MONTH(data_pedido) = MONTH(CURDATE())
            """
            filtro_movimentacoes = """
                AND YEAR(data_movimentacao) = YEAR(CURDATE())
                AND MONTH(data_movimentacao) = MONTH(CURDATE())
            """

        # ==========================================
        # TOTAL DE VENDAS
        # ==========================================

        cursor.execute(f"""
            SELECT COALESCE(SUM(valor_total), 0) AS total_vendas
            FROM pedidos
            WHERE status != 'Cancelado'
            {filtro_pedidos}
        """)

        resultado = cursor.fetchone()
        total_vendas = float(resultado["total_vendas"] or 0)

        # ==========================================
        # TOTAL DE SAÍDAS
        # ==========================================

        cursor.execute(f"""
            SELECT COALESCE(SUM(valor), 0) AS total_saidas
            FROM movimentacoes_financeiras
            WHERE tipo = 'Saída'
            {filtro_movimentacoes}
        """)

        resultado = cursor.fetchone()
        total_saidas = float(resultado["total_saidas"] or 0)

        # ==========================================
        # TOTAL DE ENTRADAS
        # ==========================================

        total_entradas = total_vendas

        # ==========================================
        # SALDO
        # ==========================================

        saldo = total_entradas - total_saidas

        # ==========================================
        # MOVIMENTAÇÕES - PEDIDOS
        # ==========================================

        cursor.execute(f"""
            SELECT
                id,
                CONCAT('Pedido #', id) AS descricao,
                'Entrada' AS tipo,
                valor_total AS valor,
                data_pedido AS data
            FROM pedidos
            WHERE status != 'Cancelado'
            {filtro_pedidos}
        """)

        movimentacoes_pedidos = cursor.fetchall()

        # ==========================================
        # MOVIMENTAÇÕES - FINANCEIRAS
        # ==========================================

        cursor.execute(f"""
            SELECT
                id,
                descricao,
                tipo,
                valor,
                data_movimentacao AS data
            FROM movimentacoes_financeiras
            WHERE 1=1
            {filtro_movimentacoes}
        """)

        movimentacoes_financeiras = cursor.fetchall()

        # ==========================================
        # JUNTAR MOVIMENTAÇÕES
        # ==========================================

        movimentacoes = movimentacoes_pedidos + movimentacoes_financeiras

        # Converter valores para número
        for movimento in movimentacoes:

            if movimento["valor"] is not None:
                movimento["valor"] = float(movimento["valor"])

            if movimento["data"] is not None:
                movimento["data"] = movimento["data"].isoformat()

        # Ordenar da mais recente para a mais antiga
        movimentacoes.sort(
            key=lambda x: x["data"] or "",
            reverse=True
        )

        return {
            "total_vendas": total_vendas,
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": saldo,
            "movimentacoes": movimentacoes
        }

    finally:

        cursor.close()
        banco.close()

# ==========================================
# API - REGISTRAR SAÍDA FINANCEIRA
# ==========================================

# ==========================================
# API - REGISTRAR SAÍDA FINANCEIRA
# ==========================================

@app.post("/api/financeiro/saida")

async def registrar_saida(request: Request):

    dados = await request.json()
    descricao = dados.get("descricao")
    valor = dados.get("valor")

    if not descricao:
        return {"erro": "A descrição é obrigatória."}

    if valor is None or float(valor) <= 0:
        return {"erro": "O valor deve ser maior que zero."}

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute("""
            INSERT INTO movimentacoes_financeiras
            (descricao, tipo, valor)
            VALUES (%s, %s, %s)
        """, (
            descricao,
            "Saída",
            float(valor)
        ))

        banco.commit()

        return {
            "mensagem": "Saída registrada com sucesso!"
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()

# ==========================================
# API - REGISTRAR SAÍDA FINANCEIRA
# ==========================================

@app.post("/api/financeiro/saida")
async def registrar_saida(request: Request):

    dados = await request.json()

    descricao = dados.get("descricao")
    valor = dados.get("valor")

    if not descricao:
        return {"erro": "A descrição é obrigatória."}

    if valor is None or float(valor) <= 0:
        return {"erro": "O valor deve ser maior que zero."}

    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            INSERT INTO movimentacoes_financeiras
            (descricao, tipo, valor)
            VALUES (%s, %s, %s)
        """, (descricao, "Saída", valor))

        banco.commit()

        return {
            "mensagem": "Saída registrada com sucesso!"
        }

    except Exception as erro:
        banco.rollback()
        return {
            "erro": str(erro)
        }

    finally:
        cursor.close()
        banco.close()



# ==========================================
# API - DETALHES DE UM PEDIDO
# ==========================================

@app.get("/api/pedidos/{pedido_id}")
def detalhes_pedido(pedido_id: int):

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                i.id,
                i.pedido_id,
                i.produto_id,
                p.nome AS produto,
                i.quantidade,
                i.preco_unitario,
                (i.quantidade * i.preco_unitario) AS subtotal
            FROM itens_pedido i
            INNER JOIN produtos p
                ON p.id = i.produto_id
            WHERE i.pedido_id = %s
            ORDER BY i.id
        """, (pedido_id,))

        itens = cursor.fetchall()

        for item in itens:
            item["preco_unitario"] = float(item["preco_unitario"])
            item["subtotal"] = float(item["subtotal"])

        return itens

    finally:
        cursor.close()
        banco.close()
# ==========================================
# API - ALTERAR STATUS DO PEDIDO
# ==========================================

# ==========================================
# API - ALTERAR STATUS DO PEDIDO
# ==========================================

@app.put("/api/pedidos/{pedido_id}/status")
async def alterar_status_pedido(pedido_id: int, request: Request):

    dados = await request.json()
    novo_status = dados.get("status")

    status_permitidos = [
        "Recebido",
        "Em preparo",
        "Pronto",
        "Entregue",
        "Cancelado"
    ]

    if novo_status not in status_permitidos:
        return {
            "erro": "Status inválido"
        }

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        # ------------------------------------------
        # VERIFICAR STATUS ATUAL
        # ------------------------------------------

        cursor.execute(
            """
            SELECT status
            FROM pedidos
            WHERE id = %s
            """,
            (pedido_id,)
        )

        pedido = cursor.fetchone()

        if not pedido:
            return {
                "erro": "Pedido não encontrado."
            }

        status_atual = pedido["status"]

        # ------------------------------------------
        # CANCELAR PEDIDO
        # DEVOLVER PRODUTOS AO ESTOQUE
        # ------------------------------------------

        if novo_status == "Cancelado" and status_atual != "Cancelado":

            cursor.execute(
                """
                SELECT
                    produto_id,
                    quantidade
                FROM itens_pedido
                WHERE pedido_id = %s
                """,
                (pedido_id,)
            )

            itens = cursor.fetchall()

            for item in itens:

                produto_id = item["produto_id"]
                quantidade = item["quantidade"]

                cursor.execute(
    """
    UPDATE produtos
    SET estoque = estoque + %s
    WHERE id = %s
    """,
    (quantidade, produto_id)
)

                cursor.execute(
                    """
                    INSERT INTO movimentacoes_estoque
                    (
                        produto_id,
                        tipo,
                        quantidade,
                        observacao
                    )
                    VALUES
                    (
                        %s,
                        'Entrada',
                        %s,
                        %s
                    )
                    """,
                    (
                        produto_id,
                        quantidade,
                        f"Cancelamento do Pedido #{pedido_id}"
                    )
                )

        # ------------------------------------------
        # SE SAIR DE CANCELADO PARA OUTRO STATUS
        # RETIRAR NOVAMENTE DO ESTOQUE
        # ------------------------------------------

        elif status_atual == "Cancelado" and novo_status != "Cancelado":

            cursor.execute(
                """
                SELECT
                    produto_id,
                    quantidade
                FROM itens_pedido
                WHERE pedido_id = %s
                """,
                (pedido_id,)
            )

            itens = cursor.fetchall()

            for item in itens:

                produto_id = item["produto_id"]
                quantidade = item["quantidade"]

                cursor.execute(
                    """
                    UPDATE produtos
                    SET estoque = estoque - %s
                    WHERE id = %s
                    """,
                    (quantidade, produto_id)
                )

                cursor.execute(
                    """
                    INSERT INTO movimentacoes_estoque
                    (
                        produto_id,
                        tipo,
                        quantidade,
                        observacao
                    )
                    VALUES
                    (
                        %s,
                        'Saída',
                        %s,
                        %s
                    )
                    """,
                    (
                        produto_id,
                        quantidade,
f"Reativação do Pedido #{pedido_id}"                    )
                )

        # ------------------------------------------
        # ATUALIZAR STATUS DO PEDIDO
        # ------------------------------------------

        cursor.execute(
            """
            UPDATE pedidos
            SET status = %s
            WHERE id = %s
            """,
            (novo_status, pedido_id)
        )

        banco.commit()

        return {
            "mensagem": f"Pedido #{pedido_id} atualizado para '{novo_status}'.",
            "pedido_id": pedido_id,
            "status": novo_status
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        """
        UPDATE pedidos
        SET status = %s
        WHERE id = %s
        """,
        (novo_status, pedido_id)
    )

    banco.commit()

    cursor.close()
    banco.close()

    return {
        "mensagem": "Status atualizado com sucesso",
        "pedido_id": pedido_id,
        "status": novo_status
    }


# ==========================================
# PÁGINA - LISTA DE PEDIDOS
# ==========================================

@app.get("/pedidos")
def pagina_pedidos():
    return FileResponse("templates/pedidos.html")


# ==========================================
# PÁGINA - NOVO PEDIDO
# ==========================================

@app.get("/novo-pedido")
def pagina_novo_pedido():
    return FileResponse("templates/novo_pedido.html")


# =========================================================
#                    ESTOQUE
# =========================================================


# ==========================================
# PÁGINA - ESTOQUE
# ==========================================

@app.get("/estoque")
def pagina_estoque():
    return FileResponse("templates/estoque.html")


# ==========================================
# API - LISTAR ESTOQUE
# ==========================================

@app.get("/api/estoque")
def listar_estoque():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            descricao,
            preco,
            estoque
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    cursor.close()
    banco.close()

    for produto in produtos:

        estoque = produto["estoque"]

        if estoque is None:
            estoque = 0

        produto["estoque"] = estoque

        if estoque == 0:
            produto["situacao"] = "Sem estoque"
        elif estoque <= 5:
            produto["situacao"] = "Estoque baixo"
        else:
            produto["situacao"] = "Estoque normal"

    return produtos


# ==========================================
# API - ENTRADA DE ESTOQUE
# ==========================================

@app.post("/api/estoque/entrada")
async def entrada_estoque(request: Request):

    dados = await request.json()

    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    motivo = dados.get("motivo")

    if not produto_id or not quantidade:
        return {
            "erro": "Produto e quantidade são obrigatórios"
        }

    quantidade = int(quantidade)

    if quantidade <= 0:
        return {
            "erro": "A quantidade deve ser maior que zero"
        }

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT estoque
        FROM produtos
        WHERE id = %s
        """,
        (produto_id,)
    )

    produto = cursor.fetchone()

    if not produto:
        cursor.close()
        banco.close()

        return {
            "erro": "Produto não encontrado"
        }

    estoque_atual = produto["estoque"] or 0
    novo_estoque = estoque_atual + quantidade

    cursor.execute(
        """
        UPDATE produtos
        SET estoque = %s
        WHERE id = %s
        """,
        (novo_estoque, produto_id)
    )

    cursor.execute(
    """
    INSERT INTO movimentacoes_estoque
    (produto_id, tipo, quantidade, observacao)
    VALUES (%s, %s, %s, %s)
    """,
    (produto_id, "Entrada", quantidade, motivo)
)
    

    banco.commit()

    cursor.close()
    banco.close()

    return {
        "mensagem": "Entrada registrada com sucesso",
        "estoque_atual": novo_estoque
    }


# ==========================================
# API - SAÍDA DE ESTOQUE
# ==========================================

@app.post("/api/estoque/saida")
async def saida_estoque(request: Request):

    dados = await request.json()

    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    motivo = dados.get("motivo")

    if not produto_id or not quantidade:
        return {
            "erro": "Produto e quantidade são obrigatórios"
        }

    quantidade = int(quantidade)

    if quantidade <= 0:
        return {
            "erro": "A quantidade deve ser maior que zero"
        }

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT estoque
        FROM produtos
        WHERE id = %s
        """,
        (produto_id,)
    )

    produto = cursor.fetchone()

    if not produto:
        cursor.close()
        banco.close()

        return {
            "erro": "Produto não encontrado"
        }

    estoque_atual = produto["estoque"] or 0

    if quantidade > estoque_atual:
        cursor.close()
        banco.close()

        return {
            "erro": "Quantidade solicitada maior que o estoque disponível"
        }

    novo_estoque = estoque_atual - quantidade

    cursor.execute(
        """
        UPDATE produtos
        SET estoque = %s
        WHERE id = %s
        """,
        (novo_estoque, produto_id)
    )

    cursor.execute(
    """
    INSERT INTO movimentacoes_estoque
    (produto_id, tipo, quantidade, observacao)
    VALUES (%s, %s, %s, %s)
    """,
    (produto_id, "Saída", quantidade, motivo)
)
    banco.commit()

    cursor.close()
    banco.close()

    return {
        "mensagem": "Saída registrada com sucesso",
        "estoque_atual": novo_estoque
    }


# ==========================================
# API - HISTÓRICO DO ESTOQUE
# ==========================================

@app.get("/api/estoque/movimentacoes")
def listar_movimentacoes():

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.id,
            m.produto_id,
            p.nome AS produto,
            m.tipo,
            m.quantidade,
            m.observacao,
            m.data_movimentacao
        FROM movimentacoes_estoque m
        INNER JOIN produtos p
            ON p.id = m.produto_id
        ORDER BY m.id DESC
    """)

    movimentacoes = cursor.fetchall()

    cursor.close()
    banco.close()

    for movimento in movimentacoes:

        if movimento["data_movimentacao"]:
            movimento["data_movimentacao"] = (
                movimento["data_movimentacao"]
                .strftime("%d/%m/%Y %H:%M")
            )

    return movimentacoes
# ==========================================
# API - EXCLUIR SAÍDA FINANCEIRA
# ==========================================

@app.delete("/api/financeiro/saida/{saida_id}")
def excluir_saida(saida_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            DELETE FROM movimentacoes_financeiras
            WHERE id = %s
        """, (saida_id,))

        banco.commit()

        return {
            "mensagem": "Saída excluída com sucesso!"
        }

    except Exception as erro:
        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:
        cursor.close()
        banco.close()