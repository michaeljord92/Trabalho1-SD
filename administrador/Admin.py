import Pyro5.api

@Pyro5.api.expose
class Admin(object):
    usuarios = []
    arquivos = {}

    def registraUsuario(self, nome):
        self.usuarios.insert(nome)
        status = "Usuario registrado: "+ nome
        return status
    
    def registraArquivo(self, nome):
        status = "Arquivo registrado: "+ nome    
        return status

    def listaArquivos(self):
        return self.arquivos
    
    def realocaArquivo(self, usuario_origem, usuario_destino):
        status = "realocado"
        return status    


daemon = Pyro5.server.Daemon()
servidor_nome = Pyro5.api.locate_ns()
servidor_nome.register("livros",daemon.register(Admin))

print("Admin em loop.")
daemon.requestLoop()