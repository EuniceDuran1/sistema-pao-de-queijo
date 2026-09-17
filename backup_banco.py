from main import conectar_banco
from decimal import Decimal
from datetime import date, datetime
from pathlib import Path


def formatar_valor(valor):
    if valor is None:
        return "NULL"

    if isinstance(valor, str):
        valor = valor.replace("\\", "\\\\")
        valor = valor.replace("'", "''")
        return f"'{valor}'"

    if isinstance(valor, (datetime, date)):
        return f"'{valor}'"

    if isinstance(valor, Decimal):
        return str(valor)

    if isinstance(valor, bool):
        return "1" if valor else "0"

    return str(valor)


banco = conectar_banco()
cursor = banco.cursor()

arquivo = Path("backup_banco_pao_de_queijo.sql")

with open(arquivo, "w", encoding="utf-8") as backup:

    cursor.execute("SELECT DATABASE()")
    banco_nome = cursor.fetchone()[0]

    backup.write(f"-- BACKUP DO BANCO: {banco_nome}\n")
    backup.write("-- Sistema Pão de Queijo\n\n")
    backup.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

    cursor.execute("SHOW FULL TABLES")
    objetos = cursor.fetchall()

    for nome, tipo in objetos:

        if tipo == "VIEW":
            cursor.execute(f"SHOW CREATE VIEW `{nome}`")
            resultado = cursor.fetchone()

            backup.write(f"\n-- VIEW: {nome}\n")
            backup.write(f"DROP VIEW IF EXISTS `{nome}`;\n")
            backup.write(resultado[1] + ";\n")

        else:
            cursor.execute(f"SHOW CREATE TABLE `{nome}`")
            resultado = cursor.fetchone()

            backup.write(f"\n-- TABELA: {nome}\n")
            backup.write(f"DROP TABLE IF EXISTS `{nome}`;\n")
            backup.write(resultado[1] + ";\n\n")

            cursor.execute(f"SELECT * FROM `{nome}`")
            registros = cursor.fetchall()

            colunas = [desc[0] for desc in cursor.description]

            for registro in registros:
                valores = ", ".join(
                    formatar_valor(valor)
                    for valor in registro
                )

                backup.write(
                    f"INSERT INTO `{nome}` "
                    f"(`{'`, `'.join(colunas)}`) "
                    f"VALUES ({valores});\n"
                )

            backup.write("\n")

    backup.write("SET FOREIGN_KEY_CHECKS = 1;\n")

cursor.close()
banco.close()

print()
print("========================================")
print("BACKUP REALIZADO COM SUCESSO!")
print("========================================")
print(f"Arquivo: {arquivo.resolve()}")
print()