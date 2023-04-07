from mnemonics.mnemonics import Mnemonic
from converter.converter import Converter

# Import global variables
from globals import Globals 
# En ORG es donde empieza
# *Comentario


class Lst:
    def __init__(self,mnemonics) -> None:
        self.source_code_lines = []
        self.dict_lst          = {}
        self.content_to_write  = []
        self.mnemonics         = mnemonics

    def create_code(self):
        for n_line in range(0,len(self.source_code_lines)):
            self.dict_lst[n_line+1] = [self.source_code_lines[n_line].replace('\n','')]
        
        self.compile_code()

    def create(self):
        pass

    def compile_code(self):
        global program_finished
        # Verificar si es un antipatron el uso de esta variable, solo si se modifica en diferentes lugares
        for key,value in self.dict_lst.items():
            # RelativeLabel = ""
            line = comment = ""
            isComment = False 
            comment_init_pos = 0
            new_memory   = "VACIO"
            start_memory_line = "VACIO"
            arr_mnemonic = ['','','']
            f = False
            op = ""
            array_op = []
            is_constant = False
            #If there is no a comment
            # Handle line 
            # Empty line stay as it came
            line       = value[0]
            array_line = line.split(" ")
            isLabel = False
            isLineLabel = False

            start_memory_s19 = Globals.get_s19_memory()


            

            # print(hex())

            # if int(start_memory_s19) >



            # If there is a comment in the line, it doesn't matter where it is
            if '*' in value[0]:
                isComment = True
                comment_init_pos = value[0].index('*')
                if comment_init_pos > 0 :
                    line,comment = value[0][:comment_init_pos-1].strip(),value[0][comment_init_pos:]



            # print(array_line,isComment)
            #!Revisar que las etiquetas del modo relativo no tengan ningun espacio a la izquierda
            if '*' not in array_line[0] and array_line[0] != '' and Converter.check_is_not_mnemonic(array_line[0]):
                # print(array_line)
                # Converter.convert_complement_2_direct(8)
                # RelativeLabel += array_line[0]

                Globals.set_relative_labels(key=array_line[0].upper(),value=[key,Globals.get_memory_address(),""])
                isLineLabel = True
            # Revisar que haya identacion de al menos un espacio para mnemonicos
            elif array_line[0] == '':
                # Reviso que haya identacion y luego le quito esos espacios en blanco
                line = line.strip()
                array_line = line.split(" ")
            else:
                if '*' not in array_line[0]:
                    Globals.set_error_code("009   INSTRUCCIÓN  CARECE DE AL MENOS UN ESPACIO RELATIVO  AL MARGEN ")
            

            #Check if there is a assembly directive 
            if Mnemonic.is_assembler_directive(line):
                if "ORG" in array_line and Converter.is_hex(array_line[-1]):
                    # Globals
                    Mnemonic.assembler_directives("ORG",array_line[-1][1:])
                    Globals.set_s19_memory(Globals.get_memory_address())
                elif "EQU" in array_line:
                    # [label EQU direction]
                    Mnemonic.assembler_directives("EQU",constants_info = [array_line[0],array_line[2]])
                elif "FCB" in array_line:
                    # [label FCB direction1,direction2]
                    Mnemonic.assembler_directives("FCB",constants_info = [array_line[0],array_line[2]])
                elif "END" in array_line:
                    Mnemonic.assembler_directives("END")
                else:
                    pass
            elif isLineLabel == False:
                # print(array_line)
                # Mnemonic always at first index
                #INH -> len of array (1) unless there is a comment 
                #Check in the data frame if there are data in the INH column
                
                if len(array_line[0]) > 0:    
                    array_line = Converter.clean_space_in_array(array_line)

                    # If the line, doesn't start with a comment
                    if '*' not in array_line[0] :


                        # Check if there is operand in mnemonics with operands
                        if len(array_line) > 1:
                            op = array_line[1]
                        else:
                            # Si no es el modo inherente hay que checar operandos
                            if self.mnemonics.inh_dressing_mode(array_line[0].lower())[0] == '--':
                                Globals.set_error_code("005\tINSTRUCCIÓN CARECE DE OPERANDOS")
                            array_line.append("")



                        label_array = Converter.check_is_label(label=array_line[1])
                        # Si el array no es vacio es una etiqueta
                        if len(label_array) >= 1:
                            isLabel = True
                            # guardar la memoria en la que empezaron antes de sumar el mnemonico relativo
                            label_array.insert(0,Globals.get_memory_address())
                            label_array[1] = key



                        if Converter.is_exception(array_line[0]):
                            array_op = array_line[1].replace("#","").split(",")

                            op = Converter.multiple_operands(array_op)

                            # Agregar el tratamiento de labels aqui



                            # Revisar el primer operando,eso dara el codigo del mnemonico
                            # directo
                            # indx
                            # indy
                            if ',X' in array_op[0].upper():
                                arr_mnemonic = self.mnemonics.indx_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                # Checar los operandos que cada excepcion tiene
                                if len(op) > Globals.get_value_exception(array_line[0]):
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")

                            elif ',Y' in array_op[0].upper():
                                arr_mnemonic = self.mnemonics.indy_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                # Checar los operandos que cada excepcion tiene
                                if len(op) > Globals.get_value_exception(array_line[0]):
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")
                            else:
                                arr_mnemonic = self.mnemonics.dir_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                # Checar los operandos que cada excepcion tiene
                                if len(op) > Globals.get_value_exception(array_line[0]):
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")
                        
                        else:


                            #if it's imm, remove the operand
                            if '#' in array_line[1]:
                                op = array_line[1].replace("#","")
                                Globals.set_is_constant(True)
                            if ',X' in array_line[1].upper():
                                op = array_line[1].split(",")[0]
                            if ',Y' in array_line[1].upper():
                                op = array_line[1].split(",")[0]


                            # Si no es el modo inherente hay que checar operandos
                            if self.mnemonics.inh_dressing_mode(array_line[0].lower())[0] == '--':
                                op = Converter.convert_operand(op)


                            #!configurar is_error in globals y no generar archivo .s19

                            #Si la longitud del array_op es mayor a 3 entonces esta fuera de rango
                            # !Dressing modes

                            #Inherent mode 
                            if self.mnemonics.inh_dressing_mode(array_line[0].lower())[0] != '--':
                                arr_mnemonic = self.mnemonics.inh_dressing_mode(array_line[0].lower()) 
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                if len(array_line) >= 2 and '*' not in array_line[1] and array_line[1].strip().replace("\t","") != '':
                                    Globals.set_error_code("006\tINSTRUCCIÓN NO LLEVA OPERANDOS")

                            elif self.mnemonics.rel_dressing_mode(array_line[0].lower())[0] != '--':
                                arr_mnemonic = self.mnemonics.rel_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                # if len(op) > 4:
                                #     Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")

                            # immediate dressing mode 
                            elif '#' in array_line[1] :
                                arr_mnemonic = self.mnemonics.imm_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                if len(op) > 4:
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")

                            #Direct addressing mode, its operand is 1 byte.  
                            #Si usa una constante, debe ser solo de 1 byte
                            # longitud es de 3 porque se agrega si llega a tener un simbolo $,0 para denotar el tipo de dato

                            elif ",X" in array_line[1].upper():
                                arr_mnemonic = self.mnemonics.indx_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                if len(op) > 2:
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")
                            elif ",Y" in array_line[1].upper():
                                arr_mnemonic = self.mnemonics.indy_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                if len(op) > 2:
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")
                            elif len(array_line[1]) <= 3:
                                arr_mnemonic = self.mnemonics.dir_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' ')) 
                                if len(op) > 2:
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA") 
                                        
                            elif  len(array_line[1]) >= 4:
                                arr_mnemonic = self.mnemonics.ext_dressing_mode(array_line[0].lower())
                                [ start_memory_line,f ] = Converter.sum_to_memory(arr_mnemonic[0].split(' '))
                                if len(op) > 4:
                                    Globals.set_error_code("007   MAGNITUD DE OPERANDO ERRONEA")
                            else:
                                Globals.set_error_code("004   MNEMÓNICO INEXISTENTE")
        




                        if len(label_array) >= 1:
                            # Quitar los errores que no tienen que ver con label
                            Globals.set_error_code(restart=True)


                        if array_line[0].lower() == "jmp":
                            aux = Globals.get_relative_labels()
                            op = aux[array_line[1]][2] 

                        if op != "":
                            # !The operand has more than 2 characters or 1 byte
                            if len(op) > 2 :
                                op = Converter.separate_bytes(op)
                                print(op)
                                [ new_memory,f ] = Converter.sum_to_memory(op.split(" "))
                            else:
                                print(op)
                                [ new_memory,f ] = Converter.sum_to_memory([op])


            # Si la direccion de memoria supero los n bytes que permitimos por linea en s19, debemos cambiar la start_memory

            if f == True:
                new = int(start_memory_s19,16) + 255
                Globals.set_s19_memory(Converter.dec_to_hex(new))
                print("NEW",Globals.get_s19_memory())


        

            # print("Mnemonic line ",array_line,arr_mnemonic[0])
            object_code = f"{arr_mnemonic[0]} {op}"

            # Agrego a mi dicc de s19, el codigo objeto de la linea

            if len(Globals.get_s19_memory()) > 0 and len(start_memory_s19) > 0 and object_code !=' ':
                Globals.set_s19_lines(start_memory_s19,object_code.strip())

            print_key = f"0{key}" if key <= 9 else key

            if isLabel == True:
                self.content_to_write.append(f"{print_key} : {start_memory_line : <10}  {object_code : <15}{line : <15}{comment : <15} {Globals.get_error_code() : <20}\n")
            elif isComment and comment_init_pos > 0:
                self.content_to_write.append(f"{print_key} : {start_memory_line : <10}  {object_code : <15}{line : <15}{comment : <15} {Globals.get_error_code() : <20}\n")
            else:
                self.content_to_write.append(f"{print_key} : {start_memory_line : <10} {object_code : <15}{line : <15} {Globals.get_error_code() : <20}\n")
            # Por cada ciclo reinicio el error Y si es una constante
            Globals.set_error_code(restart=True)
            Globals.set_is_constant(False)
            Globals.set_bytes_constant(0)


        if Globals.get_program_finished() == False:
            Globals.set_error_code("010   NO SE ENCUENTRA END")
            self.content_to_write.append(f"{print_key} : {Globals.get_error_code()}\n")



    def relative_memory(self):
        # Si es jmp la linea que indica no hacer nada
 
        new_code_object = ""

        for name,value_label in Globals.get_relative_labels().items():
            comment = ""
            # Restamos uno por el indice 0
            line_file = self.content_to_write[value_label[1]-1].split()
            if "JMP" not in line_file:

                # Buscar sobre el archivo s19 el opcode 
                # !Tal vez no sirva si tiene varios saltos
                for key_d,value in Globals.get_s19_lines().items():
                    for code in value:
                        if line_file[3] in code:
                            indx = value.index(code)
                            key = key_d

                            print("LINEA",line_file[3],indx,key)



                # Agregar el nuevo mnemonico y codigo objeto tanto al archivo lst como s19
                line_file[3] += " " + Converter.convert_memory_relative(init=value_label[2],final=value_label[0])
                
                for i in range(4,len(line_file)):
                    new_code_object += " " + line_file[i]



                Globals.set_s19_lines_relative(key,indx,f" {line_file[3]}")


                new_line = f"{value_label[1]} : {value_label[0] : <10}  {line_file[3] : <15} {new_code_object : <15} {Globals.get_error_code() : <15}\n"
                self.content_to_write[value_label[1]-1] = new_line
                
            # pass




    def get_lst_info(self):
        return self.dict_lst

    def set_lines_source_code(self,lines):
        self.source_code_lines = lines
        self.create_code()