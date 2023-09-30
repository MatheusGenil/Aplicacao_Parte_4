from flask import Flask as flk
from flask import request as rqt
from flask import jsonify as jsf
import mysql.connector
from datetime import timedelta, datetime

app = flk(__name__)

# Conectar ao banco de dados
conexao_banco = mysql.connector.connect(
    host="dbprojetologico.c24e1vlqhrlr.us-east-1.rds.amazonaws.com",
    user="professor",
    password="professor",
    database="Cinema"
)


#################### FILMES ##########################
# Rota para cadastrar um novo filme
@app.route('/filmes', methods=['POST'])
def cadastrar_filme():
    dados = rqt.get_json()

    Id_filme = dados.get('Id_filme')
    Titulo = dados.get('Titulo')
    Genero = dados.get('Genero')
    Classificação_Etaria = dados.get('Classificação_Etaria')
    Sinopse = dados.get('Sinopse')
    Duração = dados.get('Duração')

    cursor = conexao_banco.cursor()
    cursor.execute("INSERT INTO Cinema.Filme_2 (Id_filme, Titulo, Genero, Classificação_Etaria, Sinopse, Duração) VALUES (%s, %s, %s, %s, %s, %s)",
                   (Id_filme, Titulo, Genero, Classificação_Etaria, Sinopse, Duração))
    conexao_banco.commit()

    return jsf({"message": "Filme cadastrado com sucesso!"})

# Rota para obter a lista de filmes
@app.route('/filmes', methods=['GET'])
def obter_filmes():
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Filme_2")
    filmes = cursor.fetchall()
    
    if filmes:
        return jsf(filmes)
    else:
        return jsf({"message": "Lista Vazia"}), 404

# Rota para obter um Filme pelo Titulo
@app.route('/filmes/<string:filme_id>', methods=['GET'])
def obter_filmeTitulo(filme_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Filme_2 WHERE Titulo=%s",
                   (filme_id, ))
    filmes = cursor.fetchall()
    
    if filmes:
        return jsf(filmes)
    else:
        return jsf({"message": "Filme não encontrado"}), 404

# Rota para obter um Filme pelo ID
@app.route('/filmes/<int:filme_id>', methods=['GET'])
def obter_filmeID(filme_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Filme_2 WHERE Id_filme=%s",
                   (filme_id, ))
    filmes = cursor.fetchall()
    
    if filmes:
        return jsf(filmes)
    else:
        return jsf({"message": "Filme não encontrado"}), 404

# Rota para atualizar um filme pelo ID
@app.route('/filmes/<int:filme_id>', methods=['PUT'])
def atualizar_filme(filme_id):
 
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Filme_2 WHERE Id_filme = %s",
                   (filme_id, ))
    filmes = cursor.fetchall()

    if filmes:
        
        dados = rqt.get_json()
        Titulo = dados.get('Titulo')
        Genero = dados.get('Genero')
        Classificação_Etaria = dados.get('Classificação_Etaria')
        Sinopse = dados.get('Sinopse')
        Duração = dados.get('Duração')

        cursor = conexao_banco.cursor()
        cursor.execute("UPDATE Cinema.Filme_2 SET Titulo=%s, Genero=%s, Classificação_Etaria=%s, Sinopse=%s, Duração=%s WHERE Id_filme=%s",
                    (Titulo, Genero, Classificação_Etaria, Sinopse, Duração, filme_id))
        conexao_banco.commit()

        return jsf({"message": f"Filme {filme_id} atualizado com sucesso!"})
    else:
        return jsf({"message": "Filme não encontrado"}), 404

# Rota para deletar um filme pelo ID
@app.route('/filmes/<int:Id_filme>', methods=['DELETE'])
def deletar_filme(Id_filme):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Filme_2 WHERE Id_filme = %s",
                   (Id_filme, ))
    filmes = cursor.fetchall()

    if filmes:
        cursor = conexao_banco.cursor()
        cursor.execute("DELETE FROM Cinema.Filme_2 WHERE Id_filme=%s", (Id_filme,))
        conexao_banco.commit()

        return jsf({"message": f"Filme {Id_filme} deletado com sucesso!"})
    else:
        return jsf({"message": "Filme não encontrado"}), 404

#################### SALAS ###########################
# Rota para cadastrar uma nova Sala
@app.route('/salas', methods=['POST'])
def cadastrar_sala():
    dados = rqt.get_json()

    Numero = dados.get('Numero')
    Capacidade = dados.get('Capacidade')
    Status = dados.get('Status')

    cursor = conexao_banco.cursor()
    cursor.execute("INSERT INTO Cinema.Sala_2 (Numero, Capacidade, Status) VALUES (%s, %s, %s)",
                   (Numero, Capacidade, Status))
    conexao_banco.commit()

    return jsf({"message": "Sala cadastrada com sucesso!"})

# Rota para obter a lista de Salas
@app.route('/salas', methods=['GET'])
def obter_salas():
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT Numero, Capacidade, Status FROM Cinema.Sala_2")
    salas = cursor.fetchall()
    return jsf(salas)

# Rota para obter uma Sala pelo ID
@app.route('/salas/<int:sala_id>', methods=['GET'])
def obter_sala(sala_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT Capacidade, Status FROM Cinema.Sala_2 WHERE Numero = %s",
                   (sala_id, ))
    salas = cursor.fetchall()

    if salas:
        return jsf(salas)
    else:
        return jsf({"message": "Sala não encontrada"}), 404

# Rota para atualizar uma Sala pelo ID
@app.route('/salas/<int:sala_id>', methods=['PUT'])
def atualizar_sala(sala_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT Capacidade, Status FROM Cinema.Sala_2 WHERE Numero = %s",
                   (sala_id, ))
    salas = cursor.fetchall()

    if salas:
        dados = rqt.get_json()
        Capacidade = dados.get('Capacidade')
        Status = dados.get('Status')
        cursor.execute("UPDATE Cinema.Sala_2 SET Capacidade= %s, Status= %s WHERE Numero= %s",
                    (Capacidade, Status, sala_id))
        conexao_banco.commit()

        return jsf({"message": f"Sala {sala_id} atualizada com sucesso!"})
    else:
        return jsf({"message": "Sala não encontrada"}), 404
    
# Rota para deletar um Sala pelo ID
@app.route('/salas/<int:sala_id>', methods=['DELETE'])
def deletar_sala(sala_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT Capacidade, Status FROM Cinema.Sala_2 WHERE Numero = %s",
                   (sala_id, ))
    salas = cursor.fetchall()

    if salas:
        cursor.execute("DELETE FROM Cinema.Sala_2 WHERE Numero=%s", (sala_id,))
        conexao_banco.commit()

        return jsf({"message": f"sala {sala_id} deletada com sucesso!"})
    else:
        return jsf({"message": "Sala não encontrada"}), 404

#################### SESSÃO ###########################
# Serializar HORA
def serHora(obj):
    if isinstance(obj, timedelta):
        return str(obj)
    raise TypeError("Object of type timedelta is not JSON serializable")

# Rota para cadastrar uma nova Sessão
@app.route('/sessao', methods=['POST'])
def cadastrar_sessao():
    dados = rqt.get_json()

    Id_sessão = dados.get('Id_sessão')
    Hora = dados.get('Hora')
    Data = dados.get('Data')
    Filme_Id = dados.get('Filme_Id')
    Sala_Numero = dados.get('Sala_Numero')

    cursor = conexao_banco.cursor()
    cursor.execute("INSERT INTO Cinema.Sessão_2 (Id_sessão, Hora, Data, Filme_Id, Sala_Numero) VALUES (%s, %s, %s, %s, %s)",
                   (Id_sessão, Hora, Data, Filme_Id, Sala_Numero))
    conexao_banco.commit()

    return jsf({"message": "Sessão cadastrada com sucesso!"})

# Rota para obter a lista de Sessões
@app.route('/sessao', methods=['GET'])
def obter_sessoes():
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Sessão_2")
    sessao = cursor.fetchall()

    # Serializar timedelta usando a função de serialização personalizada
    for i in sessao:
        i['Hora'] = serHora(i['Hora'])

    return jsf(sessao)

# Rota para obter uma Sessão pelo ID
@app.route('/sessao/<int:sessao_id>', methods=['GET'])
def obter_sessao(sessao_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Sessão_2 WHERE Id_sessão =%s",
                   (sessao_id, ))
    sessao = cursor.fetchall()

    for i in sessao:
        i['Hora'] = serHora(i['Hora'])

    return jsf(sessao)

# Rota para atualizar uma Sala pelo ID
@app.route('/sessao/<int:sessao_id>', methods=['PUT'])
def atualizar_sessao(sessao_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Sessão_2 WHERE Id_sessão = %s",
                   (sessao_id, ))
    sessao = cursor.fetchall()
    for i in sessao:
        i['Hora'] = serHora(i['Hora'])

    if sessao:
        dados = rqt.get_json()
        Hora = dados.get('Hora')
        Data = dados.get('Data')
        Filme_Id = dados.get('Filme_Id')
        Sala_Numero = dados.get('Sala_Numero')


        cursor.execute("UPDATE Cinema.Sessão_2 SET Hora= %s, Data= %s, Filme_Id= %s, Sala_Numero= %s WHERE Id_sessão= %s",
                            (Hora, Data, Filme_Id, Sala_Numero, sessao_id))
        conexao_banco.commit()

        return jsf({"message": f"Sessão {sessao_id} atualizada com sucesso!"})  
    

    else:
        return jsf({"message": "Sessão não encontrada"}), 404

# Rota para deletar um Sala pelo ID
@app.route('/sessao/<int:sessao_id>', methods=['DELETE'])
def deletar_sessao(sessao_id):
    cursor = conexao_banco.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cinema.Sessão_2 WHERE Id_sessão = %s",
                   (sessao_id, ))
    sessao = cursor.fetchall()

    if sessao:
        cursor.execute("DELETE FROM Cinema.Sessão_2 WHERE Id_sessão=%s", (sessao_id,))
        conexao_banco.commit()

        return jsf({"message": f"Sessão {sessao_id} deletada com sucesso!"})
    else:
        return jsf({"message": "Sessão não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
