# -*- coding: utf-8 -*-
"""
@author: mdiechannel

20231023: Created
"""
# 
# For PYTHON 3+ with pySerial module installed
#

import serial

PORT = "COM7"
BAUD_RATE = 2400
BITS = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP_BITS = serial.STOPBITS_ONE
TIMEOUT = 1
ser = serial.Serial(PORT, BAUD_RATE, BITS, PARITY, STOP_BITS, timeout=TIMEOUT)
ser.setDTR(True)
ser.setRTS(False)
sample=[0] * 16
val=[]
table={ 0x7D:'0', 0x05:'1', 0x5B:'2', 0x1F:'3', 0x27:'4', 0x3E:'5', 0x7E:'6', 0x15:'7', 0x7F:'8', 0x3F:'9', 0x68:'L', 0x00:' ' }


try:
    while True:
        try: 
            byte=ord(ser.read())
        except TypeError:
            continue

        slot=(byte&0xF0)>>4
        if slot==1:
            val=[]
            sample=[0] * 16
        sample[slot]=byte&0xF

        if slot==14:
            if sample[2]&8:
                val.append('-')
            else:
                val.append(' ')
            for m in range(2,10,2):
                if (sample[m]&8) and m!=2:
                    val.append('.')
                s=((sample[m]&7)<<4)|(sample[m+1]);
                val.append(table[s])

                acdc='  '
                unit=''
                mult=''
                scale='[MANU]'
                measure='[     ]'
                rs232=''
                plus=''
                if sample[1]&1:
                    rs232='[RS232C]'
                if sample[1]&2:
                    scale='[AUTO]'
                if sample[1]&4:
                    acdc='DC'
                if sample[1]&8:
                    acdc='AC'


                if sample[10]&1:
                    measure='[DIODE]'
                if sample[10]&2:
                    mult='k'
                if sample[10]&4:
                    mult='n'
                if sample[10]&8:
                    mult='µ'
                    
                if sample[11]&1:
                    plus='[BEEP]'
                if sample[11]&2: 
                    mult='M'
                if sample[11]&4:
                    unit='%'
                if sample[11]&8:
                    mult='m'    
                    
                if sample[12]&1:
                    plus='[HOLD]'
                if sample[12]&2:
                    plus='[DELTA]'
                if sample[12]&4:
                    unit='Ω'
                if sample[12]&8:
                    unit='F'
                 
                if sample[13]&1:
                    plus='[BATT]'
                if sample[13]&2:
                    unit='Hz'
                if sample[13]&4:
                    unit='V'
                if sample[13]&8:
                    unit='A'

                if sample[14]&1:
                    unit='°C'
                if sample[14]&2:
                    units='N/A2'
                if sample[14]&4:
                    units='N/A3'
                if sample[14]&8:
                    units='N/A4'

            print("%s %s %s %s %s%s %s" %( measure,acdc,scale, ''.join(str(e) for e in val), mult, unit,plus));
        
except KeyboardInterrupt:
    print('Exit Key!')
    ser.close()