#!/usr/bin/env python3
import sys

from page_loader import cli, loader


def main():
    try:
        args = cli.get_parser().parse_args()
        page_path = loader.download(args.url, args.output)
        print(page_path)
    except loader.AppInternalError as e:
        print(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
