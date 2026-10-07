from main import conectar_banco

banco = conectar_banco()
cursor = banco.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes_financeiras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(255) NOT NULL,
        tipo VARCHAR(20) NOT NULL,
        valor DECIMAL(10,2) NOT NULL,
        data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP
   )
""")

banco.commit()

# Adicionar a coluna observacao caso ela ainda não exista
try:
    cursor.execute("""
        ALTER TABLE movimentacoes_financeiras
        ADD COLUMN observacao VARCHAR(255) NULL
    """)
    banco.commit()
    print("Coluna observacao adicionada com sucesso!")

except Exception as erro:
    print("A coluna observacao já existe.")

cursor.close()
banco.close()

print("Tabela movimentacoes_financeiras atualizada com sucesso!")