import sys
import files.file as fl
import files.lst as lst

from globals import Globals
from mnemonics.mnemonics import Mnemonic
from converter.converter import Converter


# Las etiquetas van a ser aquellas que no tienen una tabulacion


# Para saber que es modo inh pasas el mnemonico y verficas que haya info ahi

if __name__ == "__main__":
    mnemonics = Mnemonic()
    source_code = fl.File()
    lst_code = lst.Lst(mnemonics)

    Globals.set_list_mnemonics(mnemonics.get_data())


    # Read the source code with extension .asc 
    # file_name = f"{input("Write the name of the file to compile: ")}.asc" 
    source_code.read("textoCodificado1.asc")
 
    lst_code.set_lines_source_code(source_code.get_lines())
 
    lst_code.relative_memory()


    content_s19 = Globals.get_s19_content_to_write()
    
    # content_s19 = [content_s19[0].replace("\n",f" {Globals.set_checksum().upper()}")]
    # print(content_s19)


    # print(Globals.get_s19_lines())

    # print(Globals.get_s19_content_to_write())


    # print(lst_code.content_to_write)

    fl.File().write_file('source_code.s19',content_s19)
    fl.File().write_file('source_code.lst',lst_code.content_to_write)

    # print(Converter.convert_operand("list"))
    # print("Converter ",Converter.separate_bytes("ABCD"))
    # print(Globals.get_program_constants())
    # print(Globals.get_memory_address())
    # print(source_code.get_lines())
    # print(mnemonics.imm_dressing_mode('adca'))

# print("TO BINARY",Converter.convert_memory_relative("8003","800A"))