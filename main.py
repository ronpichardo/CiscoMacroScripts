import requests, xmltodict
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import csv

# This empty array will store the IP addresses that are found in a csv or txt file
codec_ips = []
username = ''
password = ''

with open('devices.csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		codec_ips.append(row[0])

def getXmlRequest(ip_addr, x_path):
	print(ip_addr, x_path)

def putXmlRequest(ip_addr, x_path):
	print(ip_addr, x_path)


for ip in codec_ips:
	#Check cameratype cmd: xstatus cameras camera model	
	print(ip)
	postUrl = f'http://{ip}/getxml?location=/Status/Cameras/Camera'
	headers = { 'Content-Type': 'text/xml; charset=UTF-8' }

	checkCamera = requests.get(postUrl, auth=(username, password), headers=headers, verify=False, timeout=5)
	xml_result = xmltodict.parse(checkCamera.text)
	camera_type = xml_result['Status']['Cameras']['Camera']['Model']

	print(camera_type)

	#Check for a Touch10 cmd: xstatus Peripherals
	postUrl = f'http://{ip}/getxml?location=/Status/Peripherals/ConnectedDevice'
	headers = { 'Content-Type': 'text/xml; charset=UTF-8' }

	check_touch = requests.get(postUrl, auth=(username, password), headers=headers, verify=False, timeout=5)
	xml_result = xmltodict.parse(check_touch.text)
	panel_type = xml_result['Status']['Peripherals']['ConnectedDevice']['Name']

	print(panel_type)

	# Check current macros on system
	postUrl = f'http://{ip}/putxml'
	headers = { 'Content-Type': 'text/xml; charset=UTF-8' }
	payload = '''
<Command>
	<Macros>
		<Macro>
			<Get></Get>
		</Macro>
	</Macros>
</Command>'''

	#If using Command/Macros/Runtime/Status
	#OrderedDict([('Command', OrderedDict([('RuntimeStatusResult', OrderedDict([('@status', 'OK'), ('ActiveMacros', '1'), ('Crashes', '0'), ('Running', 'True')]))]))])
	macro_stats = requests.post(postUrl, auth=(username, password), data=payload, headers=headers, verify=False, timeout=5)

	xml_result = xmltodict.parse(macro_stats.text)
	macro_name = xml_result['Command']['MacroGetResult']['Macro'][0]['Name']

	print(macro_name)


