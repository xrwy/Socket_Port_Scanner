from flask import Flask, render_template, request
import socket
from datetime import datetime

numbers_ = [str(num) for num in range(0,11)]
socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def main():
	return render_template('port_scanner.html')

@app.route('/port_scanner_result', methods = ['GET','POST'])
def portScannerResult():
	openPorts = []
	closedPorts = []

	if request.method == 'POST':
		ip_or_Host = request.form['address']
		portRange = request.form['port_range']

		if ip_or_Host == '' or portRange == '':
			return 'Do not leave the fields blank.'
		if len(portRange) == 1 or len(portRange) == 2:
			return 'Type the port range as specified. For Example : Start point-end point => 1-2000'
		elif '-' in portRange and len(portRange.split('-')) == 2:
			pass
		else:
			return 'Type the port range as specified. For Example : Start point-end point => 1-2000'


		range_ = portRange.split('-')
		len_ = ip_or_Host.split('.')
		if range_[0].isalpha() or range_[1].isalpha():
			return 'Error : Port Range Only Number.'
		if int(range_[0]) <= 0 or int(range_[1]) <= 0:
			return 'The starting or ending connection number cannot be 0 or less than 0.'
		if(int(range_[1])>= 65535):
			return 'End connection number cannot be greater than 65535.'
		if(int(range_[0]) >= int(range_[1])):
			return 'The start value point cannot be greater than the end value point. For Example : Start point-end point => 1-2000'
			
		if len(len_) == 4 and ip_or_Host[0].isalpha():
			ip_or_Host = socket.gethostbyname(ip_or_Host)
		else:
			if ip_or_Host[0] in numbers_:
				pass
			else:
				try:
					ip_or_Host = socket.gethostbyname(ip_or_Host)
				except:
					return 'Please provide a valid url.'

		try:
			# will scan ports between 1 to 65,535
			for port in range(int(range_[0]),int(range_[1]) + 1):
				socket.setdefaulttimeout(4)
				# returns an error indicator
				result = socket_.connect_ex((ip_or_Host,port))
				if result == 0:
					openPorts.append([port,str(datetime.now())])
				else:
					closedPorts.append([port,str(datetime.now())])
					socket_.close()
			
			if len(openPorts) == 0:
				openPorts = ''
			else:
				pass
			
			if len(closedPorts) == 0:
				closedPorts = ''
			else:
				pass

			return render_template('port_scanner_result.html', openPorts = openPorts, closedPorts = closedPorts)

		except KeyboardInterrupt:
			return 'Exiting Program !'
			#sys.exit()

		except socket.gaierror:
			return 'Hostname Could Not Be Resolved !'
			#sys.exit()
				
		except socket.error:
			return 'Server not responding !'
			#sys.exit()

	else:
		return 'For post requests only.'

if __name__ == '__main__':
	app.run(debug=True, port=5000)



