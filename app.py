#!python

from timetable.timetableparser import parse
import sys
import export
import argparse


def change_extension(filename, new_extension):
    return f"{'.'.join(filename.split('.')[:-1])}.{new_extension}"


def build_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', default=sys.stdin, help="input HTML file")
    parser.add_argument('output', default=sys.stdout, help="output HTML file")
    parser.add_argument('--simple', action='store_const', const=True,
                        default=False,
                        help="course code and additional information in parentheses are discarded from the subject")
    parser.add_argument('--nogroups', action='store_const',
                        const=True, default=False,  help="subgroups are discarded from the subject")
    args = parser.parse_args(sys.argv[1:])
    return (args.input, args.output, export.Options(args.simple, not args.nogroups))


def convert(infile, outfile, options):
    timetable = parse(infile)
    export.csv_gcal(timetable, outfile, options)


if __name__ == "__main__":
    convert(*build_options())
