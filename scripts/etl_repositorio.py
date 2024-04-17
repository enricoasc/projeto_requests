from dados_repo import Dados_Repositorios as dp

## Informações Principais de login e Busca
dados_acesso = {
    'busca_repositorio_login' : 'microsoft',
    'token_acesso_conta' : 'PEGAR NO GIT ',
    'nome_usuario_conta' :  'enricoasc',
    'repositorio_destino' : 'base_dados_git'
}
new_repo = dp(dados_acesso)

# Extract 
new_repo.busca_repositorios()


# Transform
new_repo.converte_csv()


# Load
new_repo.envia_csv(dados_acesso['repositorio_destino'])