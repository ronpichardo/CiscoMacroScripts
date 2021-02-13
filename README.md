# CiscoMacroScripts
Scripts for interfacing with Cisco CE's API for configuration 

## Overview
Using a handful of scripts that assist with handling certain configurations or getting status of devices.  The results are then saved to a file in csv format for later viewing.
Results saved as per the image
<img width="622" alt="resultsreturned2" src="https://user-images.githubusercontent.com/63974878/107840318-c4811480-6d7f-11eb-89de-310d0d55abcd.png">

Example:

<img width="504" alt="MacroRunning" src="https://user-images.githubusercontent.com/63974878/107840208-d910dd00-6d7e-11eb-8dde-33220ba51efe.png">

## Installation
Requirements - XMLtoDict, Requests
```shell
$ git clone https://github.com/ronpichardo/CiscoMacroScripts.git
$ cd CiscoMacroScripts
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
<img width="652" alt="GitInstalled" src="https://user-images.githubusercontent.com/63974878/107840181-9b13b900-6d7e-11eb-8390-995d638b0ac7.png">

## Usage
Update lines 10 and 11 with the username and password used for the devices
<img width="817" alt="userandpass" src="https://user-images.githubusercontent.com/63974878/107840248-360c9300-6d7f-11eb-9590-1d367bf1e3e1.png">
