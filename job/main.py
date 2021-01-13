import sys
import logging
import argparse
from typing import List

from job.murker import MurkerLifecycle


def configure_logging(log_level: int) -> None:
    fmt = '[%(asctime)s][%(levelname)s]%(message)s'
    logging.basicConfig(stream=sys.stdout, format=fmt, level=log_level, datefmt="%H:%M:%S")


def deploy_murkers(lifecycle: MurkerLifecycle) -> None:
    lifecycle.fetch_dependencies()
    lifecycle.compile()
    lifecycle.run()


def destroy_murkers(lifecycle: MurkerLifecycle) -> None:
    lifecycle.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')
    
    murker_parser = subparsers.add_parser('murker')

    murker_subparsers = murker_parser.add_subparsers(dest='murker_subparser')

    murker_deploy_parser = murker_subparsers.add_parser('deploy')
    murker_deploy_parser.add_argument("-ports", help="Ports of murkers to run (1 murker instance per port)", required=True, nargs='+', type=int)

    murker_deploy_parser = murker_subparsers.add_parser('destroy')

    return parser.parse_args()


if __name__ == '__main__':
    configure_logging(logging.INFO)

    args = parse_args()

    if args.subparser == 'murker':
        if args.murker_subparser == 'deploy':
            murkerLifecycle = MurkerLifecycle(args.ports)
            deploy_murkers(murkerLifecycle)
        elif args.murker_subparser == 'destroy':
            murkerLifecycle = MurkerLifecycle([])
            destroy_murkers(murkerLifecycle)


