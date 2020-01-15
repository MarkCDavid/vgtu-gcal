from ttparser import parse
from sys import argv

def filenames():
    if len(argv) < 2:
        return

    for filename in argv:
        if filename != argv[0]:
            yield filename


def convert():
    for filename in filenames():
        parse(filename)
                
if __name__ == "__main__":
    convert()



