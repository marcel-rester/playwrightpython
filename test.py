import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigation und HTTP-Status prüfen (page.goto gibt ein Response-Objekt zurück)
    response = page.goto("https://ferienhaus-rester.at/api")
    if response is None:
        raise RuntimeError("Keine Antwort beim Laden der Seite.")
    if response.status != 200:
        raise RuntimeError(f"Unerwarteter HTTP-Status: {response.status}")

    # Titel prüfen
    # Entweder exakte Prüfung:
    expect(page).to_have_title("api")
    # Oder regex-basierte Prüfung (falls nötig):
    # expect(page).to_have_title(re.compile(r"api", re.IGNORECASE))

    # Warte und Screenshot der ganzen Seite
    page.wait_for_timeout(10_000)
    page.screenshot(path="screenshotx.png")

    # Kleiner zusätzlicher Warte-Puffer
    page.wait_for_timeout(1_000)

    # Screenshot vom Canvas-Element (falls vorhanden)
    canvas = page.query_selector("#myCanvas")
    if canvas:
        canvas.screenshot(path="canvas_screenshot.png")
    else:
        print("Hinweis: Kein Element mit id='#myCanvas' gefunden. Überspringe Canvas-Screenshot.")

    # Prüfen, ob ein "Uploaded"-Text sichtbar ist
    uploaded_text = page.get_by_text("Uploaded")
    expect(uploaded_text).to_be_visible()

    # Klick auf Button
    page.click("#btn")

    # Aufräumen
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)