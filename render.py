from ipyleaflet import Map, Marker
import pynmea2
import serial
import io

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
last_time=00

while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        latitude=msg.latitude
        longitude=msg.longitude
        time=msg.timestamp
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
    except Exception as e:
        continue
    else:
        if last_time==00:
            center = (latitude, longitude)
            m = Map(center=center, zoom=15)
            marker = Marker(location=center, draggable=False)
            m.add_layer(marker);
            display(m)
            last_time=time
        else:
            marker.location=(latitude, longitude)
            last_time=time
