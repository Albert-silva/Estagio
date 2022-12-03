def login_validado(dados_recebidos):
    if not dados_recebidos.get('usuario'):
        return 'Usuario obrigatorio!', False

    if not dados_recebidos.get('senha'):
        return 'Senha obrigatorio!', False

    return '', True