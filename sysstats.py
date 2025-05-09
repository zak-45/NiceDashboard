"""
a: zak-45
d : 16/06/2024
v : 1.0.0

System Utilization Chart

ex : runcharts sysstats --dark

if you copy runcharts to sysstats, this can be run in this way :

sysstats --dark

"""
import time
import os
# disable not used costly import (from nicegui)
os.environ['MATPLOTLIB'] = 'false'

from datetime import datetime
import psutil
from nicegui import app, ui

import argparse


class SysCharts:
    """
    Create charts from system datas
    CPU, RAM, ...
    """
    cpu_warning: int = 60
    memory_warning: int = 85
    free_warning: int = 10

    def __init__(self, dark: bool = False):
        self.cpu_chart = None
        self.load_chart = None
        self.memory_chart = None
        self.disk_chart = None
        self.chart_refresh_s = 2
        self.sys_data_timer = []
        self.cpu_data_timer = []
        self.sys_interval = 5
        self.cpu_interval = 2
        self.timestamps = []

        self.gauge_data = [
            {
                'value': 20,
                'name': 'One Minute',
                'title': {
                    'offsetCenter': ['0%', '-70%']
                },
                'detail': {
                    'valueAnimation': 'true',
                    'offsetCenter': ['0%', '-50%']
                }
            },
            {
                'value': 40,
                'name': 'Five Minutes',
                'title': {
                    'offsetCenter': ['0%', '-10%']
                },
                'detail': {
                    'valueAnimation': 'true',
                    'offsetCenter': ['0%', '10%']
                }
            },
            {
                'value': 60,
                'name': 'Fifteen Minutes',
                'title': {
                    'offsetCenter': ['0%', '50%']
                },
                'detail': {
                    'valueAnimation': 'true',
                    'offsetCenter': ['0%', '70%']
                }
            }
        ]

        """ ui design """
        with ui.row().classes('no-wrap'):
            self.notify = ui.switch('Notification')
            self.notify.value = True
            self.dark_switch = ui.switch('Dark Mode')
            self.dark_mode = ui.dark_mode(on_change=self.change_chart_mode)
            if dark is True:
                self.dark_switch.value = True

        self.create_charts()
        self.log = ui.log(max_lines=30).classes('w-full h-20 bg-black text-white')
        with ui.row():
            ui.button('Clear all', on_click=self.clear)
            ui.button('Pause 5s', on_click=self.pause_chart)
            ui.button('STOP', on_click=app.stop)
        self.log.push("Auto refresh time: " + str(self.chart_refresh_s) + "sec")

        """ timers """
        self.cpu_data_timer.append(ui.timer(self.cpu_interval, lambda: self.cpu_datas()))
        self.sys_data_timer.append(ui.timer(self.sys_interval, lambda: self.sys_datas()))
        self.chart_sys_timer = ui.timer(self.chart_refresh_s, lambda: self.update_charts())

        app.native.window_args['resizable'] = True
        app.native.start_args['debug'] = False
        app.native.settings['ALLOW_DOWNLOADS'] = True

        ui.run(native=True,
               window_size=(800, 600),
               fullscreen=False,
               reload=False,
               title='System Stats',
               favicon='favicon.ico'
               )

    def create_charts(self):
        self.cpu_chart = ui.echart({
            'darkMode': 'false',
            'legend': {
                'show': 'true',
                'data': []
            },
            'title': {
                'text': "CPU"
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'xAxis': {
                'type': 'category',
                'data': []
            },
            'yAxis': {
                'type': 'value', 'axisLabel': {':formatter': 'value =>  value + " % " '}
            },
            'series': [{
                'data': [],
                'name': 'CPU %',
                'areaStyle': {'color': '#535894', 'opacity': 0.5},
                'type': 'line'
            }]
        }).on('dblclick', lambda: self.pause_chart()).classes('w-full h-45')

        self.memory_chart = ui.echart({
            'title': {
                'text': "Memory Utilization"
            },
            'xAxis': {
                'type': 'category',
                'data': []
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'yAxis': {
                'min': 0,
                'max': 100,
                'type': 'value'
            },
            'series': [{
                'data': [],
                'type': 'bar',
                'showBackground': 'true',
                'backgroundStyle': {
                    'color': 'rgba(220, 220, 220, 0.8)'
                }
            }]
        }).on('dblclick', lambda: self.pause_chart()).classes('w-full h-45')

        with ui.row().classes('w-full no-wrap'):
            with ui.card().classes('w-1/2'):
                self.disk_chart = ui.echart({
                    'darkMode': 'false',
                    'title': {
                        'text': "Disk Space Utilization",
                        'left': 'center'
                    },
                    'legend': {
                        'orient': 'vertical',
                        'left': 'left'
                    },
                    'tooltip': {
                        'trigger': 'item'
                    },
                    'series': [{
                        'name': 'Disk Space',
                        'data': [
                            {'name': '% used', 'value': 0},
                            {'name': '% free', 'value': 100}
                        ],
                        'emphasis': {
                            'itemStyle': {
                                'shadowBlur': 10,
                                'shadowOffsetX': 0,
                                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                            }},
                        'type': 'pie',
                        'radius': '50%',
                        'showBackground': 'true',
                        'backgroundStyle': {
                            'color': 'rgba(220, 220, 220, 0.8)'
                        }
                    }]
                }).on('dblclick', lambda: self.pause_chart()).classes('w-full h-45')

            with ui.card().classes('w-1/2'):
                self.load_chart = ui.echart(
                    {
                        'title': {
                            'text': "Load Averages"
                        },
                        'series': [
                            {
                                'type': 'gauge',
                                'startAngle': 180,
                                'endAngle': -270,
                                'pointer': {
                                    'show': 'false',
                                    'width': 0
                                },
                                'progress': {
                                    'show': 'true',
                                    'overlap': 'false',
                                    'roundCap': 'true',
                                    'clip': 'false',
                                    'itemStyle': {
                                        'borderWidth': 1,
                                        'borderColor': '#464646'
                                    }
                                },
                                'axisLine': {
                                    'lineStyle': {
                                        'width': 10
                                    }
                                },
                                'splitLine': {
                                    'show': 'false',
                                    'distance': 0,
                                    'length': 0
                                },
                                'axisTick': {
                                    'show': 'false',
                                    'length': 0
                                },
                                'axisLabel': {
                                    'show': 'false',
                                    'distance': 0,
                                    'fontSize': 8
                                },
                                'data': self.gauge_data,
                                'title': {
                                    'fontSize': 14
                                },
                                'detail': {
                                    'width': 50,
                                    'height': 14,
                                    'fontSize': 14,
                                    'color': 'inherit',
                                    'borderColor': 'inherit',
                                    'borderRadius': 20,
                                    'borderWidth': 1,
                                    'formatter': '{value}%'
                                }
                            }
                        ]
                    }).classes('min-w-full min-h-80')

    def pause_chart(self):
        ui.notify('Refresh has been paused for 5s ')
        self.log.push('Pause for 5 seconds')
        time.sleep(5)

    def update_charts(self):
        self.memory_chart.update()
        self.cpu_chart.update()
        self.disk_chart.update()
        self.load_chart.update()

        if self.dark_switch.value is True:
            self.dark_mode.enable()
        else:
            self.dark_mode.disable()

    def clear(self):
        self.memory_chart.options['series'][0]['data'].clear()
        self.cpu_chart.options['series'][0]['data'].clear()
        self.disk_chart.options['series'][0]['data'][0]['value'] = 0
        self.disk_chart.options['series'][0]['data'][1]['value'] = 0

        self.memory_chart.options['xAxis']['data'] = []
        self.cpu_chart.options['xAxis']['data'] = []

        self.log.clear()
        self.log.push("Auto refresh time: " + str(self.chart_refresh_s) + "sec")

    async def sys_datas(self):
        now = datetime.now()
        date_time_str = now.strftime("%H:%M:%S")
        load = self.get_load_averages()

        memory_data = self.get_memory()
        disk_free_data = round(100 - self.get_disk(), 2)
        disk_used_data = round(self.get_disk(), 2)

        self.memory_chart.options['series'][0]['data'].append(memory_data)
        self.disk_chart.options['series'][0]['data'][0]['value'] = disk_used_data
        self.disk_chart.options['series'][0]['data'][1]['value'] = disk_free_data
        self.gauge_data[0]['value'] = round(load['one_min'], 2)
        self.gauge_data[1]['value'] = round(load['five_min'], 2)
        self.gauge_data[2]['value'] = round(load['fifteen_min'], 2)
        self.load_chart.options['series'][0]['data'] = self.gauge_data

        self.memory_chart.options['xAxis']['data'].append(date_time_str)

        if memory_data >= SysCharts.memory_warning:
            if self.notify.value is True:
                ui.notify('High memory utilization', type='negative')
        if disk_free_data <= SysCharts.free_warning:
            if self.notify.value is True:
                ui.notify('High disk utilization', type='negative')

    async def cpu_datas(self):
        now = datetime.now()
        date_time_str = now.strftime("%H:%M:%S")

        cpu_data = self.get_cpu()

        self.cpu_chart.options['series'][0]['data'].append(cpu_data)
        self.cpu_chart.options['xAxis']['data'].append(date_time_str)

        if cpu_data >= SysCharts.cpu_warning:
            if self.notify.value is True:
                ui.notify('High CPU utilization', type='negative')

    @staticmethod
    def get_cpu():
        cpu = psutil.cpu_percent(interval=1, percpu=False)
        return cpu

    @staticmethod
    def get_load_averages():
        load_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
        mapped_avg = {"one_min": load_avg[0], "five_min": load_avg[1], "fifteen_min": load_avg[2]}
        return mapped_avg

    @staticmethod
    def get_memory():
        mem = psutil.virtual_memory()
        return mem[2]

    @staticmethod
    def get_disk():
        disk = psutil.disk_usage('/')
        return disk[3]

    def change_chart_mode(self):
        """toggle dark mode on chart"""
        self.cpu_chart.options.update({'darkMode': not self.cpu_chart.options['darkMode']})
        self.disk_chart.options.update({'darkMode': not self.cpu_chart.options['darkMode']})
        self.cpu_chart.update()  # render on client
        self.disk_chart.update()  # render on client


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display System utilization chart...')

    parser.add_argument('--dark',
                        action='store_true',
                        help='Activate dark mode '
                        )

    args = parser.parse_args()
    SysCharts(dark=args.dark)
