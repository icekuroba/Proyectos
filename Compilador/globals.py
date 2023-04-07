
# {
#     label: [#De linea donde se encuentra,dirrecion de memerio, "linea a remplazar"]
# }
relative_labels = {}
exception_mnemonic = {
    "BRCLR":3,
    "BRSET":3,
    "BCLR":2,
    "BSET":2
}
program_finished = False
memory_address = ""
program_constants = {}
error_code = ""
is_constant = False
bytes_constant = 0
list_mnemonics = None

s19_relative_code = []

s19_memory = ""
s19_lines = {
    # "memory":"LINE"
}

s19_content_to_write = []


class Globals:
    @staticmethod
    def separate_bytes(line=""):
        byte_sep = []
        new_line = ""
        for i in range(0,len(line),2):
            byte_sep.append(line[i:i+2])

        byte_sep = byte_sep[::-1]

        for byte in byte_sep:
            new_line = byte + " " + new_line

        return new_line.strip()

    @staticmethod
    def set_checksum():
        global s19_content_to_write
        to_check = []
        checksum = 0

        for key,values in Globals.get_s19_lines().items():
            byte_key = Globals.separate_bytes(key)

            for b in byte_key.split():
                to_check.append(b)

            for value in values:
                for b in value.strip().split():
                    to_check.append(b)

        for byte in to_check:
            checksum += int(byte,16)

        checksum = hex(checksum)

        if len(checksum) > 4:
            checksum = checksum[3:]
        else:
            checksum = checksum[2:]

        # print(s19_content_to_write)

        # s19_content_to_write.insert(-1,checksum)
        
        return checksum


    @staticmethod  
    def convert_s19_lines_to_list():
        global s19_lines 
        global s19_content_to_write

        for key in s19_lines.keys():
            line = ""
            k_line = "<" + key + "> "
            for mn in s19_lines[key]:
                line += mn
            line += "\n"
            s19_content_to_write.append(f"{k_line}{line}")



    @staticmethod  
    def get_s19_content_to_write():
        global s19_content_to_write
        Globals.convert_s19_lines_to_list()
        return s19_content_to_write


    @staticmethod  
    def set_s19_lines(key="",value=""):
        global s19_lines 

        if key not in s19_lines.keys():
            s19_lines[key] = [value]
        else:
            s19_lines[key].append(" " + value)

    @staticmethod  
    def set_s19_lines_relative(key="",index=0,value=""):
        global s19_lines 

        s19_lines[key][index] = value
   

    @staticmethod
    def set_s19_memory(new_value):
        global s19_memory 
        s19_memory = new_value

    @staticmethod
    def set_relative_labels(key,value):
        global relative_labels 
        relative_labels[key] = value

    @staticmethod  
    def set_list_mnemonics(value):
        global list_mnemonics 
        list_mnemonics = value.index.tolist()

    @staticmethod  
    def set_bytes_constant(value):
        global bytes_constant 
        bytes_constant = value


    @staticmethod  
    def set_is_constant(value):
        global is_constant 
        is_constant = value

    @staticmethod  
    def set_program_finished(new_value):
        global program_finished 
        program_finished = new_value

    @staticmethod  
    def set_error_code(new_value="",restart=False):
        global error_code 
        
        if restart:
            error_code = ""
            return
            
        error_code = error_code + " " + new_value


    @staticmethod
    def set_memory_address(new_value):
        global memory_address 
        memory_address = new_value

    @staticmethod
    def set_program_constants(key,value):
        global program_constants 
        program_constants[key] = value

    @staticmethod
    def get_program_finished():
        global program_finished 
        return program_finished

    @staticmethod
    def get_s19_memory():
        global s19_memory
        return s19_memory

    @staticmethod
    def get_memory_address():
        global memory_address 
        return memory_address

    @staticmethod
    def get_program_constants():
        global program_constants 
        return program_constants

    @staticmethod
    def get_value_constants(key=""):
        try: 
            global program_constants 
            return program_constants[key]
        except KeyError:
            Globals.set_error_code("002\tVARIABLE INEXISTENTE")

    @staticmethod
    def get_relative_labels():
        try: 
            global relative_labels 
            return relative_labels
        except KeyError:
            Globals.set_error_code("003\tETIQUETA INEXISTENTE")


    @staticmethod
    def get_value_exception(key=""):
        """
            Esta funcion regresa el numero de operandos * 2, para obtener el numero de caracteres que debe tener la variable op
        """
        try: 
            global exception_mnemonic 
            return exception_mnemonic[key]*2
        except KeyError:
            Globals.set_error_code("002\tVARIABLE INEXISTENTE")

    @staticmethod  
    def get_s19_lines():
        global s19_lines 
        return s19_lines  

    @staticmethod  
    def get_error_code():
        global error_code 
        return error_code       

    @staticmethod  
    def get_is_constant():
        global is_constant 
        return is_constant 

    @staticmethod  
    def get_exception_mnemonic():
        global exception_mnemonic 
        return exception_mnemonic 

    @staticmethod  
    def get_bytes_constant():
        global bytes_constant 
        return bytes_constant

    @staticmethod  
    def get_list_mnemonics():
        global list_mnemonics 
        return list_mnemonics


    def check_is_label(self,label):
        
        aux = Globals.get_relative_labels()

        if label in aux.keys():
            return aux[label]

        return []
