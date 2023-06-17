from ipyleaflet import Map, Marker
import pynmea2
import serial
import io
import gpxpy
import gpxpy.gpx
import signal
import sys

def signal_handler(sig, frame):
    gpx_file.write(gpx.to_xml())
    gpx_file.truncate()
    gpx_file.close()
    print("Quitting")
    sys.exit(0)

gpx_file = open('track.gpx', 'w')
gpx_file.seek(0)
gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

ser = serial.Serial('/dev/ttyACM1', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
last_time = 0

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        line = sio.readline().rstrip('\n')  # Remove newline character
        msg = pynmea2.parse(line)
        latitude = msg.latitude
        longitude = msg.longitude
        # altitude = msg.altitude
        # time = f"{msg.datestamp}T{msg.timestamp}Z"
    except serial.SerialException as e:
        # print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        # print('Parse error: {}'.format(e))
        continue
    except Exception as e:
        continue
    else:
        if last_time == 0:
            center = (latitude, longitude)
            m = Map(center=center, zoom=15)
            marker = Marker(location=center, draggable=False)
            m.add_layer(marker)
            display(m)
            last_time = time
            last_latitude=latitude
            last_longitude=longitude
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude, longitude))
        else:
            marker.location = (latitude, longitude)
            last_time = time
            if not last_latitude==latitude or not last_longitude==longitude:
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude, longitude))
                print("Added gpx point")
            last_latitude=latitude
            last_longitude=longitude
