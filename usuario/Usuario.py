import Pyro5.api

class Usuario(object):
    nome = ""
    arquivos = []

    def registraUsuario(self):
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        status = admin.registraUsuario()
        return status

    def listaArquivos(self):
        admin = Pyro5.api.Proxy("PYRONAME:admin")  # Busca referencia no servidor de nomes
        lista_de_livros = admin.lista()

        resposta = "Lista de livros:\n"
        resposta = resposta + lista_de_livros
        
        # print resposta
        return resposta

    def carregaArquivo(self,nome):
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        conteudo = admin.carregar(nome)

        # print conteudo
        return conteudo

    def gravaArquivo(self, nome, conteudo):
        admin = Pyro5.api.Proxy("PYRONAME:admin")
        status = admin.enviar(nome,conteudo)
        
        # print status
        return status