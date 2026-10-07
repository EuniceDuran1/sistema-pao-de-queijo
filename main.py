from fastapi import FastAPI, Form, Request, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

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
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
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
# =========================================
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
                AND data_pedido >= DATE_SUB(NOW(), INTERVAL 7 DAY)
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
            LEFT JOIN clientes c
                ON p.cliente_id = c.id
            ORDER BY p.id DESC
        """)

        pedidos = cursor.fetchall()

        return pedidos

    except Exception as e:
        return {"erro": str(e)}

    finally:
        cursor.close()
        banco.close()
# ==========================================
# PÁGINA DE PEDIDOS
# ==========================================

@app.get("/pedidos")
def pagina_pedidos():
    return FileResponse("templates/pedidos.html")


# ==========================================
# PÁGINA DE ESTOQUE
# ==========================================

@app.get("/estoque")
def pagina_estoque():
    return FileResponse("templates/estoque.html")

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
# API - DASHBOARD / RELATÓRIO DE VENDAS
# ==========================================

@app.get("/api/dashboard")
def dados_dashboard(periodo: str = "todos"):

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute("SELECT COUNT(*) FROM produtos")
        total_produtos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]

        filtro_data = ""

        if periodo == "hoje":
            filtro_data = """
                AND DATE(data_pedido) = CURDATE()
            """

        elif periodo == "7dias":
            filtro_data = """
                AND data_pedido >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """

        elif periodo == "mes":
            filtro_data = """
                AND YEAR(data_pedido) = YEAR(CURDATE())
                AND MONTH(data_pedido) = MONTH(CURDATE())
            """

        # Número de pedidos
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM pedidos
            WHERE status != 'Cancelado'
            {filtro_data}
        """)

        total_pedidos = cursor.fetchone()[0]

        # Total vendido
        cursor.execute(f"""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM pedidos
            WHERE status != 'Cancelado'
            {filtro_data}
        """)

        total_vendas = cursor.fetchone()[0]

        return {
            "total_produtos": total_produtos,
            "total_pedidos": total_pedidos,
            "total_clientes": total_clientes,
            "total_vendas": float(total_vendas or 0)
        }

    except Exception as erro:

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()
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
def excluir_pagamento(pagamento_id: int):
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM pagamentos WHERE id = %s",
        (pagamento_id,)
    )

    banco.commit()

    cursor.close()
    banco.close()

    return {"sucesso": True}

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
    estoque: int = Form(...),
    imagem: UploadFile = File(None)
):

    banco = conectar_banco()
    cursor = banco.cursor()

    caminho_imagem = None

    # ==========================================
    # SALVAR IMAGEM
    # ==========================================

    if imagem and imagem.filename:

        extensoes_permitidas = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }

        extensao = os.path.splitext(
            imagem.filename
        )[1].lower()

        if extensao not in extensoes_permitidas:

            cursor.close()
            banco.close()

            return RedirectResponse(
                url="/produtos/novo",
                status_code=303
            )

        # Garante que a pasta exista
        os.makedirs(
            "static/img",
            exist_ok=True
        )

        # Nome único para a imagem
        nome_arquivo = (
            f"produto_{uuid.uuid4().hex}{extensao}"
        )

        caminho_arquivo = os.path.join(
            "static/img",
            nome_arquivo
        )

        # Salva a imagem
        conteudo = await imagem.read()

        with open(
            caminho_arquivo,
            "wb"
        ) as arquivo:

            arquivo.write(conteudo)

        # Caminho salvo no banco
        caminho_imagem = (
            f"/static/img/{nome_arquivo}"
        )

    # ==========================================
    # CADASTRAR PRODUTO
    # ==========================================

    cursor.execute(
        """
        INSERT INTO produtos
        (nome, descricao, preco, estoque, imagem)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            nome,
            descricao,
            preco,
            estoque,
            caminho_imagem
        )
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
    return FileResponse(
        "templates/editar_produto.html"
    )

# ==========================================
# API - EDITAR PRODUTO
# ==========================================

@app.put("/api/produtos/{produto_id}")
async def atualizar_produto(
    produto_id: int,
    request: Request
):

    dados = await request.json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")
    preco = dados.get("preco")
    estoque = dados.get("estoque")

    if not nome or preco is None or estoque is None:
        return {
            "erro": "Nome, preço e estoque são obrigatórios"
        }

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute(
            """
            UPDATE produtos
            SET
                nome = %s,
                descricao = %s,
                preco = %s,
                estoque = %s
            WHERE id = %s
            """,
            (
                nome,
                descricao,
                preco,
                estoque,
                produto_id
            )
        )

        banco.commit()

        if cursor.rowcount == 0:
            return {
                "erro": "Produto não encontrado"
            }

        return {
            "mensagem": "Produto atualizado com sucesso"
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
            estoque,
            imagem
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

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

    cursor.close()
    banco.close()

    return produtos

# ==========================================
# API - BUSCAR UM PRODUTO PELO ID
# ==========================================

@app.get("/api/produtos/{produto_id}")
def buscar_produto(produto_id: int):

    banco = conectar_banco()

    cursor = banco.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            nome,
            descricao,
            preco,
            estoque,
            imagem
        FROM produtos
        WHERE id = %s
        """,
        (produto_id,)
    )

    produto = cursor.fetchone()

    cursor.close()
    banco.close()

    if not produto:
        return {
            "erro": "Produto não encontrado"
        }

    return produto
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

    # Validação dos campos
    if not produto_id or not quantidade:
        return {
            "erro": "Produto e quantidade são obrigatórios"
        }

    try:
        quantidade = int(quantidade)
    except (ValueError, TypeError):
        return {
            "erro": "A quantidade deve ser um número válido"
        }

    if quantidade <= 0:
        return {
            "erro": "A quantidade deve ser maior que zero"
        }

    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:

        # Busca o produto
        cursor.execute(
            """
            SELECT id, nome, estoque
            FROM produtos
            WHERE id = %s
            """,
            (produto_id,)
        )

        produto = cursor.fetchone()

        if not produto:
            return {
                "erro": "Produto não encontrado"
            }

        estoque_atual = produto["estoque"] or 0

        # Verifica se existe estoque suficiente
        if quantidade > estoque_atual:
            return {
                "erro": "Quantidade solicitada maior que o estoque disponível"
            }

        # Calcula o novo estoque
        novo_estoque = estoque_atual - quantidade

        # Atualiza o estoque
        cursor.execute(
            """
            UPDATE produtos
            SET estoque = %s
            WHERE id = %s
            """,
            (novo_estoque, produto_id)
        )

        # Registra a movimentação
        cursor.execute(
            """
            INSERT INTO movimentacoes_estoque
            (produto_id, tipo, quantidade, observacao)
            VALUES (%s, %s, %s, %s)
            """,
            (
                produto_id,
                "Saída",
                quantidade,
                motivo or "-"
            )
        )

        banco.commit()

        return {
            "mensagem": "Saída registrada com sucesso",
            "estoque_anterior": estoque_atual,
            "estoque_atual": novo_estoque
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": f"Erro ao registrar saída: {str(erro)}"
        }

    finally:

        cursor.close()
        banco.close()

        
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

@app.delete("/api/estoque/movimentacoes")
def limpar_movimentacoes():

    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        cursor.execute("""
            DELETE FROM movimentacoes_estoque
        """)

        banco.commit()

        return {
            "mensagem": "Histórico de movimentações limpo com sucesso"
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": f"Erro ao limpar histórico: {str(erro)}"
        }

    finally:
        cursor.close()
        banco.close()

# ==========================================
# API - CADASTRAR SAÍDA FINANCEIRA
# ==========================================

class SaidaFinanceira(BaseModel):
    descricao: str
    valor: float
    observacao: str = ""


@app.post("/api/financeiro/saida")
async def cadastrar_saida_financeira(dados: SaidaFinanceira):

    descricao = dados.descricao
    valor = dados.valor
    observacao = dados.observacao

    if not descricao or valor is None:
        return {
            "erro": "Descrição e valor são obrigatórios"
        }

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return {
            "erro": "O valor deve ser um número válido"
        }

    if valor <= 0:
        return {
            "erro": "O valor deve ser maior que zero"
        }

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO movimentacoes_financeiras
            (descricao, tipo, valor, observacao)
            VALUES (%s, %s, %s, %s)
            """,
            (
                descricao,
                "Saída",
                valor,
                observacao or ""
            )
        )

        banco.commit()

        return {
            "mensagem": "Saída registrada com sucesso"
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": f"Erro ao registrar saída: {str(erro)}"
        }

    finally:

        cursor.close()
        banco.close()

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


# ==========================================
# API - EXCLUIR ENTRADA FINANCEIRA
# ==========================================

@app.delete("/api/financeiro/entrada/{entrada_id}")
def excluir_entrada(entrada_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        cursor.execute("""
            DELETE FROM movimentacoes_financeiras
            WHERE id = %s
        """, (entrada_id,))

        banco.commit()

        return {
            "mensagem": "Entrada excluída com sucesso!"
        }

    except Exception as erro:

        banco.rollback()

        return {
            "erro": str(erro)
        }

    finally:

        cursor.close()
        banco.close()

# ============================================================
# API - CONSULTAR DADOS FINANCEIROS
# ============================================================

@app.get("/api/financeiro")
def obter_financeiro():
    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        
        # ----------------------------------------------------
        # TOTAL DE VENDAS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM pedidos
            WHERE status != 'Cancelado'
        """)

        total_vendas = cursor.fetchone()[0] or 0

        # ----------------------------------------------------
        # TOTAL DE ENTRADAS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM movimentacoes_financeiras
            WHERE tipo = 'Entrada'
        """)

        entradas_financeiras = cursor.fetchone()[0] or 0
        total_entradas = total_vendas + entradas_financeiras
        # ----------------------------------------------------
        # TOTAL DE SAÍDAS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM movimentacoes_financeiras
            WHERE tipo = 'Saída'
        """)

        total_saidas = cursor.fetchone()[0] or 0

        # ----------------------------------------------------
        # SALDO
        # ----------------------------------------------------
        saldo = total_entradas - total_saidas

        # ----------------------------------------------------
        # MOVIMENTAÇÕES FINANCEIRAS
        # ----------------------------------------------------
        cursor.execute("""
            SELECT
                id,
                descricao,
                tipo,
                valor,
                data_movimentacao
            FROM movimentacoes_financeiras
            ORDER BY data_movimentacao DESC, id DESC
        """)

        movimentacoes = cursor.fetchall()

        lista_movimentacoes = []

        for movimento in movimentacoes:
            lista_movimentacoes.append({
                "id": movimento[0],
                "descricao": movimento[1],
                "tipo": movimento[2],
                "valor": float(movimento[3]),
                "data": movimento[4]
            })

        return {
            "total_vendas": float(total_vendas),
            "total_entradas": float(total_entradas),
            "total_saidas": float(total_saidas),
            "saldo": float(saldo),
            "movimentacoes": lista_movimentacoes
        }

    finally:
        cursor.close()
        banco.close()
# ==========================================
# IMPRIMIR PEDIDO
# ==========================================

@app.get("/imprimir_pedido/{pedido_id}", response_class=HTMLResponse)
async def imprimir_pedido(pedido_id: int):

    banco = conectar_banco()
    cursor = banco.cursor()

    try:

        # Buscar dados do pedido
        cursor.execute("""
            SELECT
                p.id,
                p.data_pedido,
                p.valor_total,
                p.status,
                c.nome,
                c.telefone,
                c.endereco
            FROM pedidos p
            INNER JOIN clientes c
                ON p.cliente_id = c.id
            WHERE p.id = %s
        """, (pedido_id,))

        pedido = cursor.fetchone()

        if not pedido:
            return HTMLResponse(
                "<h2>Pedido não encontrado.</h2>",
                status_code=404
            )

        # Buscar itens do pedido
        cursor.execute("""
            SELECT
                pr.nome,
                ip.quantidade,
                ip.preco_unitario,
                (ip.quantidade * ip.preco_unitario) AS subtotal
            FROM itens_pedido ip
            INNER JOIN produtos pr
                ON ip.produto_id = pr.id
            WHERE ip.pedido_id = %s
        """, (pedido_id,))

        itens = cursor.fetchall()

        # Dados do pedido
        id_pedido = pedido[0]
        data_pedido = pedido[1]
        valor_total = float(pedido[2])
        status = pedido[3]
        cliente = pedido[4]
        telefone = pedido[5]
        endereco = pedido[6]

        # Montar tabela de itens
        itens_html = ""

        for item in itens:

            nome_produto = item[0]
            quantidade = item[1]
            preco_unitario = float(item[2])
            subtotal = float(item[3])

            itens_html += f"""
                <tr>
                    <td>{nome_produto}</td>
                    <td>{quantidade}</td>
                    <td>R$ {preco_unitario:.2f}</td>
                    <td>R$ {subtotal:.2f}</td>
                </tr>
            """

        # Página de impressão
        html = f"""
        <!DOCTYPE html>

        <html lang="pt-BR">

        <head>

            <meta charset="UTF-8">

            <title>Pedido #{id_pedido}</title>

                        <style>
                * {{
                    box-sizing: border-box;
                }}

                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                    font-size: 14px;
                }}

                .cabecalho {{
                    text-align: center;
                    border-bottom: 2px solid #8B4A00;
                    padding-bottom: 10px;
                    margin-bottom: 15px;
                }}

                .cabecalho h1 {{
                    margin: 0;
                    color: #8B4A00;
                    font-size: 24px;
                }}

                .cabecalho h2 {{
                    margin: 6px 0 0;
                    font-size: 18px;
                }}

                .informacoes {{
                    margin-bottom: 15px;
                }}

                .informacoes p {{
                    margin: 4px 0;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 12px;
                }}

                th {{
                    background: #8B4A00;
                    color: white;
                    padding: 7px;
                    text-align: left;
                    font-size: 13px;
                }}

                td {{
                    padding: 7px;
                    border-bottom: 1px solid #ddd;
                    font-size: 13px;
                }}

                .total {{
                    text-align: right;
                    margin-top: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #8B4A00;
                }}

                .botao-imprimir {{
                    margin-top: 25px;
                    padding: 12px 25px;
                    background: #8B4A00;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}

                @media print {{
    @page {{
        size: A4 portrait;
        margin: 8mm;
    }}

    body {{
        margin: 0;
        padding: 0;
        font-size: 11px;
        color: #222;
    }}

    .cabecalho {{
        padding-bottom: 8px;
        margin-bottom: 10px;
    }}

    .cabecalho h1 {{
        font-size: 20px;
        margin: 0;
    }}

    .cabecalho h2 {{
        font-size: 15px;
        margin: 4px 0 0 0;
    }}

    .informacoes {{
        margin-bottom: 10px;
    }}

    .informacoes p {{
        margin: 3px 0;
    }}

    table {{
        margin-top: 10px;
    }}

    th {{
        padding: 6px;
        font-size: 11px;
    }}

    td {{
        padding: 6px;
        font-size: 11px;
    }}

    .total {{
        margin-top: 10px;
        font-size: 15px;
    }}

    
}}
                    .cabecalho {{
                        padding-bottom: 8px;
                        margin-bottom: 12px;
                    }}

                    .cabecalho h1 {{
                        font-size: 20px;
                    }}

                    .cabecalho h2 {{
                        font-size: 16px;
                    }}

                    .informacoes {{
                        margin-bottom: 10px;
                    }}

                    .informacoes p {{
                        margin: 3px 0;
                    }}

                    table {{
                        margin-top: 8px;
                    }}

                    th,
                    td {{
                        padding: 5px;
                        font-size: 11px;
                    }}

                    .total {{
                        margin-top: 10px;
                        font-size: 16px;
                    }}
@media print {{
    @page {{
        size: A4 portrait;
        margin: 10mm;
    }}

    body {{
        margin: 0;
        font-size: 12px;
    }}

    .botao-imprimir {{
        display: none !important;
    }}
}}
            </style>
        </head>

        <body>

            <div class="cabecalho">

                <h1>🥖 Sistema Pão de Queijo</h1>

                <h2>Pedido #{id_pedido}</h2>

            </div>

            <div class="informacoes">

                <p>
                    <strong>Cliente:</strong>
                    {cliente}
                </p>

                <p>
                    <strong>Telefone:</strong>
                    {telefone or "-"}
                </p>

                <p>
                    <strong>Endereço:</strong>
                    {endereco or "-"}
                </p>

                <p>
                    <strong>Data do pedido:</strong>
                    {data_pedido}
                </p>

                <p>
                    <strong>Status:</strong>
                    {status}
                </p>

            </div>

            <table>

                <thead>

                    <tr>
                        <th>Produto</th>
                        <th>Quantidade</th>
                        <th>Preço unitário</th>
                        <th>Subtotal</th>
                    </tr>

                </thead>

                <tbody>

                    {itens_html}

                </tbody>

            </table>

            <div class="total">

    Total do pedido:

    R$ {valor_total:.2f}

</div>

<button class="botao-imprimir" onclick="window.print()">
    🖨️ Imprimir
</button>

</body>
</html>
"""
        return HTMLResponse(content=html)

    except Exception as erro:

        print("Erro ao imprimir pedido:", erro)

        return HTMLResponse(
            f"<h2>Erro ao carregar pedido: {erro}</h2>",
            status_code=500
        )

    finally:

        cursor.close()
        banco.close()


# ==========================================
# PÁGINA - FINANCEIRO
# ==========================================

@app.get("/financeiro")
def pagina_financeiro():
    return FileResponse("templates/financeiro.html")


# ==========================================
# PÁGINA - RELATÓRIOS
# ==========================================

@app.get("/relatorios")
def pagina_relatorios():
    return FileResponse("templates/relatorios.html")


# ==========================================
# PÁGINA - NOVA SAÍDA FINANCEIRA
# ==========================================

@app.get("/nova_saida")
def pagina_nova_saida():
    return FileResponse("templates/nova_saida.html")

# ==========================================
# PÁGINA - NOVA ENTRADA FINANCEIRA
# ==========================================

@app.get("/nova_entrada")
def pagina_nova_entrada():
    return FileResponse("templates/nova_entrada.html")