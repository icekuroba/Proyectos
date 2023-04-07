from globals import Globals

class Converter:
    def __init__(self) -> None:
        pass

    

    @staticmethod
    def check_is_label(label) -> list:
        
        aux = Globals.get_relative_labels()

        if label in aux.keys():
            return aux[label]

        return []


    @staticmethod
    def check_is_not_mnemonic(label=""):
        # Si es label, agregar su numero de linea, o su memoria total a globals
        mn = Globals.get_list_mnemonics()

        print(label.lower())

        # Si la palabra es un mnemonico solo esta mal identado 
        if label.lower() in mn:
            return False
        # Si no esta identado y no es un mnemonico es una etiqueta
        return True

        return []

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
    def dec_to_hex(value):
        try:
            hx = hex(int(value)).upper()[2:]
            if len(hx)%2 != 0:
                hx = "0" + hx 

            # Separate string in substrings of length 2
            
            return hx
        except ValueError:
            pass

    @staticmethod
    def clean_space_in_array(array = []):
        clean_array = []
        for item in array:
            if item != '':
                clean_array.append(item)
        return clean_array



    @staticmethod
    def ascii_to_hex(value):
        try:
            asc = ord(value)
            hx = hex(asc).upper()[2:]

            if len(hx)%2 != 0:
                hx = "0" + hx 
            return hx
        except TypeError:
            pass



    def octal_to_hex(value):
        """
        !Get the number without the 0
        """
        try:
            oct = int(value, base=8)
            hx = hex(oct).upper()[2:]

            if len(hx)%2 != 0:
                hx = "0" + hx 

            return hx
        except TypeError:
            pass



    @staticmethod
    def sum_to_memory(data=[]):

        # Maximun 255 bytes 80FF
        # start_memory - final_memory <= 255 bytes, new line = True
        start_memory_str = ""
        new_line = False
        if len(data) >= 1 and data[0] != '--':
            start_memory = int(Globals.get_memory_address(), base=16)
            start_memory_str = Converter.dec_to_hex( start_memory )
            n_bytes = len(data) # 1 bytes o 2 bytes  Para directiva  Falta info
            final_memory_int = int(Converter.dec_to_hex( start_memory + n_bytes),base=16)
            final_memory_str = Converter.dec_to_hex( start_memory + n_bytes)

            if abs(final_memory_int - int(Globals.get_s19_memory(),16)) > 255:
                new_line = True

            Globals.set_memory_address(final_memory_str)

        return [start_memory_str,new_line]



    @staticmethod
    def convert_complement_2_direct(value):
            # zfill rellena por la izquierda Nos dara una string tipo 00001000
            binary = bin(value)[2:].zfill(8)
            one = "00000001"
            n_binary = ""
            result = ""
            rest = 0

            print("BEFORE",binary)

            # Negar el numero binario bi
  
            for i in range(8):
                if binary[i] == '0':
                    n_binary += "1"
                else:
                    n_binary += "0"

            for i in range(7,-1,-1):
                # print("suma",int(n_binary[i]),int(one[i]))
                sum = int(n_binary[i]) + int(one[i]) + rest
                if sum >= 2:
                    result += "0"
                    rest = 1
                else:
                    result += str(sum)
                    rest = 0

            # El resultado sale en reversa por hacer concatenacion, entonces doy reverse a la cadena o arreglo la concatenacion
            result = result[::-1]

            return Converter.dec_to_hex(int(result, base=2))



            


    @staticmethod
    def convert_constant(const = ""):
        values_constant = Globals.get_value_constants(const.upper())
        return values_constant

    @staticmethod
    def is_constant(line = ""):
        if line.upper() in Globals.get_program_constants().keys():
            return True
        return False


    @staticmethod
    def is_octal(line = ""):
        if len(line) > 1:
            if line[0] == '0':
                return True
        return False

    @staticmethod
    def is_ascii(line):
        if "'" in line:
            return True
        return False
    
    @staticmethod
    def is_hex(line):
        if "$" in line:
            return True
        return False

    @staticmethod
    def is_exception(line):
        if line.upper() in Globals.get_exception_mnemonic().keys():
            return True
        return False

    @staticmethod
    def multiple_operands(array_op=[]):
        
        Globals.set_bytes_constant(len(array_op))
        # print("BYTES",Globals.get_bytes_constant())
        nw = ""
        for item in array_op:
            nw = nw + Converter.convert_operand(item)
        return nw

    @staticmethod
    def  convert_operand(op=""):
        if Converter.is_hex(op):
            op = op[1:]
            if len(op)%2 != 0:
                op = "0" + op 
        elif Converter.is_ascii(op):
            # Remove the prefix '
            op = Converter.ascii_to_hex(op[1:])
        elif Converter.is_octal(op):
            # Remove the prefix 0
            op = Converter.octal_to_hex(op)
        elif Converter.dec_to_hex(op): 
            op = Converter.dec_to_hex(op) 
        else:

            if Converter.is_constant(op):
                array_op = Converter.convert_constant(op)
                return Converter.multiple_operands(array_op)
            else:
                # Si no hay un error y llega a este punto poner el error
                if Globals.get_error_code() == "":
                    if Globals.get_is_constant():
                        Globals.set_error_code("001   CONSTANTE INEXISTENTE")
                    else:
                        Globals.set_error_code("002   VARIABLE INEXISTENTE")
                    op = ""
            
        
        return op

    @staticmethod
    def  convert_memory_relative(init="",final="") -> str:
        # Obtener desde donde sale, hasta donde llega
        aux_init = int(init,base=16)
        aux_fin  = int(final,base=16) + int("0002",base=16)


        result   =  aux_fin - aux_init
        
        if result <  -127 or result > 128:
            Globals.set_error_code("008\tSALTO RELATIVO MUY LEJANO")
        
        result = abs(aux_fin - aux_init)

        result_complement_hex_str = Converter.convert_complement_2_direct(result)
        # result_hex = Converter.dec_to_hex(result) 
        return result_complement_hex_str