# the_watcher
Watch for google searches and push to pushover app if finding anything

This was created to find a vinyl called "Cool" by "Broder John" which is rarely on sale.

If anything found (that is not in the blocked url-list) pushes to a [Pushover](https://pushover.net/) app.)

## Setup
Python external dependencies are ```googlesearch```.
Can be installed with pip:   
```pip3 install google```

### Credentials
Set up your pushover credentials in the file ```credentials.json``` from you pushover app.

### Cron
1 cron job1 are required for this to work
My setup is to run this on my raspberry pi.

Runs every day at 6:00
```0 6 * * * python3 /home/pi/projects/the_watcher/main.py```

## Contact
If you have any questions on how to set it up or other comments.   
Please contact me at [michael.sorsater@gmail.com](mailto:michael.sorsater@gmail.com)
