import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser(description='web-page loader')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=os.getcwd(), help='path for save')
    return parser
