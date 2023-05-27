from scrapers.sp_scraper import scrapeMe
import asyncio
import time


if __name__ == "__main__":
    start_time = time.time()

    
    async def main():
        southpark_url = "https://www.southparkstudios.com/seasons/south-park/wcj3pl/season-22"
        test = await scrapeMe(southpark_url)
        return test
    
    
    asyncio.run(main())
    total_time = round(time.time()-start_time, 2)
    time_in_secs = round(total_time)
    time_in_mins = round(total_time/60)

    print(f"{time_in_secs} seconds.")

