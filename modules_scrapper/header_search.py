import asyncio
import random
from playwright.async_api import async_playwright

async def buscar_producto_desde_header(page, producto):
    try:
        await page.wait_for_selector('#ctrl-product-searcher', timeout=10000)
        await page.hover('#ctrl-product-searcher')
        await page.focus('#ctrl-product-searcher')
        await asyncio.sleep(random.uniform(1, 2))
        await page.type('#ctrl-product-searcher', producto, delay=random.randint(50, 150))
        await asyncio.sleep(random.uniform(1.5, 2.5))

        await page.hover('#lb--trigger-search-all-result')
        await page.evaluate('document.querySelector("#lb--trigger-search-all-result").scrollIntoViewIfNeeded();')
        await asyncio.sleep(random.uniform(1, 2))
        await page.mouse.down()
        await page.mouse.up()
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await page.click('#lb--trigger-search-all-result')

        print(f"🔍 Búsqueda enviada desde buscador principal: {producto}")

        await asyncio.sleep(random.uniform(3.5, 6.5))
        await page.wait_for_function("""
            () => {
                return document.querySelector("fp-product-large") ||
                       document.querySelector("fp-search-landing-empty");
            }
        """, timeout=60000)

    except Exception as e:
        print(f"❌ Error al buscar producto desde header: {e}")