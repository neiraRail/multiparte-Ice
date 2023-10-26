import sys, random
import smbus
from src.sum.SumHandler import SumHandler

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

Device_Address = 0x68 
bus = smbus.SMBus(1) 

class SensorNode():
    def __init__(self, id, sumHandler: SumHandler):
        self.id = id
        self.sumHandler = sumHandler
        self.secreto = None


        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
        
        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)
        
        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def read_raw_data(self, addr):
	    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

    
    def run(self):
        while True:
            acc_x = self.read_raw_data(ACCEL_XOUT_H)
            self.secreto = (acc_x >> 4) & 1
            St = self.sumHandler.sumar(self.secreto) % 2
            yield St

            if "--debug" in sys.argv:
                input("Presiona Enter para continuar...")