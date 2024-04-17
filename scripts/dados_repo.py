import requests
import pandas as pd
import base64

class Dados_Repositorios:

    def __init__(self, dados):   

        self.__api_base_url = 'https://api.github.com'
        self.__owner = dados['busca_repositorio_login']
        self.__access_token = dados['token_acesso_conta']
        self.__username = dados['nome_usuario_conta']

        self.__headers= {'Authorization': 'Bearer '+ self.__access_token,
                        'X-GitHub-Api-Version' : '2022-11-28'}
        self.__dados_amz = pd.DataFrame()
        self.__caminho_arquivo = ''

##### Interface usuario

    def busca_repositorios(self):
        self.__get_repository()
    
    def converte_csv(self):
        self.__exporting_file()
    
    def envia_csv(self,nome_repo,descricao_repo=''):
        self.__create_repo(nome_repo,descricao_repo)


##### Funções Encapsuladas - Extract

    def __get_repository(self): 
        repo_list = []
        url = f'{self.__api_base_url}/users/{self.__owner}/repos'
        page_num = 1
        while True:
            try:
                url_page = f'{url}?page={page_num}'
                response = requests.get(url_page,headers=self.__headers)
                
                if len(response.json()) > 0 and response.status_code in range(200,299) :
                    repo_list.append(response.json())
                    page_num+=1
                else:
                    break
                      
            except:
                print(f'Erro ao acessar API get_repository_22 :{str(response.status_code)}')
                break
        
        if len(repo_list)>0:
            self.__data_extraction(repo_list)
        else:
            print(f'Nenhum repositorio encontrado para {self.__owner}')
             

    def __data_extraction(self,repo_pages):
        repos_name = [] 
        repos_language = []

        for page in repo_pages:
            for repo in page:
                repos_name.append(repo['name'])
                repos_language.append(repo['language'])
        
        self.__dados_amz['repository_name'] = repos_name
        self.__dados_amz['language'] = repos_language
        print(':.. Dados armazenados com sucesso ..:')


##### Funções Encapsuladas - Transform
    
    def __exporting_file(self):
        try:
            if len(self.__dados_amz)>0:                 
                self.__dados_amz.to_csv(f'data_processed/{self.__owner}.csv')
                print(f':.. Arquivo csv criado em /data_processed/{self.__owner}.csv ..:')
                self.__caminho_arquivo = f'data_processed/{self.__owner}.csv'
            else:
                print('dados não armazenados do repositório')
        except:
            print(f'Não foi possivel exportar para = ../data_processed/{self.__owner}.csv exporting_file_69')

##### Funções Encapsuladas - Load

    def __create_repo(self,name_repo,desc_repo):
        url = f'{self.__api_base_url}/user/repos'

        dict_data = {
            'name' : f'{name_repo}',
            'description' : f'{desc_repo}',
            'private' : False
        }

        try:
            response = requests.post(url, json=dict_data ,headers=self.__headers)

            if response.status_code in range(200,299):
                print(f':.. Repositório criado com sucesso ..:')
                self.__send_file(name_repo)
            else:
                if 'name already exists on this account' in response.text:
                    self.__send_file(name_repo)
                else:
                    print(f'Erro ao criar Repositorio :')
                    print(response.json())
        except:
            print(f'Erro na api create_repo_97 :')



    def __prepare_file(self):
        if self.__caminho_arquivo != '':
            with open(self.__caminho_arquivo,'rb') as file:
                file_content = file.read()

            encoded_content = base64.b64encode(file_content) 
            return encoded_content
        else:
            print('arquivo não criado')
            return None


    def __send_file(self,repo):

        path = self.__caminho_arquivo.split('/')
        file_encoded = self.__prepare_file()

        url = f'{self.__api_base_url}/repos/{self.__username}/{repo}/contents/{path[-1]}'
        data = {
            'message': 'Adicionando arquivo de repositorio do Git',
            'content': file_encoded.decode('utf-8')
        }

        try:
            if  file_encoded != None:   
                response = requests.put(url,json=data, headers=self.__headers )
                if response.status_code in range(200,299):
                    print(f':.. Arquivo enviado ao repositório {repo} com sucesso ..:')
                else:
                    print(f':Erro ao enviar arquivo ao repositório {repo} :')
                    print(response.json())
            else:
                print('Arquivo não enviado a conta')
        except:
            print('Erro na api send_file_123')

        
