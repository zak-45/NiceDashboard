"""
a: zak-45
d : 16/06/2024
v : 1.0.0

Select chart to run

ex : runcharts devstats --dark

if you copy runcharts to devstats, this can be run in this way :

devstats --dark

"""
import subprocess
import sys
import argparse


dark_mode = ''


def select_exe():
    if sys.platform == 'linux':
        return './runcharts.bin'

    elif sys.platform == 'darwin':
        return './runcharts.app'

    else:
        return './runcharts.exe'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Display charts...')
    parser.add_argument('chart_name',
                        choices=['devstats', 'netstats', 'sysstats'],
                        metavar='chart',
                        type=str,
                        nargs='+',
                        help='Select a chart to display')

    parser.add_argument('--dev_ip',
                        required=False,
                        type=str,
                        help='List of IP addresses separated by comma : ip,ip2,ip3...')

    parser.add_argument('--dark',
                        action='store_true',
                        help='Activate dark mode '
                        )

    args = parser.parse_args()

    if args.dark is True:
        dark_mode = ['--dark']
    else:
        dark_mode = []

    ips = []
    ip_list = []
    if args.dev_ip is not None:
        ips = ['--dev_ip']
        ip_list = [args.dev_ip]

    if 'devstats' in args.chart_name:
        subprocess.Popen(["devstats"] + ips + ip_list + dark_mode,
                         executable=select_exe(),
                         text=True)

    if 'netstats' in args.chart_name:
        subprocess.Popen(["netstats"] + dark_mode,
                         executable=select_exe(),
                         text=True)

    if 'sysstats' in args.chart_name:
        subprocess.Popen(["sysstats"] + dark_mode,
                         executable=select_exe(),
                         text=True)
