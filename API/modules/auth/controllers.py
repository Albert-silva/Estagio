import jwt
import pytz
from datetime import datetime, timedelta
from database import mysql


def login(dados_recebido):
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * FROM sis_usuario WHERE usuario = %s", [dados_recebido['usuario']])
    usuario_selecionado = cursor.fetchone()

    if not usuario_selecionado:
        return 'Usuário não encontrado', 400

    if usuario_selecionado[3] != dados_recebido['senha']:
        return 'Senha Incorreta', 400

    data_hora_atual = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    dados = {
        'usuarioid': usuario_selecionado[0],
        'usuario': usuario_selecionado[1],
        'nome': usuario_selecionado[2],
        'iat': data_hora_atual,
        'exp': data_hora_atual + timedelta(hours=8000)
    }
    token = jwt.encode(dados, "SENHA_TOKEN", algorithm="HS256")

    cursor.close()

    return token, 200

def incluir(user_infos):
    cursor = mysql.get_db().cursor()

    try:
        usuario = user_infos['usuario']
        nome  = user_infos['nome']
        senha = user_infos['senha']
        data = datetime.now()

        cursor.execute("SELECT * FROM sis_usuario where usuario = %s", [usuario])
        usuario_selecionado = cursor.fetchone()
        if usuario_selecionado:
            return 'Usuário já existe', 400

        cursor.execute("INSERT INTO sis_usuario (usuario , nome , senha , datacriacao) VALUES (%s, %s, %s, %s)",
        [usuario, nome, senha, data])

        mysql.get_db().commit()

        cursor.close()
    
        return 'Usuario cadastrado com sucesso', 200

    except Exception:
        return 'Erro ao cadastrar o usuário', 400

def todos_usuarios(args={}):
    cursor = mysql.get_db().cursor()

    id = args.get('id')
    nome = args.get('nome')

    if id and nome:
        cursor.execute("SELECT * FROM sis_usuario WHERE usuarioid = %s and nome = %s", [id, nome])
    elif id:
        cursor.execute("SELECT * FROM sis_usuario WHERE usuarioid = %s", [id])
    elif nome:
        cursor.execute("SELECT * FROM sis_usuario WHERE nome = %s", [nome])
    else:
        cursor.execute("SELECT * FROM sis_usuario")

    users_db = cursor.fetchall()

    all_users = []
    for user in users_db:
        new_user = {
            'usuarioid': user[0],
            'usuario': user[1],
            'nome': user[2],
            'senha': "",
            'datacriacao': user[4].strftime('%d/%m/%Y'),
            'dataalteracao': user[5].strftime('%d/%m/%Y') if user[5] else None,
            'grupos': []
        }

        cursor.execute("SELECT * FROM sis_grupo_usuario INNER JOIN sis_grupo ON sis_grupo_usuario.grupoid = sis_grupo.grupoid WHERE sis_grupo_usuario.usuarioid = %s", [user[0]])
        grupos_db = cursor.fetchall()
        for grupo in grupos_db:
            new_group = {
                'grupoid': grupo[2],
                'nome': grupo[3],
                'datacriacao': grupo[4].strftime('%d/%m/%Y'),
                'dataalteracao': grupo[5].strftime('%d/%m/%Y') if grupo[5] else None
            }
            new_user['grupos'].append(new_group)

        all_users.append(new_user)

    cursor.close()

    return all_users

def um_usuario (usuarioid):
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * FROM sis_usuario WHERE usuarioid = %s", [usuarioid])

    usuario_selecionado = cursor.fetchone()

    if not usuario_selecionado :
        return 'Usuário não encontrado', 400
    
    user = {
        'usuarioid': usuario_selecionado[0],
        'usuario': usuario_selecionado[1],
        'nome': usuario_selecionado[2],
        'senha': "",
        'datacriacao': usuario_selecionado[4].strftime('%d/%m/%Y'),
        'dataalteracao': usuario_selecionado[5].strftime('%d/%m/%Y') if usuario_selecionado[5] else None,
        'grupos': []
    }

    cursor.execute("SELECT * FROM sis_grupo_usuario INNER JOIN sis_grupo ON sis_grupo_usuario.grupoid = sis_grupo.grupoid WHERE sis_grupo_usuario.usuarioid = %s", [usuario_selecionado[0]])
    grupos_db = cursor.fetchall()
    for grupo in grupos_db:
        new_group = {
            'grupoid': grupo[2],
            'nome': grupo[3],
            'datacriacao': grupo[4].strftime('%d/%m/%Y'),
            'dataalteracao': grupo[5].strftime('%d/%m/%Y') if grupo[5] else None
        }
        user['grupos'].append(new_group)

    cursor.close()

    return user, 200

def incluir_grupo(grupo_infos):
    cursor = mysql.get_db().cursor()

    nome  = grupo_infos['nome']
    data = datetime.now()

    cursor.execute("SELECT * FROM sis_grupo where nome = %s", [nome])
    grupo_selecionado = cursor.fetchone()
    if grupo_selecionado:
        return 'Grupo já existe', 400

    cursor.execute("INSERT INTO sis_grupo (nome, datacriacao) VALUES (%s, %s)", [nome, data])

    mysql.get_db().commit()

    cursor.close()

    return 'Grupo cadastrado com sucesso', 200

def todos_grupos(nome = None):
    cursor = mysql.get_db().cursor()

    if nome:
        cursor.execute("SELECT * FROM sis_grupo WHERE nome = %s", [nome])
    else:
        cursor.execute("SELECT * FROM sis_grupo")

    grupos_db = cursor.fetchall()

    all_grupos = []

    for grupo in grupos_db:
        new_grupo = {
            'grupoid': grupo[0],
            'nome': grupo[1],
            'datacriacao': grupo[2].strftime('%d/%m/%Y'),
            'dataalteracao': grupo[3].strftime('%d/%m/%Y') if grupo[3] else None
        }

        all_grupos.append(new_grupo)

    cursor.close()

    return all_grupos

def um_grupo (grupoid):
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * FROM sis_grupo WHERE grupoid = %s", [grupoid])

    grupo_selecionado = cursor.fetchone()

    if not grupo_selecionado :
        return 'Grupo não encontrado', 400
    
    grupo = {
        'grupoid': grupo_selecionado[0],
        'nome': grupo_selecionado[1],
        'datacriacao': grupo_selecionado[2].strftime('%d/%m/%Y'),
        'dataalteracao': grupo_selecionado[3].strftime('%d/%m/%Y') if grupo_selecionado[3] else None
    }
    cursor.close()

    return grupo
