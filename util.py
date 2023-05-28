from playwright.async_api import async_playwright
import aiofiles

class Util():
	async def check_stream(self, stream_id: int) -> bool:
		async with async_playwright() as playwright:
			browser = await playwright.chromium.launch()  # Verwende Chromium (Chrome) als Browser
			page = await browser.new_page()

			await page.goto("https://gronkh.tv/streams/"+str(stream_id))

			await page.wait_for_timeout(500)

			page_content = await page.content()

			await browser.close()

			return not 'grnk-error' in page_content
	
	async def read_file(self, filename: str):
		async with aiofiles.open(filename, mode='r') as file:
			contents = await file.read()
			return contents

	async def write_file(self, filename: str, content: str) -> None:
		async with aiofiles.open(filename, mode='w') as file:
			await file.write(content)