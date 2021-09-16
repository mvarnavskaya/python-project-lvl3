#!/usr/bin/env python3
import sys
from page_loader import page_loader, cli


def main():
    try:
        args = cli.get_parser().parse_args()
        page_path = page_loader.download(args.url, args.output)
        print(page_path)
    except page_loader.AppInternalError as e:
        print(e)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
