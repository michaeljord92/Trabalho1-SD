import Pyro5.api


@Pyro5.api.expose
class Usuario(object):
    nome = ""
    arquivos = []

    def __init__(self, nomeUsuario):
        self.nome = nomeUsuario
        print("Iniciado novo usuario: "+self.nome)
        
        # Registra o usuario no administrador
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        status = admin.registrarUsuario(self.nome)
        print(status)

    def getNome(self):
        print("Get Nome: "+self.nome)
        return self.nome

    def registrarUsuario(self):
        '''
        Registra este usuario no administrador
        '''
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        nomeUsuario = admin.registrarUsuario()
        self.nome = nomeUsuario

        status = "Usuario registrado"
        return status

    def listarArquivos(self):
        '''
        Lista arquivos catalogados pelo administrador
        '''
        admin = Pyro5.api.Proxy(
            "PYRONAME:admin")  # Busca referencia no servidor de nomes
        lista_de_livros = admin.listarArquivos()

        resposta = "Lista de livros:\n"
        resposta = resposta + lista_de_livros
        print(resposta)

        return lista_de_livros

    def carregarArquivo(self, nomeArquivo, nomeUsuario):
        '''
        Carrega arquivo para leitura
        '''
        usuario = Pyro5.api.Proxy("PYRONAME:"+nomeUsuario)
        conteudo = usuario.enviarArquivo(nomeArquivo)

        # print conteudo
        return conteudo

    def enviarArquivo(self, nomeArquivo):
        '''
        Retorna conteudo de arquivo local
        '''
        arquivo = open(file="./arquivos/"+nomeArquivo, mode='r')
        conteudo = arquivo.readlines()
        arquivo.close()

        return conteudo

    def gravarArquivo(self, nomeArquivo, conteudo):
        '''
        Grava arquivo localmente
        '''
        arquivo = open(file="./arquivos/"+nomeArquivo, mode='w')
        arquivo.writelines(conteudo)
        arquivo.close()

        status = "Arquivo gravado"

        print(status)
        return status

    def gravarArquivoNovo(self, nomeArquivo, conteudo):
        '''
        Grava um novo arquivo localmente e informa o administrador
        '''
        # gravar arquivo localmente
        self.gravarArquivo(nomeArquivo, conteudo)

        # registrar arquivo no administrador
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        status = admin.registrarArquivo(nomeArquivo, self.nome)

        status = "Arquivo novo gravado"
        print(status)
        return status


# Requesita um nome de usuario ao servidor
admin = Pyro5.api.Proxy("PYRONAME:admin")
nomeUsuario = admin.indicaNomeUsuario()
print("Nome indicado pelo admin: " + nomeUsuario)

# Registra usuario no servidor de nome e inicia-o
daemon = Pyro5.server.Daemon()
servidor_nome = Pyro5.api.locate_ns()
servidor_nome.register(nomeUsuario, daemon.register(
    Usuario(nomeUsuario)))

print("Usuario "+nomeUsuario+" em loop.")
daemon.requestLoop()
