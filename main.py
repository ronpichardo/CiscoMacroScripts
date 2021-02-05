import requests, xmltodict
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import csv, json

from multiprocessing.pool import ThreadPool

# This empty array will store the IP addresses that are found in a csv or txt file
codec_ips = []
username = ''
password = ''

# ToDo for saving results of the script
# results_file = open('results.csv', 'a')

with open('devices.csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		codec_ips.append(row[0])

def getXmlRequest(ip_addr, x_path):
	
	r = requests.get(f'http://{ip_addr}/getxml?location={x_path}', auth=(username, password), verify=False, timeout=5)
	xml_result = xmltodict.parse(r.text)
	return xml_result

def putXmlRequest(ip_addr, x_path):

	headers = { 'Content-Type': 'text/xml; charset=UTF-8' }
	r = requests.post(f'http://{ip}/putxml', data=x_path, headers=headers, auth=(username, password), verify=False, timeout=5)
	xml_result = xmltodict.parse(r.text)
	return xml_result

def gather_info(ip):

	system_name = getXmlRequest(ip, '/Configuration/SystemUnit/Name')
	system_name = system_name['Configuration']['SystemUnit']['Name']['#text']
	print(system_name)

	#Check cameratype cmd: xstatus cameras camera model	
	camera_type = getXmlRequest(ip, 'Status/Cameras/Camera/Model')
	camera_type = camera_type['Status']['Cameras']['Camera']['Model']
	print(camera_type)

	#Check for a Touch10 cmd: xstatus Peripherals
	panel_type = getXmlRequest(ip, 'Status/Peripherals/ConnectedDevice')
	panel_type = panel_type['Status']['Peripherals']['ConnectedDevice']['Name']
	print(panel_type)

	# Check current macros on system cmd: xcommand Macros Macro Get
	payload = '''
	<Command>
		<Macros>
			<Macro>
				<Get></Get>
			</Macro>
		</Macros>
	</Command>'''

	macro_stats = putXmlRequest(ip, payload)
	macro_stats = macro_stats['Command']['MacroGetResult']['Macro']
	
	try:
		print(macro_stats['Name'])
	except:
		print(f'Number of Macros: {len(macro_stats)}')
		for macro in macro_stats:
			print(macro['Name'])

	# Check the status of loaded macros cmd: xcommand Macros Runtime Status
	payload = '''
	<Command>
		<Macros>
			<Runtime>
				<Status></Status>
			</Runtime>
		</Macros>
	</Command>'''

	macro_activity = putXmlRequest(ip, payload)
	macro_activity = macro_activity['Command']['RuntimeStatusResult']
	print(macro_activity['ActiveMacros'], macro_activity['Running'])

	# Get the SoftwareVersion of the codec cmd: xstatus Status SystemUnit Software Version
	software_version = getXmlRequest(ip, 'Status/SystemUnit/Software/Version')
	software_version = software_version['Status']['SystemUnit']['Software']['Version']
	print(software_version)

	# ToBeImplemented, outputting to a file for the results
	# results_file.write(system_name + ',' + ip + ',' + software_version + ',' + camera_type + ',' + panel_type)
	print()


def main():

	pool = ThreadPool(3)
	results = pool.map(gather_info, codec_ips)
	pool.close()
	pool.join()

	return results

if __name__ == '__main__':

	for ip in codec_ips:
		try:
			system_name = getXmlRequest(ip, '/Configuration/SystemUnit/Name')

		except requests.exceptions.ConnectionError:
			print('[ConnectionError] - ' + ip)
			codec_ips.remove(ip)
		except requests.exceptions.ConnectTimeout:
			print('[ConnectionTimeoutError] - ' + ip)
			codec_ips.remove(ip)
		except TimeoutError:
			print('[TimeoutError] - ' + ip)
			codec_ips.remove(ip)
		except Exception as e:
			print(f'[Exception] - {e} on {ip}')
			codec_ips.remove(ip)


	main()