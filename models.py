import datetime

class Linha(object):
    
    '''Criar objeto com os atributos presentes no JSON recebido pela API, para representar as linhas dos ônibus'''
    
    def __init__(self, codigo, nome, ponto_partida, ponto_retorno, circular):
        self.codigo = codigo
        self.nome = nome
        self.ponto_partida = ponto_partida
        self.ponto_retorno = ponto_retorno
        self.circular = circular

    def __str__(self):
        return "Linha: %s, Nome: %s, Origem: %s, Retorno: %s, Circular: %r" % (self.codigo, self.nome, self.ponto_partida, self.ponto_retorno, self.circular)
 

class Parada(object):
    
    '''Criar objeto com os atributos presentes no JSON recebido pela API para representar as paradas dos ônibus'''
    
    def __init__(self, codigo, nome, endereco, latitude, longitude):
        self.codigo = codigo
        self.nome = nome
        self.endereco = endereco
        if not longitude is None:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
            self.possui_gps = True
        else:
            self.latitude = 0.0
            self.longitude = 0.0
            self.possui_gps = False

    def __str__(self):
        return "Parada: %s, Nome: %s, Endereco: %s, Latitude: %f, Longitude: %f" % (self.codigo, self.nome, self.endereco, self.latitude, self.longitude)
 

class Veiculo(object):
    
    '''Criar objeto com os atributos presentes no JSON recebido pela API para representar os veículos em rota'''
    
    def __init__(self, codigo, latitude, longitude, hora, linha):
        self.codigo = codigo
        self.latitude = latitude
        self.longitude = longitude
        self.hora = hora
        self.linha = linha

    def __str__(self):
        return "Ônibus: %s, Latitude: %s, Longitude: %s, Hora: %s, Linha: %s"% (self.codigo, self.latitude, self.longitude, self.hora, self.linha )
 
