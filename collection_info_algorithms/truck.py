# encoding: utf-8

class truck:
    def __init__(self, plate, capacity):
        self.plate = plate
        self.capacity_desc = capacity
        self.capacity = self.capacity_desc_to_m3(self.capacity_desc)
    
    def capacity_desc_to_m3(self, cap_text):
        if cap_text == 'Remoção 14/16 m3':
            return 14
        elif cap_text == 'Remoção 9 m3 - Mini':
            return 9
        elif cap_text == 'Remoção 11 m3 - Maxi':
            return 11
        elif cap_text == 'Remoção 9 m3 - Médio':
            return 9
        elif cap_text == 'Remoção 7 m3':
            return 7    