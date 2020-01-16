from ttparser import parse
from sys import argv
import export

def filenames():
    if len(argv) < 2:
        return

    for filename in argv:
        if filename != argv[0]:
            yield filename

def change_extension(filename, new_extension):
    return f"{'.'.join(filename.split('.')[:-1])}.{new_extension}"

def convert():
    for filename in filenames():
        new_filename = change_extension(filename, "csv")
        timetable = parse(filename)
        export.csv_gcal(timetable, new_filename)

                
if __name__ == "__main__":
    convert()



