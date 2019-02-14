'''
QR Code Scanner and Lucas-Kanade Tracker
---------
Scans QR code using zbar library and if the chosen one, then tracks it using Lucas Kanade optical flow
Usage : scan_and_track.py
keys  : ESC - exit
---------
'''

import numpy as np
import cv2
from pyzbar import pyzbar

#Parameters for Lucas-Kanade sparse flow
lk_params = dict(winSize = (30,30),
                 maxLevel = 1,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

#Function to scan QR codes
def scan_QR(image):
	
	status = 0	
	x1 = 0
	y1 = 0
	w1 = 0
	h1 = 0

	barcodes = pyzbar.decode(image)
	
	for barcode in barcodes:
	
		(x,y,w,h) = barcode.rect
		cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)

		#note: barcodeData contains the information
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		#Required barcodes to be tracked
		if barcodeData in ['tel:07777777777', 'tel:077777777777', 'Syke404']:
			status = 1
			x1 = x
			y1 = y
			w1 = w
			h1 = h

		text = "{} ({})".format(barcodeData, barcodeType)
		
		cv2.putText(image, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

	return image, status, x1,y1,w1,h1

'''--------------Main code-------------'''

cap = cv2.VideoCapture(0)
tracking = 0
count = 0

while True:

	if tracking == 0:
		ret, frame = cap.read()
		height, width, channels = frame.shape
		scanned_image, track_status, x, y, w, h= scan_QR(frame)
		cv2.imshow("Frame", scanned_image)
		if track_status == 1:
			tracking = 1
			old_points = np.array([[x, y], [x+w, y], [x, y+h], [x+w, y+h]], dtype = np.float32)

	if tracking ==1:
		count += 1
		ret, frame2 = cap.read()		
		new_points, status, error = cv2.calcOpticalFlowPyrLK(frame, frame2, old_points, None, **lk_params)
		print(new_points)
		cv2.rectangle(frame2, (new_points[0][0], new_points[0][1]), (new_points[3][0], new_points[3,1]), (255,0,0),3)
		text = "Tracking"
		cv2.putText(frame2, text, (height-100, width-100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
		cv2.imshow("Tracked Frame", frame2)

		frame = frame2.copy()
		old_points = new_points

		# Number of frames before scanning again (good optical flow can have a larger count value)
		if count == 100:
			count = 0
			tracking = 0

		
	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()

