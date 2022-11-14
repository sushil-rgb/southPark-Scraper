import time
import winsound
from tools import scrapeMe


start_time = time.time()

southpark_url = "https://www.southparkstudios.com/seasons/south-park/s6x4l8/season-10"
print(scrapeMe(southpark_url))


total_time = round(time.time()-start_time, 2)
time_in_secs = round(total_time)
time_in_mins = round(total_time/60)

print(f"{time_in_secs} seconds")


# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)
