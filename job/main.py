import sys
import logging
import argparse
from typing import List

from job.murker import MurkerLifecycle
from job.murabi import MurabiLifecycle


DEFAULT_MURABI_PORT=8080


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

    murabi_parser = subparsers.add_parser(name='murabi')
    murabi_subparsers = murabi_parser.add_subparsers(dest='murabi_subparser')

    murabi_deploy_parser = murabi_subparsers.add_parser(name='deploy')
    murabi_deploy_parser.add_argument("-p", help="Port for murabi to listen on", required=False, type=int, default=DEFAULT_MURABI_PORT)

    murabi_deploy_parser = murabi_subparsers.add_parser(name='destroy')

    return parser.parse_args()


def parse_murabi_port(args: argparse.Namespace) -> int:
    if 'murabi_port' in args:
        return args.murabi_port

    return DEFAULT_MURABI_PORT


def run_murker_subcommand(args: argparse.Namespace) -> None:
    if 'ports' in args:
        ports = args.ports
    else:
        ports = []

    murabi_port = parse_murabi_port(args)

    murkerLifecycle = MurkerLifecycle(ports, murabi_port)

    if args.murker_subparser == 'deploy':
        deploy_murkers(murkerLifecycle)
    elif args.murker_subparser == 'destroy':
        destroy_murkers(murkerLifecycle)
    elif args.murker_subparser == 'ports':
        active_ports = murkerLifecycle.active_ports()
        print(active_ports)


def run_murabi_subcommand(args: argparse.Namespace) -> None:
    murabi_port = parse_murabi_port(args)

    murkerLifecycle = MurkerLifecycle([], murabi_port)
    murabi = MurabiLifecycle(murkerLifecycle, murabi_port)

    if args.murabi_subparser == 'deploy':
        murabi.run()
    elif args.murabi_subparser == 'destroy':
        murabi.kill()


if __name__ == '__main__':
    configure_logging(logging.INFO)
    args = parse_args()

    if args.subparser == 'murker':
        run_murker_subcommand(args)
    elif args.subparser == 'murabi':
        run_murabi_subcommand(args)
