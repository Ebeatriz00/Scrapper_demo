# Scrapper_demo

Demostración de scrapper con Python + Playwright que busca productos en la web de Inkafarma y extrae el primer resultado (enlace al producto).

---

## 📌 Funcionalidades

- Ingresa a https://inkafarma.pe
- Busca un producto usando el buscador principal
- Detecta si hay resultados o mensaje de "no encontrado"
- Extrae el **enlace** del primer producto mostrado
- Guarda los resultados en tres formatos:
  - `resultados.csv`
  - `resultados.xlsx`
  - `resultados.json`

---

## 🧰 Requisitos

- Python 3.10+
- Playwright
- Pandas

Instala dependencias con:

```bash
pip install -r requirements.txt
playwright install
