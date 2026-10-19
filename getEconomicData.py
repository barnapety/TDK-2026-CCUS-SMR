# READY
import yfinance as yf
import pandas as pd

def getEconomicData(companies):
    columns = ['name','stock','gics_sector','gics_industry','market_cap']
    df = pd.DataFrame(columns=columns)
    for company in companies:
        if company != "":
            df.loc[len(df)] = searchCompany(company)
    return df

def searchCompany(company):
    print('Searching Company:', company)
    ticker = yf.Ticker(company)
    info = ticker.info
    print(info)
    # get the necessary info
    if "longName" in info:
        company_name = ticker.info["longName"]
    elif "shortName" in info:
        company_name = ticker.info["shortName"]
    else:
        return None
    if 'sector' in info:
        sector = info.get('sector')
    else:
        return None
    if 'industry' in info:
        industry_group = info.get('industry')
    else:
        return None
    if 'marketCap' in info:
        market_cap = info.get('marketCap')
    else:
        return None

    di = {'name':company_name,'stock':company,'gics_sector':sector,'gics_industry':industry_group,'market_cap':market_cap}
    return di