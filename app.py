from flask import Flask, request, url_for, render_template, session
import dataset

app = Flask(__name__)
app.secret_key = 'MINHA_CHAVE_CRIPTOGRADAFA'

@app.route('/')
def main():
    return render_template('index2.html')


@app.route('/principal')
def principal():
    try:
        with dataset.connect('sqlite:///enotas.db') as db:
            lista = db['notas'].all()

            if not len(list(lista)):
                link = (url_for('formulario_notas'))
                return f'Nenhuma nota encontrada, cadastre a primeiro em: <a href="{link}">Acessar</a>'
            else:
                lista = db['notas'].all()
                html = '<ul>'
                for item in lista:
                    html += '<li>{id} - {nome} - {nota}</li>'.format(id=item['id'], nome=item['nome'],
                                                                     nota=item['nota'])
                return 'Estou no Banco!!<br>{}'.format(html), 200

    except TypeError:
        return 'Erro ao acessar o BD!!!'


@app.route('/notas')
def formulario_notas():
    return render_template('index3.html')


@app.route('/criando', methods=['POST'])
def criar():
    if request.method == 'POST':
        session['nome'] = request.form['nome']
        session['nota'] = request.form['nota']
        with dataset.connect('sqlite:///enotas.db') as db:

            db['notas'].insert(dict(nome=session['nome'], nota=session['nota']))
        return 'Realizando operacoes CRUD', 200

    else:
        link = (url_for('formulario_notas'))
        return f'Erro ao criar, cadastre novamente em: <a href="{link}">Acessar</a>'


@app.route('/alterando', methods=['POST'])
def alterando():
    if request.method == 'POST':
        session['nome'] = request.form['nome']
        session['nota'] = request.form['nota']
        with dataset.connect('sqlite:///enotas.db') as db:
            try:
                lista = db['notas'].find_one(nome=session['nome'])
                lista['nota'] = session['nota']
                db['notas'].update(lista, ['id'])

                return 'Nota alterada com sucesso!!!', 200
            except TypeError:
                name = session['nome']
                link = (url_for('formulario_notas'))
                return f'Erro ao alterar o usuario {name}, tente novamente em: <a href="{link}">Acessar</a>'


@app.route('/excluindo', methods=['POST'])
def excluir():
    if request.method == 'POST':
        session['id'] = request.form['id']
        with dataset.connect('sqlite:///enotas.db') as db:
            lista = db['notas'].all()
            verificar = [f'{n["id"]}' for n in lista]

            if session['id'] in verificar:
                db['notas'].delete(id=session['id'])
            else:
                return 'Esse ID nao existe!!'
        return 'Excluido o dado do id {}'.format(session['id']), 200
    else:
        link = (url_for('formulario_notas'))
        return f'Erro ao excluir, cadastre novamente em: <a href="{link}">Acessar</a>'


app.run(debug=True)
