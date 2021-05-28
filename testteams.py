import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import xmltodict
from multiprocessing.pool import ThreadPool

import sys, csv, logging, time

codec_ips = []
username = ''
password = ''
meeting_id = ''

def testXml(ip):

  try:
    test_xml = requests.get(f'http://{ip}/getxml?location=/Configuration/SystemUnit/Name', auth=(username, password), verify=False, timeout=5)
    xml_result = xmltodict.parse(test_xml.text)

    return { 'msg': xml_result['Configuration']['SystemUnit']['Name']['#text'] }

  except requests.exceptions.ConnectTimeout:
    print(f'[ConnectTimeoutError] - getting System Name on IP: {ip}')
    return { 'msg': None }
  except requests.exceptions.ConnectionError:
    print(f'[ConnectionError] getting System Name on IP: {ip}')
    return { 'msg': None }
  except TimeoutError:
    print(f'[TimeoutError] getting System Name on IP: {ip}')
    return { 'msg': None }
  except Exception as e:
    print(f'[ExceptionError] getting System Name on IP: {ip} - {e}')
    return { 'msg': 'NoNameFb' }

def getXml(ip, x_path):

  get_xml = requests.get(f'http://{ip}/getxml?location=/{x_path}', auth=(username, password), verify=False, timeout=5)
  xml_result = xmltodict.parse(get_xml.text)

  return xml_result

def putXml(ip, x_path):

  headers = { 'Content-Type': 'text/xml; charset=UTF-8' }
  put_xml = requests.post(f'http://{ip}/putxml', data=x_path, headers=headers, auth=(username, password), verify=False, timeout=5)

  xml_result = xmltodict.parse(put_xml.text)
  return xml_result

def autobotted(ip):

  system_type = getXml(ip, 'Configuration/SystemUnit/Name')

  system_name = system_type['Configuration']['SystemUnit']['Name']['#text']

  payload = '''
  <Command>
    <Macros>
      <Macro>
        <Get></Get>
      </Macro>
    </Macros>
  </Command>'''

  macro_status = putXml(ip, payload)

  running_macros = macro_status['Command']['MacroGetResult']['Macro']
  
  try:
    macro_name = running_macros['Name']
    macro_status = running_macros['Active']
    print(f'Macro is loaded on {system_name}, current state of teamsdialer is: {macro_status}')
  except:
    for macro in running_macros:
      macro_name = macro['Name']
      macro_status = macro['Active']
      if macro_name == 'teamsdialer':
        print(f'Macro is loaded on {system_name}, current state of teamsdialer is: {macro_status}')
    # else:
    #   print('teamsdialer Macro is not loaded onto this system, please load Macro on ' + ip)
    #   pass

  payload=f'''
<Command>
  <UserInterface>
    <Extensions>
      <Panel>
        <Clicked>
          <PanelId>msteamsdialer</PanelId>
        </Clicked>
      </Panel>
    </Extensions>
  </UserInterface>
</Command>'''
  
  click_panel = putXml(ip, payload)
  
  status_msg = click_panel['Command']['PanelClickedResult']['@status']
  if status_msg == 'OK':
    print(f'{system_name} - PanelButton was Clicked Successfully')
  else:
    error_msg = click_panel['Command']['PanelClickedResult']['Reason']
    print(f'{status_msg} Clicking Button on: {ip} - {error_msg}')

  payload = f'''
<Command>
  <UserInterface>
    <Message>
      <TextInput>
        <Response>
          <Text>{meeting_id}</Text>
          <FeedbackId>dialerId</FeedbackId>
        </Response>
      </TextInput>
    </Message>
  </UserInterface>
</Command>'''

  call_button = putXml(ip, payload)

  payload = f'''<Command><Audio><Volume><Mute></Mute></Volume></Audio></Command>'''
  kill_audio = putXml(ip, payload)
  payload = f'''<Command><Audio><Microphones><Mute></Mute></Microphones></Audio></Command>'''
  mute_call = putXml(ip, payload)

  time.sleep(15)

  payload = f'''<Command>  <Call>    <Disconnect></Disconnect>  </Call></Command>'''

  disconnect_call = putXml(ip, payload)

  if disconnect_call['Command']['CallDisconnectResult']['@status'] != 'OK':
    print(f'{system_name} unable to disconnect')

  print(system_name + ' Call Succeeded, now Disconnecting from the call...')
  
def main():
  
  working_codecs = []
  try:

    for ip in codec_ips:
      system_name = testXml(ip)
      if system_name['msg'] is not None:
        working_codecs.append(ip)

    pool = ThreadPool(5)
    results = pool.map(autobotted, working_codecs)
    pool.close()
    pool.join()

    return results
  except Exception as e:
    print(e)

if __name__ == "__main__":

  # Save results of what is in the CSV file into the codecs_ip array
  try:
    
    csv_filename = sys.argv[1]
    meeting_id = sys.argv[2]

    if '.csv' not in csv_filename:
      csv_filename += '.csv'
    with open(csv_filename) as csv_file:
      csv_reader = csv.reader(csv_file)
      for ip in csv_reader: 
        codec_ips.append(ip[0])

  except IndexError:
    print('Required arguments not found.\n\nUsage: python3 main.py <filename>.csv <meetingid>\n')
  except FileNotFoundError:
    print('No file found by the name: ' + csv_filename)

  main()
