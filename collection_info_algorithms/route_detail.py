class route_detail:
    def __init__(self, line):
        self.address = line[6] # MORADA
        self.freg_id = line[10] # FRG_ID
        self.freg_desc = line[11] # FRG_DESC
        self.collection_type_abrev = line[12] # TPRS_AB
        self.collection_type = line[13] # TPRS_DESC
        self.route = line[17] # CRC_COD
        self.par_impar = line[20] # CRC_COD
        self.route_type_description = line[23] # TRC_DESC
