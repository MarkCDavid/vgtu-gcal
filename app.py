from timetableparser import parse
import sys
import export
import argparse


def change_extension(filename, new_extension):
    return f"{'.'.join(filename.split('.')[:-1])}.{new_extension}"


def build_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('scriptname', default=sys.stdin)
    parser.add_argument('infile', default=sys.stdin)
    parser.add_argument('outfile', default=sys.stdout)
    parser.add_argument('--simple', action='store_const', const=True, default=True)
    parser.add_argument('--nogroups', action='store_const', const=True, default=True)
    args = parser.parse_args(sys.argv)
    return (args.infile, args.outfile, export.Options(args.simple, not args.nogroups))


def convert(infile, outfile, options):
    timetable = parse(infile)
    export.csv_gcal(timetable, outfile, options)


if __name__ == "__main__":
    convert(*build_options())
