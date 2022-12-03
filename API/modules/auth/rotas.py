from flask import Blueprint, request, jsonify
from database import mysql
from modules.auth.validacao import login_validado
from modules.auth.controllers import login, incluir, todos_usuarios, um_usuario, incluir_grupo, todos_grupos, um_grupo
from decorators import validate_token

auth_rotas = Blueprint('auth', __name__, url_prefix='/api')


@auth_rotas.route('/login', methods=["POST"])
def login_route():
    dados_recebido = request.json
    msg, status = login_validado(request.json)
    if not status:
        return msg, 400

    msg, status = login(dados_recebido)
    if status >= 400:
        return msg, status

    return {
        'menssagem': 'Bem-Vindo, login realizado com Sucesso!',
        'token': msg
    }

@auth_rotas.route('/usuario', methods=["POST"])
@validate_token
def incluir_route():
    dados_recebidos_corpo = request.json
    resultado, status = incluir(dados_recebidos_corpo)

    return {
        'messagem': resultado
    }, status

@auth_rotas.route('/usuarios', methods=["GET"])
@validate_token
def todos_usuario_route():
    args = request.args

    all_users = todos_usuarios(args)

    return jsonify (all_users)

@auth_rotas.route('/usuario/<usuarioid>', methods=["GET"])
@validate_token
def um_usuario_route(usuarioid):
    one_user, status = um_usuario(usuarioid)
    return one_user, status

@auth_rotas.route('/grupo', methods=["POST"])
@validate_token
def incluirgrupo_route():
    dados_recebidos_corpo = request.json
    resultado, status = incluir_grupo(dados_recebidos_corpo)
    return resultado, status

@auth_rotas.route('/grupo', methods=["GET"])
@validate_token
def todos_grupos_route():
    args = request.args

    all_grupos = todos_grupos(nome = args.get('nome'))
    return jsonify (all_grupos)

@auth_rotas.route('/grupo/<grupoid>', methods=["GET"])
@validate_token
def um_grupo_route(grupoid):
    one_grupo = um_grupo(grupoid)
    return one_grupo