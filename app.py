import sqlite3

def conexao_banco():
    conexao = sqlite3.connect('contatos.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conexao.commit()
    return conexao


def cadastrar_contato(nome_contato, tel_contato, email_contato):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)',
        (nome_contato, tel_contato, email_contato)
    )
    conexao.commit()
    conexao.close()


def exibir_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM contatos')
    registros = cursor.fetchall()
    conexao.close()

    if len(registros) == 0:
        print("\nNenhum contato cadastrado no momento.")
        return

    print("\n=== AGENDA DE CONTATOS ===")
    print(f"{'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30}")
    print("=" * 75)
    for item in registros:
        print(f"{item[0]:<5} | {item[1]:<20} | {item[2]:<15} | {item[3]:<30}")


def pesquisar_contato():
    termo = input("Informe o nome para pesquisa: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM contatos WHERE nome LIKE ?', (f'%{termo}%',))
    resultados = cursor.fetchall()
    conexao.close()

    if len(resultados) == 0:
        print("\nNenhum registro encontrado para essa busca.")
        return

    print("\n=== CONTATOS ENCONTRADOS ===")
    print(f"{'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30}")
    print("=" * 75)
    for item in resultados:
        print(f"{item[0]:<5} | {item[1]:<20} | {item[2]:<15} | {item[3]:<30}")


def editar_contato():
    id_busca = input("Informe o ID do contato para editar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = ?', (id_busca,))
    registro = cursor.fetchone()

    if registro is None:
        print("ID não encontrado.")
        conexao.close()
        return

    print(f"Dados atuais: {registro[1]} | {registro[2]} | {registro[3]}")
    nome_atualizado = input("Novo nome (deixe em branco para não alterar): ")
    tel_atualizado = input("Novo telefone (deixe em branco para não alterar): ")
    email_atualizado = input("Novo email (deixe em branco para não alterar): ")

    if nome_atualizado == "":
        nome_atualizado = registro[1]
    if tel_atualizado == "":
        tel_atualizado = registro[2]
    if email_atualizado == "":
        email_atualizado = registro[3]

    cursor.execute(
        'UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?',
        (nome_atualizado, tel_atualizado, email_atualizado, id_busca)
    )
    conexao.commit()
    conexao.close()
    print("Dados atualizados com sucesso!")


def remover_contato():
    id_busca = input("Informe o ID do contato que deseja remover: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = ?', (id_busca,))
    registro = cursor.fetchone()

    if registro is None:
        print("ID não encontrado.")
        conexao.close()
        return

    resposta = input(f"Confirmar remoção de '{registro[1]}'? (s/n): ")
    if resposta.lower() == 's':
        cursor.execute('DELETE FROM contatos WHERE id = ?', (id_busca,))
        conexao.commit()
        print("Contato removido com sucesso!")
    else:
        print("Operação cancelada.")

    conexao.close()


def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Novo contato")
        print("[2] Ver todos os contatos")
        print("[3] Pesquisar por nome")
        print("[4] Editar contato")
        print("[5] Remover contato")
        print("[6] Encerrar")

        escolha = input("Digite a opção desejada: ")

        if escolha == "1":
            nome_in = input("Nome: ")
            tel_in = input("Telefone: ")
            email_in = input("Email: ")
            cadastrar_contato(nome_in, tel_in, email_in)
            print("Contato salvo com sucesso!")
        elif escolha == "2":
            exibir_contatos()
        elif escolha == "3":
            pesquisar_contato()
        elif escolha == "4":
            editar_contato()
        elif escolha == "5":
            remover_contato()
        elif escolha == "6":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Escolha um número de 1 a 6.")


menu()