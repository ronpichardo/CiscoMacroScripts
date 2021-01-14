# CiscoMacroScripts
Scripts for interfacing with Cisco CE's API for configuration 

## Overview
Using a handful of scripts that assist with handling certain configurations or getting status of devices.  The results are then saved to a file in csv format for later viewing.

Example:
- Checking for the status of SpeakerTrack if it is on/off.  Option to turn on SpeakerTrack if it is off
- Connect and get the Product type (Cisco Webex Mini, Cisco Webex Pro, etc) and Camera Type (P60, QuadCam, etc)

## Installation
Requirements - XMLtoDict, Requests
```shell
$ git clone https://github.com/ronpichardo/CiscoMacroScripts.git
$ cd CiscoMacroScripts
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
