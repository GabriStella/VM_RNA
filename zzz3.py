print("terzo file che non elimina tutto")
import time
from datetime import datetime, timedelta

start_time = datetime.now()
end_time = start_time + timedelta(minutes=2)

while datetime.now() < end_time:
    orario = datetime.now().strftime('%H:%M:%S')
    print(f"{orario} FACCIO COSE")
    time.sleep(3 * 10)
