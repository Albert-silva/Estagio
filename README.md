# Estagio

WebService para cadastro de usuários e grupos de usuários em Rest-API para teste de estágio Compsis

## Prerequeriments

- Python >= 3.7
- Banco de Dados MySQL >= 5.6

## Install

### Clone o projeto
```
    git clone git@github.com:Albert-silva/Estagio.git
```
```
    cd Estagio
```

### Instalar as dependências

```
    cd API/
```
```
    pip3 install -r requirements.txt
```

## Running

Acessar a pasta `bd` e execute o arquivo `codigobd.sql` no seu banco de dados.

Depois, rode a api com o comando :
```
   FLASK_APP=app.py flask run
```

Abrir http://localhost:5000/