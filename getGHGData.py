from duckduckgo_search import DDGS # pip install duckduckgo_search szükséges a DuckDuckGo "korlátlanul hozzáférhető API-jának eléréséhez.
from bs4 import BeautifulSoup # A BeautifulSoup-ot a HTML weboldalak olvasásához használtam

from helper_func import *

def nzdpu(company_name):
    names = generate_name_variants(company_name)
    # Get nzId and lry:
    for name in names:
        print("Trying NZDPU for",name)
        nzid_url = f"https://nzdpu.com/wis/coverage/companies?name={name}&start=0&limit=10&order_by=company_name&order=ASC"
        resp = nzdpu_do_get_request(nzid_url)
        if resp['total'] == 0:
            continue

        # Company found in NZDPU database, do searching:
        first = resp['items'][0]
        last_report_yr = first['latest_reported_year']
        nz_id = first['nz_id']
        url = f'https://nzdpu.com/wis/coverage/companies/{nz_id}/disclosure-details?year={last_report_yr}'
        resp = nzdpu_do_get_request(url)
        keys = ['total_s1_emissions_ghg', 's1_co2_emissions', 'total_s2_lb_emissions_ghg', 'total_s2_mb_emissions_ghg', 'total_s3_emissions_ghg']  # needed keys
        res = get_keys(resp, keys)
        return last_report_yr, res
    return None

def searchNet0Tracker(company_name):
    names = generate_name_variants(company_name)
    yr = 0
    flag = False
    emissions = {}
    for name in names:
        print("Trying Net0Tracker for",name)
        url = f"https://net0tracker.com/corporates.html/{name}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if "No match found" in soup.text:
            continue
        else:
            bs = soup.find_all("div", attrs={"class": "table-wrapper"})
            if len(bs) == 0:
                continue
            useful = bs[0]
            yr = useful.find("thead").find_all("th")[1]
            yr = int(str(yr.get_text(strip=True))[1:])
            data_rows = soup.find("tbody").find_all("tr")
            for row in data_rows:
                label = row.find("td").get_text(strip=True)
                cells = row.find_all("td")[1:]
                if "Scope 1" in label and "-" not in label:
                    text = cells[0].get_text(strip=True).replace(',', '')
                    emissions["Scope 1"] = float(text) if text.replace(',', '',1).isdigit() else None
                elif "Scope 2 - market-based" in label:
                    text = cells[0].get_text(strip=True).replace(',', '')
                    emissions["Scope 2 - mb"] = float(text) if text.replace(',', '',1).isdigit() else None
                elif "Scope 2 - location-based" in label:
                    text = cells[0].get_text(strip=True).replace(',','')
                    emissions["Scope 2 - lb"] = float(text) if text.replace(',', '',1).isdigit() else None
                elif "Scope 3" in label and "-" not in label:
                    text = cells[0].get_text(strip=True).replace(',', '')
                    emissions["Scope 3"] = float(text) if text.replace(',', '',1).isdigit() else None
            flag = True
    return (yr, emissions) if flag else None

def searchPDFs(company_name, n = 3):
    query = f"{company_name} sustainability report filetype:pdf"
    with DDGS() as ddgs:
        return [r["href"] for r in ddgs.text(query, max_results=n)]

def getGHGData(companies):
    company_ghg_data = []
    for company in companies:
        print("Processing",company)
        if company is not None:
            ghg = {'name': company,
                   'year':0,
                   'total_s1_emissions_ghg':0,
                   's1_co2_emissions':0,
                   'total_s2_lb_emissions_ghg':0,
                   'total_s2_mb_emissions_ghg':0,
                   'total_s3_emissions_ghg':0,
                   'light_data':'NZDPU',
                   'links':[]}

            nzdpu_ = nzdpu(company)
            if nzdpu_ is None:
                ghg['light_data'] = 'nzTracker'
                nzTracker = searchNet0Tracker(company)
                if searchNet0Tracker(company) is None:
                    ghg['light_data'] = 'WebPDF'
                else:
                    # Fill in NZTracker
                    ghg['year'] = nzTracker[0]
                    ghg['total_s1_emissions_ghg'] = nzTracker[1]['Scope 1']
                    ghg['total_s2_mb_emissions_ghg'] = nzTracker[1]['Scope 2 - mb']
                    ghg['total_s3_emissions_ghg'] = nzTracker[1]['Scope 3']
                    ghg['total_s2_lb_emissions_ghg'] = nzTracker[1]['Scope 2 - lb']
            else:
                # Fill in NZDPU
                ghg['year'] = nzdpu_[0]
                ghg['total_s1_emissions_ghg'] = nzdpu_[1]['total_s1_emissions_ghg'].iloc[0]
                ghg['s1_co2_emissions'] = nzdpu_[1]['s1_co2_emissions'].iloc[0]
                ghg['total_s2_lb_emissions_ghg'] = nzdpu_[1]['total_s2_lb_emissions_ghg'].iloc[0]
                ghg['total_s2_mb_emissions_ghg'] = nzdpu_[1]['total_s2_mb_emissions_ghg'].iloc[0]
                ghg['total_s3_emissions_ghg'] = nzdpu_[1]['total_s3_emissions_ghg'].iloc[0]

            ghg['links'] = searchPDFs(company)

            if len(ghg['links']) == 0 and ghg['light_data'] == 'WebPDF':
                ghg['light_data'] = 'None'

            company_ghg_data.append(ghg)
        else:
            gh_ = {'name': None,
                   'year': 0,
                   'total_s1_emissions_ghg': 0,
                   's1_co2_emissions': 0,
                   'total_s2_lb_emissions_ghg': 0,
                   'total_s2_mb_emissions_ghg': 0,
                   'total_s3_emissions_ghg': 0,
                   'light_data': 0,
                   'links': []}
            company_ghg_data.append(gh_)
    return company_ghg_data

    # Keresési sorrend:
    # 1. NZDPU API
    # IF NOT FOUND:
    #   2. net0tracker scraping
    # IF NOT FOUND:
    #       3. Report PDF scraping
    # IF NOT FOUND:
    #           4. NOT FOUND