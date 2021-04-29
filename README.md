# Server Stats Monitor

*A script that grabs various stats from your server/computer and writes them to a JSON file where you can do whatever you want with the data.*

An example JSON output of this program can be found at https://pigeonburger.xyz/stats/server.json - reload it a couple of times to see it change with my server's load.

**A demonstration of this script working and then displaying stats can be found on the homepage of my website: https://pigeonburger.xyz**

<h2>Requirements:</h2>

- Python 3.6 or above
- psutil library (install using `pip install psutil`)
- A blank file created called `server.json` that only has `{}` inside it. (not doing this will result in the program erroring out)

The comments inside `servermon.py` explain what everything does, I recommend reading them.

**Adjustments to how the CPU temperature and fan speed are read will be REQUIRED as it can differ for each machine. See the comments inside `servermon.py`**