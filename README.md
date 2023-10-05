# Rasp_gsm
use gsm module to send messages, get gps location and send data via gprs
to use :
1)cd /path/to/your/desired/directory
2)git clone
3) create your main file i.e send_messages.py
4) Add the script below:
   
from gsm import GSM
import time

if __name__ == "__main__":
    gsm = GSM("/dev/ttyS0", 9600, None)
    gsm.send_text("+123456789", "Hi can we meet outside CE now!") 
    time.sleep(5)
    gsm.send_text("+123456789", "Hello can we meet outside CEDED now!")
    
    
