import Pyro5.api
import os
import datetime


@Pyro5.api.expose
class Admin(object):
    nome = "admin"
    usuarios = []
    arquivos = {}
    limiteUsuarios = 50

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

    def getUsuarios(self) -> list:
        '''
        Retorna lista de usuario
        '''
        return self.usuarios

    def indicaNomeUsuario(self) -> str:
        '''
        Indica um novo nome de usuario
        '''
        nomeUsuario = "usuario"+str(len(self.usuarios))
        # print("Nome de usuario indicado: "+nomeUsuario)
        return nomeUsuario

    def registrarUsuario(self, nomeUsuario="") -> dict:
        '''
        Registra usuario novo à lista de usuarios

        Retorna um "dict" com "mensagem" do tipo "string" e com "registro" do tipo "bool". 
        '''
        # verificar limite de usuarios
        if len(self.usuarios) >= self.limiteUsuarios:
            status = {"mensagem": "Usuario não registrado. Limite de " +
                      str(self.limiteUsuarios) + " usuarios excedidos", "registro": False}
            return status

        # registra o usuario
        self.usuarios.append(nomeUsuario)
        mensagem = "Usuario registrado: " + str(nomeUsuario)
        status = {"mensagem": mensagem, "registro": True}
        self.gravarLog(mensagem)

        return status

    def registrarArquivo(self, nomeArquivo, nomeUsuario) -> dict:
        '''
        Registra um novo arquivo da rede e seu correspondente usuario
        onde está hospedado
        '''
        self.arquivos[nomeArquivo] = nomeUsuario
        mensagem = "Arquivo registrado " + nomeArquivo+" do usuario " + nomeUsuario
        resposta = {"status": True, "mensagem": mensagem}

        self.gravarLog(mensagem)
        # print(mensagem)
        return resposta

    def listarArquivos(self) -> dict:
        '''
        Retorna a lista de arquivos e seus 
        correspondente usuarios hospedeiros
        '''
        return self.arquivos

    def realocarArquivo(self, nomeArquivo, usuarioOrigem, usuarioDestino) -> dict:
        '''
        Realoca arquivo entre os usuários
        '''
        origem = Pyro5.api.Proxy("PYRONAME:"+usuarioOrigem)
        destino = Pyro5.api.Proxy("PYRONAME:"+usuarioDestino)

        # manda usuario destino gravar uma copia
        resposta = destino.gravarArquivo(
            nomeArquivo, origem.enviarArquivo(nomeArquivo))

        if resposta["status"]:
            # manda usuario origem excluir
            resposta = origem.excluirArquivo(nomeArquivo)
            if resposta["status"]:
                # atualiza a lista de arquivos e seus correspodentes usuario
                self.arquivos[nomeArquivo] = usuarioDestino
                mensagem = "Arquivo realocado do usuario " + \
                    str(usuarioOrigem)+" para o "+str(usuarioDestino)
                self.gravarLog(mensagem)
                resposta = {"status":True,"mensagem":mensagem}
            else:
                mensagem = "Arquivo não removido do usuario origem."
                resposta = {"status":False,"mensagem":mensagem}
        else:
            mensagem = "Arquivo não gravado pelo usuario destino."
            resposta = {"status":False,"mensagem":mensagem}

        
        return resposta

    def balancearArquivos(self):
        '''
        Identifica desbalanceamento de arquivos entre os usuarios 
        e realiza balanceamento.
        '''
        # falta aqui implementar algum algoritimo de balanceamento


# Registra administrador no servidor de nomes
daemon = Pyro5.server.Daemon()

servidor_nome = Pyro5.api.locate_ns()
servidor_nome.register("admin", daemon.register(Admin))

print("Administrador em loop.")
daemon.requestLoop()
