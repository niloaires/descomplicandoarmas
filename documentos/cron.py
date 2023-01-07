import os
import datetime
diretorioRaiz='/var/www/html/media/docs'
dataAtual=datetime.datetime.today()
ano=dataAtual.year
mes=dataAtual.month
def criarDiretorios():
    checagem= os.path.isdir('{}/{}/{}'.format(diretorioRaiz, ano, mes))
    if checagem is False:
        os.mkdir('{}/{}/{}'.format(diretorioRaiz, ano, mes),mode=0o777)