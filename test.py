import serial

serialport = serial.Serial("/dev/ttyACM0", 115200, timeout=0.5)

while True:    
	s = raw_input("Type...\n")
	serialport.write(s)