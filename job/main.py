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
    
    murker_parser = subparsers.add_parser(name='murker')

    murker_subparsers = murker_parser.add_subparsers(dest='murker_subparser')

    murker_deploy_parser = murker_subparsers.add_parser(name='deploy')
    murker_deploy_parser.add_argument("-ports", help="Ports of murkers to run (1 murker instance per port)", required=True, nargs='+', type=int)
    murker_deploy_parser.add_argument("-murabi-port", help="Port of murabi to access", required=True, type=int)

    murker_subparsers.add_parser(name='destroy')
    murker_subparsers.add_parser(name='ports')

    return parser.parse_args()


def run_murker_subcommand(args: argparse.Namespace) -> None:
    if 'ports' in args:
        ports = args.ports
    else:
        ports = []

    if 'murabi_port' in args:
        murabi_port = args.murabi_port
    else:
        murabi_port = 8080

    murkerLifecycle = MurkerLifecycle(ports, murabi_port)

    if args.murker_subparser == 'deploy':
        deploy_murkers(murkerLifecycle)
    elif args.murker_subparser == 'destroy':
        destroy_murkers(murkerLifecycle)
    elif args.murker_subparser == 'ports':
        active_ports = murkerLifecycle.active_ports()
        print(active_ports)


if __name__ == '__main__':
    configure_logging(logging.INFO)
    args = parse_args()

    if args.subparser == 'murker':
        run_murker_subcommand(args)
