import Pyro5.api
import os
import datetime


@Pyro5.api.expose
class Usuario(object):
    nome = ""   # Nome de identificação de usuario no sistema
    arquivos = []   # Lista de arquivos locais
    registrado = False  # Registrado no administrador

    def __init__(self, nomeUsuario=""):

        if nomeUsuario == "":
            # Requesita um nome de identificação de usuario ao servidor
            admin = Pyro5.api.Proxy("PYRONAME:admin")
            self.nome = admin.indicaNomeUsuario()
            status = "Nome indicado pelo admin: " + self.nome
            # self.gravarLog(status)
        else:
            # Atribui nome de identifição de usuario
            self.nome = nomeUsuario

        status = "Iniciado novo usuario: "+self.nome
        # self.gravarLog(status)

        # Registra o usuario no administrador
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        resposta = admin.registrarUsuario(self.nome)
        status = "Registro no administrador: \n\tResposta do administrador: " + \
            str(resposta["mensagem"])
        # self.gravarLog(status)
        self.registrado = resposta["registro"]

    def gravarLog(self, mensagem="") -> None:
        '''
        Grava mensagem no arquivo de log.
        '''
        # Criar diretorio para gravação do arquivo
        diretorio = os.getcwd() + "/logs/"
        try:
            os.makedirs(diretorio, exist_ok=True)
        except OSError:
            status = "Erro na gravação de arquivo de log\n" + \
                "Erro na criação de diretorio\n" + "Erro: "+str(OSError)
            print(status)
            # self.gravarLog(status)

        # abrir arquivo para log
        nomeArquivo = "log_"+self.nome+".log"
        try:
            arquivo = open(file=diretorio+nomeArquivo, mode='at')
        except OSError:
            status = "Erro ao abrir arquivo para log\n"+"Erro: "+str(OSError)
            print(status)
            # self.gravarLog(status)
        else:
            data = datetime.datetime.now()
            _log = str(data)+" "+str(mensagem)
            arquivo.write(_log+"\n")
            arquivo.close()
            # print("log: "+_log)

    # def getNome(self) -> str:
    #     '''
    #     Retorna nome de usuario
    #     '''
    #     status = "Get nome: "+self.nome
    #     self.gravarLog(status)
    #     return self.nome

    # def getArquivos(self) -> list:
    #     '''
    #     Retorna lista de aquivos locais
    #     '''
    #     status = "Get arquivos: \n"+str(self.arquivos)
    #     self.gravarLog(status)
    #     return self.arquivos

    def listarArquivos(self) -> str:
        '''
        Lista arquivos catalogados pelo administrador
        '''
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        listaArquivos = admin.listarArquivos()

        print("Lista de livros: \n" + str(listaArquivos.keys()))
        
        mensagem = "Lista de livros lidas do administrador."
        # self.gravarLog(mensagem)

        return mensagem

    def carregarArquivo(self, nomeArquivo) -> dict:
        '''
        Carrega conteudo de arquivo e exibe-o.
        '''
        # Busca lista de livros e seus correspodentes
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        lista_de_livros = admin.listarArquivos()

        # Requisita ao correspondente o conteudo do arquivo
        nomeUsuario = lista_de_livros[nomeArquivo]
        usuario = Pyro5.api.Proxy("PYRONAME:"+nomeUsuario)
        resposta = usuario.enviarArquivo(nomeArquivo)
        if resposta["status"]:
            print(resposta["conteudo"])
            mensagem = "Arquivo "+str(nomeArquivo) + \
                " lido do usuario "+str(nomeUsuario)
            self.gravarLog(mensagem)
            resposta = {"status": True, "mensagem": mensagem}
        else:
            mensagem = "Arquivo "+str(nomeArquivo) + \
                " não lido do usuario "+str(nomeUsuario)
            # self.gravarLog(mensagem)
            resposta = {"status": False, "mensagem": mensagem}

        return resposta

    def enviarArquivo(self, nomeArquivo) -> dict:
        '''
        Retorna conteudo de arquivo local.

        Retorna um "dict" com "status" de leitura e um "conteudo" 
        com a leitura do arquivo local ou com a mensagem de erro.
        '''
        diretorio = os.getcwd() + "/arquivos/"+self.nome+"/"
        try:
            arquivo = open(file=diretorio+nomeArquivo, mode='r')
        except IOError:
            mensagem = "Erro no envio de arquivo\n"+"Erro: "+str(IOError)
            resposta = {"status": False, "conteudo": mensagem}
            # self.gravarLog(mensagem)
        else:
            conteudo = arquivo.readlines()
            arquivo.close()
            resposta = {"status": True, "conteudo": conteudo}
            status = "Arquivo "+str(nomeArquivo)+" lido e conteudo enviado."
            self.gravarLog(status)

        return resposta

    def gravarArquivo(self, nomeArquivo="", conteudo="") -> dict:
        '''
        Grava arquivo localmente

        Retorna "dict" com "status" de gravação e com "mensagem".
        '''
        # Criar diretorio para gravação do arquivo
        diretorio = os.getcwd() + "/arquivos/"+self.nome+"/"
        try:
            os.makedirs(diretorio, exist_ok=True)
        except OSError:
            mensagem = "Erro na gravação de arquivo\n" + \
                "Erro na criação de diretorio\n" + "Erro: "+str(OSError)
            resposta = {"status": False, "mensagem": mensagem}
            # self.gravarLog(mensagem)

        # Abrir arquivo e gravar conteudo
        try:
            arquivo = open(file=diretorio+nomeArquivo, mode='w')
        except IOError:
            mensagem = "Erro na gravação de arquivo\n" + "Erro: "+str(IOError)
            # self.gravarLog(mensagem)
            resposta = {"status": False, "mensagem": mensagem}
        else:
            arquivo.writelines(conteudo)
            arquivo.close()
            self.arquivos.append(nomeArquivo)

            mensagem = "Arquivo "+nomeArquivo + " gravado"
            # self.gravarLog(mensagem)
            resposta = {"status": True, "mensagem": mensagem}

        print(mensagem["mensagem"])
        return resposta

    def gravarArquivoNovo(self, nomeArquivo="", conteudo="") -> dict:
        '''
        Grava um novo arquivo localmente e informa o administrador
        '''
        # gravar arquivo localmente
        resposta = self.gravarArquivo(nomeArquivo, conteudo)
        if resposta["status"]:
            # registrar arquivo no administrador
            admin = Pyro5.api.Proxy("PYRONAME:admin")
            resposta = admin.registrarArquivo(nomeArquivo, self.nome)
            if resposta["status"]:
                mensagem = "Arquivo novo " + \
                    str(nomeArquivo)+" gravado localmente e registrado no administrador."
                self.gravarLog(mensagem)
                resposta = {"status": True, "mensagem": mensagem}
            else:
                mensagem = "Arquivo novo " + \
                    str(nomeArquivo) + \
                    " gravado localmente mas não registrado no administrador."
                # self.gravarLog(mensagem)
                resposta = {"status": False, "mensagem": mensagem}
        else:
            mensagem = "Arquivo novo " + \
                str(nomeArquivo)+" não gravado localmente."
            # self.gravarLog(mensagem)
            resposta = {"status": False, "mensagem": mensagem}

        return resposta

    def excluirArquivo(self, nomeArquivo="") -> dict:
        '''
        Excluir um arquivo localmente
        '''
        # verifica existencia do arquivo
        diretorio = os.getcwd() + "/arquivos/"+self.nome+"/"
        if os.path.exists(diretorio+nomeArquivo):
            try:
                # exclui o arquivo local
                os.remove(diretorio+nomeArquivo)
            except OSError:
                mensagem = "Erro na exclusão do arquivo " + \
                    str(nomeArquivo) + "\n" + "Erro: "+str(OSError)
                # self.gravarLog(mensagem)
                resposta = {"status": False, "mensagem": mensagem}
            else:
                self.arquivos.remove(nomeArquivo)
                mensagem = "Arquivo excluído: "+str(nomeArquivo)
                # self.gravarLog(mensagem)
                resposta = {"status": True, "mensagem": mensagem}
        else:
            mensagem = "Arquivo "+str(nomeArquivo)+" não encontrado."
            # self.gravarLog(mensagem)
            resposta = {"status": False, "mensagem": mensagem}

        return resposta


# Instancia usuario
usuario = Usuario()

if usuario.registrado:
    # Registra usuario no servidor de nomes
    daemon = Pyro5.server.Daemon()
    servidor_nome = Pyro5.api.locate_ns()
    servidor_nome.register(usuario.nome, daemon.register(usuario))
    status = "Usuario "+usuario.nome+" registrado no servidor de nomes."
    # usuario.gravarLog(status)

    status = "Usuario "+usuario.nome+" em loop."
    # usuario.gravarLog(status)
    daemon.requestLoop()
else:
    status = "Usuario não registrado no administrador."
    # usuario.gravarLog(status)
