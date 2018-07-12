# icinga2_check_oom
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_oom.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_oom?ref=badge_shield)

Icinga2/Nagios check for Out of memory problems. ATM it check all dmesg output. If you want after check make it green again, you need to run dmesg -c.

```bash
usage: check_oom.py [-h] [-m {warning,critical,default}] [-v]

Check for OOM killer events

optional arguments:
  -h, --help            show this help message and exit
  -m {warning,critical,default}, --mode {warning,critical,default}
                        Mode of results for this check: warning, critical,
                        default
  -s, --short           If this option is specified, check ignores dmesg OOM
                          problems older then 24 hours
  -v, --verbose         Show verbose output from demsg about OOM killer events

check_oom.py: v.1.1 by Dmytro Prokhorenkov
```



## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_oom.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fl13t%2Ficinga2_check_oom?ref=badge_large)