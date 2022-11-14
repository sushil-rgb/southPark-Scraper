import random
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd


def userAgents():
    with open('user-agents.txt') as f:
        agents = f.read().split("\n")
        return random.choice(agents)


def scrapeMe(url):
    season_number = url.split("-")[-1]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=1*1000)
        page = browser.new_page(user_agent=userAgents())
        print(f"Initiating the automation | Powered by Playwright •")
        page.goto(url)

        page.wait_for_url(url)

        show_more_button = page.query_selector("//button[@type='button']")
        if show_more_button:
            show_more_button.click()

        content_xpath = "//li[@class='item full-ep css-q2f74n-Wrapper e19yuxbf0']"
        page.wait_for_selector(content_xpath, timeout=5*1000)

        print(f"Scraping Season {season_number} datas.")

        episodes = [epi.query_selector("//h2[@role='heading']").inner_text().strip(
        ).split("•")[-1].strip() for epi in page.query_selector_all(content_xpath)]
        episode_names = [name.query_selector("//h3[@class='text css-161tfdw-StyledSubHeader e3775fq0']").inner_text(
        ).strip() for name in page.query_selector_all(content_xpath)]
        episode_plots = [plot.query_selector("//div[@class='deck']/span").inner_text(
        ).strip() for plot in page.query_selector_all(content_xpath)]
        episode_air_date = [date.query_selector("//div[@class='meta']/span").inner_text(
        ).strip() for date in page.query_selector_all(content_xpath)]
        episode_links = [
            f"""https://www.southparkstudios.com{link.query_selector("//a").get_attribute('href')}""" for link in page.query_selector_all(content_xpath)]

        browser.close()

        data_in_dicts = {
            "Episode": episodes,
            "Episode Name": episode_names,
            "Episode Plot": episode_plots,
            "Episode Air Date": episode_air_date,
            "Episode Link": episode_links,

        }

        df = pd.DataFrame(data=data_in_dicts)
        df.to_excel(
            f"""South Park Season {season_number} database.xlsx""", index=False)
        print(f"Season {season_number} is saved.")
