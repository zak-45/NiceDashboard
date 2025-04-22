# Compilation mode, standalone everywhere
# nuitka-project: --nofollow-import-to=doctest
# nuitka-project: --nofollow-import-to=matplotlib
# nuitka-project: --noinclude-default-mode=error
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --onefile-windows-splash-screen-image={MAIN_DIRECTORY}/splash-screen.png

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
import os
import argparse
import tkinter as tk

# disable not used costly import (from nicegui)
os.environ['MATPLOTLIB'] = 'false'


def select_exe():
    """ Absolute path of running script """
    return os.path.abspath(sys.argv[0])


def copy_exe():
    if sys.platform == 'linux':
        os.rename('./NiceDashboard/runcharts-Linux.bin', './NiceDashboard/runcharts.bin')

    elif sys.platform == 'darwin':
        os.rename('./NiceDashboard/runcharts-macOS.app', './NiceDashboard/runcharts.app')

    else:
        os.rename('./NiceDashboard/runcharts-Windows.exe', './NiceDashboard/runcharts.exe')


if __name__ == '__main__':
    # packaging support (compile)
    from multiprocessing import freeze_support  # noqa

    freeze_support()  # noqa

    # test to see if executed from compiled version
    # instruct user to go to runcharts folder to execute program
    if "NUITKA_ONEFILE_PARENT" in os.environ:

        def on_ok_click():
            # Close the window when OK button is clicked
            root.destroy()

        copy_exe()  # copy exe file

        # Create the main window
        root = tk.Tk()
        root.title("WLEDVideoSync Information")
        root.geometry("800x460")  # Set the size of the window
        root.configure(bg='#657B83')  # Set the background color

        # Define the window's contents
        info_text = ("Extracted executable to NiceDashboard folder.....\n\n \
        You can safely delete this file after extraction finished to save some space.\n \
        This is a portable version, nothing installed on your system and can be moved where wanted.\n\n \
        -------------------------------------------------------------------------------------------------\n \
        THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,\n \
        INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n \
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\n \
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,\n \
        DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n \
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n \
        -------------------------------------------------------------------------------------------------\n ")

        info_label = tk.Label(root, text=info_text, bg='#657B83', fg='white', justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)

        # Create the OK button
        ok_button = tk.Button(root, text="Ok", command=on_ok_click, bg='gray', fg='white')
        ok_button.pack(pady=10)

        # Start the Tkinter event loop
        root.mainloop()
        sys.exit()

    parser = argparse.ArgumentParser(description='Display charts...')
    parser.add_argument('chart_name',
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
