
import datetime
import json
import requests
import folium
import webbrowser

from models import Linha, Veiculo, Parada


class Inthegra_API():
    
    '''Programa para consumir API fornecida pela STRANS (Superintendência Municipal de Transportes e Trânsitos)
    para obter informações sobre o monitoramento da frota de ônibus da cidade de Teresina-PI'''
    
    url_base = 'https://api.inthegra.strans.teresina.pi.gov.br/v1'
    email = ''    
    senha = ''
    api_key = ''

    def signin():
        '''
        Adicionar ao header o token de autorização fornecido pelo request POST da função getHeaders
        '''
        global token
        credenciais = {"email": Inthegra_API.email, "password": Inthegra_API.senha}
        req = requests.post(Inthegra_API.url_base +'/signin', data=json.dumps(credenciais), headers=Inthegra_API.coletar_headers())
        dados = req.json()    
        token = dados['token']      
        if req.status_code == 200:
            print('CÓDIGO HTTP: 200. A conexão foi um sucesso!')
            print('Token de acesso gerado: ', token)        
        else:
            req.raise_for_status()

        

    def coletar_headers():
        
        '''Função para retornar os headers da requisição'''
        
        headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'en',
            'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'X-Api-Key': Inthegra_API.api_key
                   }
        return headers
        


    def listar_linhas():
        '''Retorna um vetor com todas as linhas de ônibus'''
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token
        req = requests.get(Inthegra_API.url_base + '/linhas', headers = headers)        
        linhas = []
        for linha in req.json():
            rota = Linha(
                codigo = linha.get('CodigoLinha'),
                nome = linha.get('Denomicao'),
                ponto_partida = linha.get('Origem'),
                ponto_retorno = linha.get('Retorno'),
                circular = linha.get('Circular')
                )
            linhas.append(rota)
        return linhas

    def quantidade_linhas_total():
        '''Retorna a quantidade total de linhas em rota'''
        linhas = Inthegra_API.listar_linhas()
        return len(linhas)
        

    def listar_paradas():
        '''Retorna um vetor com todas as paradas de ônibus'''
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token
        req = requests.get(Inthegra_API.url_base + '/paradas', headers = headers)
        paradas = []
        for parada in req.json():
            ponto_de_parada = Parada(
                codigo = parada.get('CodigoParada'),
                nome = parada.get('Denomicao'),
                endereco = parada.get('Endereco'),
                latitude = parada.get('Lat'),
                longitude = parada.get('Long')
                )
            paradas.append(ponto_de_parada)
        return paradas

    def quantidade_paradas_total():
        '''Retorna a quantidade total de paradas de todas as linhas em rota'''
        paradas = Inthegra_API.listar_paradas()
        return len(paradas)       
        


    def listar_veiculos():
        '''Retorna um vetor com todos os veículos'''
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token
        req = requests.get(Inthegra_API.url_base + '/veiculos', headers = headers)       
        veiculos = []
        for registro in req.json():
            linha = registro['Linha']
            rota = Linha(
                    codigo = linha.get('CodigoLinha'),
                    nome = linha.get('Denomicao'),
                    ponto_partida = linha.get('Origem'),
                    ponto_retorno = linha.get('Retorno'),
                    circular = linha.get('Circular')
                              )
            for veiculo in linha.get('Veiculos'):
                frota = Veiculo(
                        codigo = veiculo.get('CodigoVeiculo'),
                        latitude = veiculo.get('Lat'),
                        longitude = veiculo.get('Long'),
                        hora = veiculo.get('Hora'),
                        linha = rota
                              )
                veiculos.append(frota)
        return veiculos
    
    def procurar_veiculo_codigo_linha(codigo_linha):
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token
        req = requests.get(Inthegra_API.url_base + '/veiculosLinha?busca=' + str(codigo_linha), headers = headers)       
        veiculos = []       
        if req.status_code == 404:
            print('Termo informado: {}. Sem resultados para o termo informado!'.format(str(codigo_linha)))
        #Progamar lógica de retorno os veículos encontrados.
            



    def quantidade_veiculos_em_rota():
        '''Retorna a quantidade total de veículos encontrados em rota'''
        veiculos = Inthegra_API.listar_veiculos()
        return len(veiculos)


    def procurar_parada_termo(query):       
        '''Retorna as paradas que possuem o parâmetro informado nos campos Denominacao e Endereco
           Parâmetro solicitado: string contendo parte do endereço.      
        '''           
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token       
        req = requests.get(Inthegra_API.url_base + '/paradas?busca=' + str(query), headers = headers)   
        paradas_encontradas = []
        if not req.json():
            print('Termo informado: {}. Sem resultados para o termo informado!'.format(str(query)))
        else:            
            for parada in req.json():               
                ponto_de_parada = Parada(
                codigo = parada.get('CodigoParada'),
                nome = parada.get('Denomicao'),
                endereco = parada.get('Endereco'),
                latitude = parada.get('Lat'),
                longitude = parada.get('Long')
                )
                paradas_encontradas.append(ponto_de_parada)
            return paradas_encontradas  
        
    def quantidade_paradas_por_termo(query):
        paradas = Inthegra_API.procurar_parada_termo(query)
        return len(paradas)


    def procurar_parada_codigoLinha(codigo_linha):
        '''Retorna as paradas da linha indicada no parâmetro informado
           Parâmetro solicitado: string contendo o código da linha.
        '''
        headers = Inthegra_API.coletar_headers()
        headers['X-Auth-Token'] = token       
        req = requests.get(Inthegra_API.url_base + '/paradasLinha?busca=' + str(codigo_linha), headers = headers)
        paradas_encontradas = []              
        if req.status_code == 404:
            print('Termo informado: {}. Sem resultados para o termo informado!'.format(str(codigo_linha)))
        else:
            linha = req.json()['Linha']
            rota = Linha(
                codigo=linha.get('CodigoLinha'),
                nome=linha.get('Denomicao'),
                ponto_partida=linha.get('Origem'),
                ponto_retorno=linha.get('Retorno'),
                circular=linha.get('Circular')
                          )
            for parada in req.json()['Paradas']:
                paradas = Parada(
                        codigo = parada.get('CodigoParada'),
                        nome = parada.get('Denomicao'),
                        endereco = parada.get('Endereco'),
                        latitude = parada.get('Lat'),
                        longitude = parada.get('Long')    
                                 )
                paradas_encontradas.append(paradas)

            return paradas_encontradas
         


       
Inthegra_API.signin()   #Fazer login na API
a = Inthegra_API.listar_veiculos()
for i in a:
    print(i['Linha']['Veiculos'][0]['Lat'])

mapa = folium.Map(location=[-5.0765337,-42.8108589],
                  zoom_start=12,                                  
                  )

#Marcar posição do ponto com circulo
def marcarPercursso(latitude, longitude):
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=5,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(mapa)
    
    
percusso = []                 
for linha in a:
    folium.Marker(
        [linha['Linha']['Veiculos'][0]['Lat'], linha['Linha']['Veiculos'][0]['Long']],
        tooltip="<strong>Linha: "+linha["Linha"]['Denomicao']+"</strong>"+" - Hora atualização: "+linha["Linha"]['Veiculos'][0]['Hora'],
        ).add_to(mapa)
    percusso.append([linha['Linha']['Veiculos'][0]['Lat'], linha['Linha']['Veiculos'][0]['Long']])
    for i in percusso:
        marcarPercursso(i[0], i[1])

mapa.save('mapa.html')
webbrowser.open_new_tab('mapa.html')

#print('Há {} veículos em rota neste momento!'.format(Inthegra_API.quantidade_veiculos_em_rota()))

#TODO Criar exceção para quando o serviço estiver fora do ar.
#TODO Abrir o novo mapa direto no navegador padrão.
#TODO Atualizar o posicionamento a cada 30 segundos.
#TODO Alterar o ícone do marcador para um ícone de veículo.
#TODO Demonstrar na tela a quantidade de veículos rastreados.
#TODO Escolher linha de ônibus.
