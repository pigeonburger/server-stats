# Server stats monitor by Pigeonburger
# https://github.com/pigeonburger/server-stats


import psutil, json
from typing import List, Union

# THIS IS JUST A THING THAT ACCURATELY CONVERTS BYTES TO MB, GB, TB ETC - THE ACTUAL SERVER STATS PART IS BELOW THIS CLASS
# This method of accurately converting bytes to a human-readable string was taken from https://stackoverflow.com/a/63839503
class RenderBytes:
    METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005]
    PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"]

    @staticmethod
    def format(num: Union[int, float], metric: bool=False, precision: int=1) -> str:

        assert isinstance(num, (int, float)), "num must be an int or float"
        assert isinstance(metric, bool), "metric must be a bool"
        assert isinstance(precision, int) and precision >= 0 and precision <= 3, "precision must be an int (range 0-3)"

        unit_labels = RenderBytes.METRIC_LABELS if metric else RenderBytes.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - RenderBytes.PRECISION_OFFSETS[precision]

        is_negative = num < 0
        if is_negative:
            num = abs(num)

        for unit in unit_labels:
            if num < unit_step_thresh:
                break
            if unit != last_label:
                num /= unit_step

        return RenderBytes.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)


## THIS IS THE ACTUAL SERVER STATS PART ##

# INFINITELY RUN THIS (every 2 seconds because it takes 2 seconds to analyze CPU)
while True:
    with open("server.json", 'r+') as server_stats: # The output of this program is written to server.json by default.

        # Check CPU usage by analyzing for 2 seconds
        cpuper = psutil.cpu_percent(interval=2)

        # Get percentage of RAM in use
        totalmem = str(psutil.virtual_memory().percent)

        # Check how much total storage you have, and how much is taken up. For Windows, change it from '/' to 'C:\\'
        store = psutil.disk_usage('/')
        totalstore = RenderBytes.format(store.total, metric=True, precision=2)
        usedstore = RenderBytes.format(store.used, metric=True, precision=2)

        # Get CPU temperature (this does not work universally, you will need to find the name of your CPU temp sensor and replace it here)
        temperature = psutil.sensors_temperatures()['k10temp'][0].current
        cputemp = str(round(temperature, 1))+"&deg;C"
        cputemp_butforamericans = str(round((temperature * 1.8) + 32, 1))+"&deg;F"

        # Get CPU cooler fan speed (again, this needs to be adjusted like CPU temperature)
        fanspeed = str(psutil.sensors_fans()['nct6779'][1].current)+"RPM"

        cpu = f"{cpuper}%"
        ram = f'{totalmem}%'
        storage = f'{usedstore} of {totalstore}'

        # Write the data to a JSON file
        data = json.load(server_stats)

        data['cpu'] = cpu
        data['ram'] = ram
        data['storage'] = storage
        data['temperature'] = cputemp
        data['temperature_but_its_for_the_americans_instead'] = cputemp_butforamericans
        data['fan'] = fanspeed

        server_stats.seek(0)
        json.dump(data, server_stats)
        server_stats.truncate()
