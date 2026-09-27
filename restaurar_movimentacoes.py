from main import conectar_banco
from pathlib import Path
import re

# Arquivo de backup
arquivo_backup = Path("backup_banco_pao_de_queijo.sql")

# Lê o backup
conteudo = arquivo_backup.read_text(encoding="utf-8")

# Localiza somente a seção da tabela movimentacoes_estoque
inicio = conteudo.find("-- TABELA: movimentacoes_estoque")

if inicio == -1:
    print("ERRO: tabela movimentacoes_estoque não encontrada no backup.")
    exit()

# Procura a próxima tabela depois de movimentacoes_estoque
proxima_tabela = conteudo.find("-- TABELA:", inicio + 10)

if proxima_tabela == -1:
    secao = conteudo[inicio:]
else:
    secao = conteudo[inicio:proxima_tabela]

# Pega somente os INSERTs da tabela movimentacoes_estoque
inserts = re.findall(
    r"INSERT INTO `movimentacoes_estoque`.*?;",
    secao,
    re.DOTALL
)

print(f"Registros encontrados no backup: {len(inserts)}")

if not inserts:
    print("Nenhum registro encontrado para restaurar.")
    exit()

# Conecta ao banco
banco = conectar_banco()
cursor = banco.cursor()

try:
    for sql in inserts:
        cursor.execute(sql)

    banco.commit()

    print()
    print("==========================================")
    print("HISTÓRICO RESTAURADO COM SUCESSO!")
    print(f"Registros restaurados: {len(inserts)}")
    print("==========================================")

except Exception as erro:
    banco.rollback()
    print()
    print("ERRO AO RESTAURAR:")
    print(erro)

finally:
    cursor.close()
    banco.close()