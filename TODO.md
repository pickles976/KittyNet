https://bbs.archlinux.org/viewtopic.php?id=202682


- [ ] Fix brightness issue
- [ ] Consolidate both processes into one

sudo apt-get -y install v4l-utils

v4l2-ctl -c white_balance_temperature_auto=0
v4l2-ctl -c exposure_auto_priority=0

python3 main.py start_capture --save-images=True --show-webcam=False --denoise=True --threshold=7.5

v4l2-ctl -l
