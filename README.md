# Rasp_gsm
Use of a  gsm sim module to send messages, get gps location and send data via gprs.
Applicable in making a tracking device or remote controlling of the raspberry pi or a security system.
to use :

1) cd ``` /path/to/your/desired/directory```


2) clone the repository
```     
git clone https://github.com/Stevemwa/Rasp_gsm.git
```

3) create your main file i.e ```send_messages.py```

   
5) Add the script below:
   
```python
from gsm import GSM
import time

if __name__ == "__main__": 
    gsm = GSM("/dev/ttyS0", 9600, None)
    gsm.send_text("+123456789", "Hi can we meet outside CE now!")
    time.sleep(5)
    coordinates=gsm.get_gps_coordinates()
    gsm.send_text("+123456789", coordinates)
    
```
