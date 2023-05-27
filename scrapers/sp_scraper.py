from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from tools.tools import userAgents, select_yaml, create_path
from bs4 import BeautifulSoup
import pandas as pd


async def scrapeMe(url):
    season_number = url.split("-")[-1]
    scrape = select_yaml('sp')
    
    sp_dicts = []

    async with async_playwright() as p:        
        browser = await p.chromium.launch(headless = True, slow_mo = 0.5 * 1000)
        page = await browser.new_page(user_agent = await userAgents())
        print(f"Initiating the automation | Powered by Playwright.")
        
        await page.goto(url)
        
        show_more_button = await page.query_selector(scrape['show_more_button'])
        
        if show_more_button:
            await show_more_button.click()

        content = await page.content()
        await browser.close()
        
        soup = BeautifulSoup(content, 'lxml')
                
        for content in soup.select(scrape['main_content']):
            datas = {
                'Episode': (content.select_one(scrape['episode_num']).text.strip()).split("•")[-1].strip(),
                'Episode Name': content.select_one(scrape['episode_name']).text.strip(),
                'Episode Plot': content.select_one(scrape['episode_plot']).text.strip(),
                'Episode Air Date': content.select_one(scrape['episode_air_date']).text.strip(),
                'Episode Link': f"""https://www.southparkstudios.com{content.select_one(scrape['episode_link']).get('href')}""",
            }        
            
            sp_dicts.append(datas)
        
        df = pd.DataFrame(sp_dicts)
        
        await create_path("SouthPark database")
        
        df.to_excel(
            f"""Southpark database//South Park Season {season_number} database.xlsx""", index=False)
        print(f"Season {season_number} database saved.")

