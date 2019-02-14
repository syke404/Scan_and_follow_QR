# Scan_and_follow_QR
Scan for required QR code and then track it using Lucas-Kanade optical flow

Description:
scan_and_track.py contains a preliminary code which consists of two parts:

1) Scan and search for required QR code using Zbar library
2) Once the requred QR has been found, track its motion using Lucas-Kanade sparse optical flow

Notes:
Four corners of QR code are taken as points to be tracked in optical flow
Count mentions the number of frames optical flow should track the QR before scanning again

Improvements needed:
Presently, due to the design of QR codes, the tracked points slowly localize within the QR code (mostly due to pyramid). Either should tune LK parameters or should choose different points for tracking
