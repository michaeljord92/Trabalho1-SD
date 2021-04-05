# Trabalho – PPD – 2020/1
## Sistema de Arquivos Distribuído
Entregar em 09/04/2021


O Sistema deverá formar uma rede Peer-2-Peer para armazenamento distribuído de dados
que serão compartilhados entre todos os usuários. Todo o sistema deverá funcionar com no
mínimo 1 e no máximo 50 usuários e com ao menos um processo administrador. Os arquivos
serão simulados por strings de no máximo 500 caracteres.
O sistema deverá ter a aplicação “Usuário” com as seguintes funções:
- Listar arquivos: Lista todos os arquivos armazenados no sistema, indicando o nome
de cada um;
- Carrega arquivo: Recebe como entrada o nome do arquivo a ser carregado e exibe
o conteúdo do arquivo na tela;
- Grava arquivo: Recebe como entrada o nome e o conteúdo do arquivo como
entrada, imprime uma resposta na tela confirmando ou não o armazenamento do
arquivo.

O sistema deverá ter um processo “administrador” que deve:
- Manter registro de usuários conectados;
- Manter registro dos arquivos armazenado e suas localizações;
- Manter o balanceamento da distribuição dos arquivos.

O sistema como um todo deve:
- Manter a escalabilidade permitindo a inclusão de novos usuários e o
balanceamento de carga (distribuindo os arquivos entre os usuários);
- Fornecer transparência de localização e mobilidade (acesso aos arquivos em outros
usuários).
Os processos deveram manter um arquivo de texto para realizar o log das operações
realizadas. O processo cliente deverá registrar:
- Novos arquivos armazenados;
- Arquivos enviados;
- Arquivos recebidos.

O processo administrador deverá registrar:
- Novos arquivos armazenados;
- Novos clientes registrados;
- Arquivos realocados (transferidos para outros clientes).

Todo o sistema elaborado deverá ser sua arquitetura documentada detalhando os processos
e suas funções no sistema, métodos implementados e as tecnologias utilizadas (RPC, RMI,
Servidor de nomes, etc).

Todos os códigos deverão ser entregues.

A documentação contará como a primeira avaliação escrita (A1) e o código como o primeiro
trabalho prático (T1).
