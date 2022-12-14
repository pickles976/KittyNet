
### TODO:
- [x] Fix brightness issue
- [x] Get working with threshold

### Compensating for white balance adjustment
v4l2-ctl -l

v4l2-ctl -c white_balance_temperature_auto=0
v4l2-ctl -c exposure_auto_priority=0

### Running with commands
python3 main.py start_capture --save-images=True --show-webcam=False --denoise=True --threshold=10.0
