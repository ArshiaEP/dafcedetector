# dafcedetector
An automated Python script to detect real-time website defacement occurrences:
This tool is specifically designed to check desired websites using the Python Selenium library for notifying even small changes in website appearance.

![image](https://github.com/ArshiaEP/dafcedetector/assets/136557600/52a84316-f021-4df2-9da1-bb3c60d811e8)


## Features

- The ability to scan many URLs.(config_file.txt)
- Optimizing itself with host system hardware configurations(line#413).
- Support all alerting platforms like Slack,...(slack_alert function)
- Containing two verification methods:

  1-Screenshot

  2-Hash

  3-The combination of 1&2
- Saving defaced evidence with complete detail such as exact time, the website URL and screenshot.
- The ability to send an E-mail as an alert method using SMTP(send_email function).
- The ability to specify change tolerance in the source code(config_file.txt).
- Completely modular and customizable for different usages.
- The ability to set a blocklist for hash/screenshot checks.(config_file.txt)
- Containing a logging module for the console and a log file(need to be uncommented line#62).
- Containing a heartbeat mechanism for verifying the tool state.(Im_alive)

## Documentation

[Documentation]

- method description:

   1-Screenshot:

  in this method when you run the script, it will capture 2 screenshots in that directory which FDBshot is the first database shot that is not going to be replaced anymore cause it checks the file's existence before capturing it and the SECshot that will be replaced every time the script ran. finally, it compares these two captured screenshots using imagecompare library and returns two results containing "same?" which returns the boolean "percentage which is an integer showing the scale of changes".

  2-Hash:

  There is a hash script in this directory that takes a URL and returns a hash string that you should use in the config file as the hash DB then it will compare the live website hash with the database and return a boolean(hashresult).


## Installation


How To Config:

1-Install  [Python](https://www.python.org/downloads/)


2- install the requirement using CMD/Powershell:
```
pip install -r requirement.txt
```
3- Check the installed google chrome version and download the proper Chrome driver [here](https://chromedriver.chromium.org/downloads)

NOTE!!! The installed google chrome browser version and the driver must be the same and both the script file & Chromedriver need to be in the same directory(line#325).
Do not forget to change the default directory of the main script and also the path to Chromedriver(line#366-377-394).

4- Run hash.py to get the DBhash for each URL and add it to the config file

5- Set the custom tolerance for each URL 

6- Set the slack webhook for both health-check & deface-alert in the config file

7- To run, You can config a time schedule to run a bat file that locates and runs the main script or you can convert it to an exe and use it that way.

8-Enjoy :)
## Tested On

Tested On Windows 10,11 & Windows Server 2019

Script sends a heartbeat message after a complete & neat run.!
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Contact
If you had any comments, feedback or suggestions feel free to dm me on [discord](poltergeist#8351)

