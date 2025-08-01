import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import time

async def click_occ_pagination():
    print("🔍 CLICKING OCC PAGINATION BUTTONS")
    print("=" * 50)
    
    keyword = "recursos-humanos"
    BASE_URL = "https://www.occ.com.mx"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        url = f"{BASE_URL}/empleos/de-{keyword}/en-mexico"
        print(f"📄 Testing URL: {url}")
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)
            
            # Scroll to bottom
            print("📜 Scrolling to bottom...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            
            # Get initial job count
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            initial_articles = soup.select('div[id^="jobcard-"]')
            print(f"💼 Initial jobs: {len(initial_articles)}")
            
            # Try to find and click pagination buttons
            pagination_attempts = [
                # Try clicking any button with numbers
                'button:has-text("2")',
                'button:has-text("3")',
                'button:has-text("4")',
                'button:has-text("5")',
                'a:has-text("2")',
                'a:has-text("3")',
                'a:has-text("4")',
                'a:has-text("5")',
                # Try clicking "Siguiente" or "Next"
                'button:has-text("Siguiente")',
                'button:has-text("Next")',
                'a:has-text("Siguiente")',
                'a:has-text("Next")',
                # Try clicking any button at the bottom
                'button:last-child',
                'a:last-child'
            ]
            
            for i, selector in enumerate(pagination_attempts):
                try:
                    print(f"🔍 Trying selector {i+1}: {selector}")
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        print(f"✅ Found element: {selector}")
                        
                        # Get text before clicking
                        text = await element.text_content()
                        print(f"📝 Element text: '{text}'")
                        
                        # Click the element
                        await element.click()
                        await page.wait_for_timeout(3000)
                        
                        # Check if new jobs loaded
                        html = await page.content()
                        soup = BeautifulSoup(html, "html.parser")
                        new_articles = soup.select('div[id^="jobcard-"]')
                        print(f"💼 Jobs after click: {len(new_articles)}")
                        
                        if len(new_articles) > len(initial_articles):
                            print(f"🎉 SUCCESS! New jobs loaded: +{len(new_articles) - len(initial_articles)}")
                            
                            # Get new job IDs
                            new_job_ids = []
                            for article in new_articles:
                                if article.has_attr("id"):
                                    job_id = article["id"].replace("jobcard-", "")
                                    new_job_ids.append(job_id)
                            
                            print(f"🆔 New job IDs: {new_job_ids[:5]}...")
                            break
                        else:
                            print("📄 No new jobs loaded, trying next selector...")
                            
                except Exception as e:
                    print(f"❌ Error with selector {selector}: {str(e)}")
                    continue
            
            # If no pagination worked, try clicking any clickable element at the bottom
            print("🔍 Trying to click any element at the bottom...")
            try:
                # Get all clickable elements at the bottom
                bottom_elements = page.locator('button, a').all()
                print(f"🔘 Found {len(bottom_elements)} clickable elements")
                
                for i, element in enumerate(bottom_elements[-10:]):  # Try last 10 elements
                    try:
                        text = await element.text_content()
                        print(f"🔘 Element {i}: '{text}'")
                        
                        if text and any(char.isdigit() for char in text):
                            print(f"🎯 Clicking numbered element: '{text}'")
                            await element.click()
                            await page.wait_for_timeout(3000)
                            
                            # Check for new jobs
                            html = await page.content()
                            soup = BeautifulSoup(html, "html.parser")
                            new_articles = soup.select('div[id^="jobcard-"]')
                            print(f"💼 Jobs after click: {len(new_articles)}")
                            
                            if len(new_articles) > len(initial_articles):
                                print(f"🎉 SUCCESS! New jobs loaded!")
                                break
                    except:
                        continue
                        
            except Exception as e:
                print(f"❌ Error clicking bottom elements: {str(e)}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(click_occ_pagination()) 