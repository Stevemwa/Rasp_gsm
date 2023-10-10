import serial
import time

class GSM:
    def __init__(self, port, baudrate, pin=None):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.pin = pin

        if self.pin:
            self.send_command('AT+CPIN=' + self.pin)
            self.wait_for_response()
	    print("initialized self")

    def send_command(self, command):
        self.serial_port.write(command.encode() + b'\r')

    def read_response(self, timeout=3):
        response = b''
        start_time = time.time()

        while True:
            char = self.serial_port.read(1)
            response += char

            if char == b'\n' or char == b'' or (time.time() - start_time) > timeout:
                break

            return response.decode().strip()

    def wait_for_response(self, timeout=3):
        response = self.read_response(timeout)
        start_time = time.time()
        while not response and (time.time() - start_time) <= timeout:
            response = self.read_response(timeout)
            time.sleep(1)
        return response

    def send_sms(self, recipient, message):
        self.send_command('AT+CMGF=1')
        self.wait_for_response()
        print("sent message")
        
        self.send_command('AT+CMGS="' + recipient + '"')

        self.wait_for_response()
        
        print("selected recipient")
        self.send_command(message)
        print("sent message")
        self.send_command(chr(26))  # End SMS
        self.wait_for_response()
    
    def send_text(self, recipient, message):
        self.send_command('AT+CMGF=1')
        #self.wait_for_response()
        time.sleep(3)
        print("selected message mode")
        
        self.send_command('AT+CMGS="' + recipient + '"')

        #self.wait_for_response()
        time.sleep(4)
        
        print("selected recipient")
        self.send_command(message)
        print("sent message")
        self.send_command(chr(26))  # End SMS
        #self.wait_for_response()

    def init_gprs(self, apn, username, password):
        self.send_command('AT+SAPBR=3,1,"APN","' + apn + '"')
        self.wait_for_response()

        self.send_command('AT+SAPBR=1,1')
        self.wait_for_response()

        self.send_command('AT+HTTPINIT')
        self.wait_for_response()

        self.send_command('AT+HTTPPARA="CID",1')
        self.wait_for_response()

        self.send_command('AT+HTTPPARA="URL","your_server_url"')
        self.wait_for_response()

        self.send_command('AT+HTTPPARA="CONTENT","application/json"')

    def send_gprs_data(self, data):
        self.send_command('AT+HTTPDATA=' + str(len(data)) + ',10000')
        self.wait_for_response()

        self.send_command(data)
        self.wait_for_response()

        self.send_command('AT+HTTPACTION=1')
        self.wait_for_response()

    def get_gps_coordinates(self):
        self.send_command('AT+CGPSPWR=1')  # Turn on GPS power
        time.sleep(1)
        self.send_command('AT+CGPSRST=0')  # Cold start GPS
        time.sleep(1)
        self.send_command('AT+CGPSSTATUS?') 
        response = self.wait_for_response()
        print("status check response: " + response)
        # self.send_command('AT+GPS=1') 

        while True:
            self.send_command('AT+CGPSINFO')
            response = self.wait_for_response()
            print(response)
            if response.startswith('+CGPSINFO:'):
                data = response.split(': ')[1].split(',')
                if len(data) >= 4:
                    latitude = data[0]
                    longitude = data[1]
                    altitude = data[3]
                    coordinates = "Latitude: " + str(latitude) + ", Longitude: " + str(longitude) + ", Altitude: " + str(altitude)
                    print(coordinates)
                    return coordinates
                    time.sleep(2)  # Update GPS data every 10 seconds

    def disconnect(self):
        self.serial_port.close()

