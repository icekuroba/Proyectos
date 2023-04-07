import sys
import pandas as pd
from globals import Globals


class Mnemonic:
    def __init__(self):
        self.data_frame = self._load_up()




    def imm_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame['IMM_CODE'][mnemonic].strip(), self.data_frame['IMM_BYTES'][mnemonic].strip(), self.data_frame['IMM_CYCLES'][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    def dir_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame['DIR_CODE'][mnemonic].strip(), self.data_frame['DIR_BYTES'][mnemonic].strip(), self.data_frame['DIR_CYCLES'][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    def indx_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame["IND,X_CODE"][mnemonic].strip(), self.data_frame["IND,X_BYTES"][mnemonic].strip(), self.data_frame["IND,X_CYCLES"][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    def indy_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame["IND,Y_CODE"][mnemonic].strip(), self.data_frame["IND,Y_BYTES"][mnemonic].strip(), self.data_frame["IND,Y_CYCLES"][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']
    def ext_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame['EXT_CODE'][mnemonic].strip(), self.data_frame['EXT_BYTES'][mnemonic].strip(), self.data_frame['EXT_CYCLES'][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    def inh_dressing_mode(self,mnemonic):
        try:
            
            # print([self.data_frame['INH_CODE'][mnemonic].strip(), self.data_frame['INH_BYTES'][mnemonic], self.data_frame['INH_CYCLES'][mnemonic]])
            return [self.data_frame['INH_CODE'][mnemonic].strip(), self.data_frame['INH_BYTES'][mnemonic].strip(), self.data_frame['INH_CYCLES'][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    def rel_dressing_mode(self,mnemonic):
        try:
            return [self.data_frame['REL_CODE'][mnemonic].strip(), self.data_frame['REL_BYTES'][mnemonic].strip(), self.data_frame['REL_CYCLES'][mnemonic].strip()]
        except KeyError:
            Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
            return ['--','','']

    @staticmethod
    def is_assembler_directive(line):
        directive = ["ORG","EQU","FCB","END"]
        for ins in line.split(" "):
            if ins in directive:
                return True
        return False

    @staticmethod
    def assembler_directives(directive,address = "",constants_info = []):
        if directive == "ORG":
            Globals.set_memory_address(address)
        elif directive == "EQU":
            Globals.set_program_constants(key=constants_info[0],value= [constants_info[1]] )
        elif directive == "FCB":
            # print(constants_info[1])
            Globals.set_program_constants(key = constants_info[0], value = constants_info[1].split(","))
        elif directive == "END":
            Globals.set_program_finished(True)
        else:
            pass
            
        
    def get_data(self):
        return self.data_frame

    #Función privada 
    def _load_up(self):
        tmp_df_mnemonic = pd.read_csv("../Compilador/Lista.csv")
        tmp_df_mnemonic = tmp_df_mnemonic.set_index("MNEMONICO")
        return tmp_df_mnemonic
