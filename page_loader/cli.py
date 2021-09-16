import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help='specify path to save')
    return parser
