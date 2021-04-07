import Pyro5.api

@Pyro5.api.expose
class Admin(object):
    usuarios = []
    arquivos = {}

    
    def getUsuarios(self):
        '''
        Retorna lista de usuario
        '''
        return self.usuarios

    def indicaNomeUsuario(self):
        '''
        Indica um novo nome de usuario
        '''
        nomeUsuario = "usuarioA"
        print("Nome de usuario indicado: "+nomeUsuario)
        return nomeUsuario

    def registrarUsuario(self,nomeUsuario):
        '''
        Registra usuario novo à lista de usuarios
        '''
        # self.usuarios.insert(nomeUsuario)
        self.usuarios.append(nomeUsuario)

        status = "Usuario registrado: "+ nomeUsuario
        print(status)
        
        return status
    
    def registrarArquivo(self, nomeArquivo, nomeUsuario):
        '''
        Registra um novo arquivo da rede e seu correspondente usuario
        onde está hospedado
        '''
        self.arquivos
        status = "Arquivo registrado: "+ nomeArquivo    
        print(status)
        return status

    def listarArquivos(self):
        '''
        Retorna a lista de arquivos e seus correspondente usuarios hospedeiros
        '''
        return self.arquivos
    
    def realocarArquivo(self, usuarioOrigem, usuarioDestino):
        '''
        Redistribui os aquivos entre os usuários
        '''
        status = "realocado"
        return status    


daemon = Pyro5.server.Daemon()
servidor_nome = Pyro5.api.locate_ns()
servidor_nome.register("admin",daemon.register(Admin))

print("Administrador em loop.")
daemon.requestLoop()