# encoding: utf-8 

from datetime import datetime

class collection_data:
    def __init__(self, line):
        #line = line.split(";")
        self.group = line[13] # GrpReal
        self.origin = line[14] # Origem
        self.destiny = line[15] # Destino
        self.operation = line[16] # Operaçao
        self.operation_group = line[17] # GrpOperacao
        self.date = datetime.strptime(line[20], "%d/%m/%Y") # Data
        self.week = datetime.strftime(self.date, "%W")
        self.shift = line[21] # Turno
        self.year = line[22] # Ano
        self.month = line[23] # Mes
        self.day = line[24] # Dia
        self.time = line[25] # Hora
        self.weight = line[27] # Peso
        self.unit = line[28] # Uni
        self.route = line[30] # Circuito
        self.route_type = line[31] # Tipo CRC
        self.truck_plate = line[34] # Matricula
        self.truck_capacity = line[35] # Capac
        self.truck_type = line[36] # Tipo Viat
        self.truck_fuel_type = line[37] # Combustivel