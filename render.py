from ipyleaflet import Map, Marker
import pynmea2
import serial
import io

ser = serial.Serial('/dev/ttyS1', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
last_time=00


def check_last_update(time,last_time):
    if nmea==last_nmea:
        return False
    else:
        return True

while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
    else:
        if check_last_update(time=msg.timestamp,last_time=last_time)==True:
            if last_time==00:
                m = Map(center=msg.latitude, msg.longitude, zoom=15)
                marker = Marker(location=center, draggable=False)
                m.add_layer(marker);
                display(m)
            else:
                marker.location=(msg.latitude, msg.longitude)
                last_time=msg.timestamp
