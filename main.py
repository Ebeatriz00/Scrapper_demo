import asyncio
import random
import pandas as pd
import json
from playwright.async_api import async_playwright
from modules_scrapper.header_search import buscar_producto_desde_header
from modules_scrapper.close_modal import cerrar_modal_emergente


async def demo_scraper_inkafarma(producto):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        await page.goto("https://inkafarma.pe", timeout=120000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        try:
            await page.click('#truste-consent-button', timeout=5000)
        except:
            pass

        await buscar_producto_desde_header(page, producto)

        try:
            await cerrar_modal_emergente(page)
            await asyncio.sleep(random.uniform(3.5, 6.5))
            try:
                await page.wait_for_function(
                    """() => {
                        return document.querySelector("fp-search-empty-inka") || 
                                document.querySelector("fp-product-large");
                    }""",
                    timeout=250000
                )
                html = await page.content()
                await asyncio.sleep(random.uniform(3.5, 6.5))

                if "no encontramos productos que coincidan con" in html.lower():
                    print(f"⚠️ Producto NO encontrado: {producto}")
                    return None

            except Exception as e:
                print(f"❌ Error esperando contenido dinámico: {e}")
                return None

        except:
            print("❌ No se encontraron productos.")
            await browser.close()
            return None

        try:
            card = await page.query_selector('fp-product-large.d-none.d-sm-block.h-100')
            enlace = await card.query_selector('a')
            href = await enlace.get_attribute("href")
            url = f"https://inkafarma.pe{href}" if href.startswith("/") else href
            print(f"🔗 Link producto: {url}")
            await browser.close()

            return {
                "producto": producto,
                "url": url
            }

        except Exception as e:
            print(f"❌ Error leyendo datos: {e}")
            await browser.close()
            return None


# === 🧪 Guardar resultados ===
def guardar_resultados(data: list):
    df = pd.DataFrame(data)
    df.to_csv("resultados.csv", index=False)
    df.to_excel("resultados.xlsx", index=False)
    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ Resultados guardados como Excel, CSV y JSON.")


# === 🚀 Ejecución ===
if __name__ == "__main__":
    productos = ["panadol", "ibuprofeno", "paracetamol"]
    resultados = []

    for prod in productos:
        resultado = asyncio.run(demo_scraper_inkafarma(prod))
        if resultado:
            resultados.append(resultado)

    if resultados:
        guardar_resultados(resultados)
