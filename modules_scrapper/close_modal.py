
import asyncio
import random

async def cerrar_modal_emergente(page):
        try:
            await page.wait_for_selector('.evg-btn-dismissal', timeout=6000)
            await page.evaluate("""
                () => {
                    const btn = document.querySelector('.evg-btn-dismissal');
                    if (btn) btn.click();
                }
            """)
            #logger.info("❎ Modal emergente cerrado con JS")
            await asyncio.sleep(random.uniform(3.5, 6.5))
        except Exception as e:
            print(f" error al cerrarlo: {e}")
