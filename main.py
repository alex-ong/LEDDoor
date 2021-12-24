from webcam_monitor.status import check_status
import time

if __name__ == '__main__':
    while True:
        print(check_status())
        time.sleep(0.5)