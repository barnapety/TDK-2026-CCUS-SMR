# Nagyvállalati dekarbonizációs stratégiák és GHG-kibocsátások adatelemzése (TDK)

Ez a repository *"A kis moduláris reaktorok és a szén-dioxid befogási, felhasználási és tárolási megoldások összehasonlítása a menetrendtartó erőművek szempontjából"* című TDK-dolgozatának (**Barna Péter Bálint**, BME TTK, Nukleáris Technika Intézet, 2026) 4. fejezetéhez készült adatgyűjtő és kiértékelő Python-kódokat tartalmazza.

## A projekt célja
Az itt található scriptek a világ 500 ($\pm$ 100) legnagyobb piaci kapitalizációjú vállalatának pénzügyi és üvegházhatásúgáz-kibocsátási (Scope 1, 2, 3) adatait gyűjtik össze, majd kulcsszavas keresési algoritmus segítségével számszerűsítik a vállalatok elköteleződését három alacsony karbonkibocsátású technológia (**CCUS**, **SMR**, **Megújulók**) iránt.

Az adatgyűjtés fő forrásai:
1. **Pénzügyi, Gazdasági és GICS adatok forrása**: Yahoo Finance
2. **Kibocsátási adatok forrása**: Net-Zero Data Public Utility (NZDPU) és Net Zero Tracker
3. **Fenntarthatósági PDF-ek linkjei**: DuckDuckGo Search API
4. **Technológiai elköteleződés pontozásához felhasznált forrás**: Google Custom Search Engine API

---

## Modulok és fájlok leírása

### Jupyter Notebookok (Fő munkafolyamat)
* **`getGHGAndFinancialData.ipynb`**: A pénzügyi (piaci kapitalizáció, GICS szektorok) és a GHG-kibocsátási adatok lekérdezését, összekapcsolását végző munkafüzet. A 
futtatást ezzel a munkafüzettel kell kezdeni, a megkeresendő cégek tőzsdei 'Ticker'-jét tartalmazó (a kódban 'tickersForAnalysis.txt' néven írt) szöveges fájllal,
melyben soronként vannak a tickerek elrendezve.
* **`scoreCompanies.ipynb`**: A vállalati elköteleződési pontszámok (CCUS, SMR, Renewable scores) kiszámítását végzi.

### Python modulok
* **`getEconomicData.py`**: A vállalatok pénzügyi mutatóinak és szektorális besorolásának automatizált lekérdezéséért felelős szkript.
* **`getGHGData.py`**: Az NZDPU-ból és a Net Zero Tracker-ből történő kibocsátásiadat-kinyerést megvalósító függvények.
* **`helper_func.py`**: Általános segédfüggvények lekérdezésekhez és osztályozáshoz.

---

## Futtatási követelmények
A kódok futtatásához Python 3.x+ környezet, valamint a `requirements.txt` fájlban szereplő csomagok telepítése szükséges:
```bash
pip install -r requirements.txt
```
Egyes kódrészletek futtatásához saját NZDPU, valamint Google Custom Search Engine API kulcsok szükségesek! Ezeket jeleztem a kódban 
**YOUR_NZDPU_API_TOKEN**, **YOUR_GOOGLE_API_KEY**, valamint **YOUR_CUSTOM_SEARCH_ENGINE_ID** placeholderekkel.