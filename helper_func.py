import pandas as pd
import requests
import numpy as np
import re

API_TOKEN = "YOUR_NZDPU_API_TOKEN"  # NZDPU API Token

# Kommenteld ki ha a getGHGAndFinancialData.ipynb notebookkal használod a modult!!!
#with open('nzdpu_api_key.txt','r') as f:
#    API_TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

def nzdpu_do_get_request(request):
    resp = requests.get(request, headers=HEADERS)
    print('status', resp.raise_for_status())
    return resp.json()

def get_keys(json, keys):
    df = pd.json_normalize(json["values"])
    result = pd.DataFrame()
    for col in keys:
        if col in df.columns:
            result[col] = df[col]
        else:
            result[col] = 0
    return result

def generate_name_variants(full_name: str, capital=True):
    """
    Egy teljes név alapján listát generál a lehetséges cégnév-változatokról, kezelve a gyakori utótagokat és azok rövidítéseit.
    :param full_name: A cég neve (pl. "Apple Inc." vagy "Apple Incorporated")
    :return variantsUnique: A névváltozatok rendezett listája.
    """

    # A teljes elnevezések és rövidítések definiálása
    suffix_map = {
        "corporation": ["corp", "corp.", "corporation"],
        "incorporated": ["inc", "inc.", "incorporated"],
        "limited": ["ltd", "ltd.", "limited"],
        "company": ["co", "co.", "company"],
        "public limited company": ["plc", "p.l.c."],
        "limited liability company": ["llc", "l.l.c."],
        "joint stock company": ["jsc", "j.s.c.", "joint stock co", "joint stock company", "joint stock"],
        "joint stock co": ["jsc", "j.s.c.", "joint stock co", "joint stock company", "joint stock"]
    }

    # e.g., "inc" -> "incorporated", "inc." -> "incorporated"
    reverse_suffix_map = {}
    for canonical_key, variant_list in suffix_map.items():
        for variant in variant_list:
            cleaned_variant = re.sub(r"[,\.]", "", variant).lower()
            if cleaned_variant not in reverse_suffix_map:
                reverse_suffix_map[cleaned_variant] = canonical_key

    # Név feldolgozása

    name = full_name.strip()
    variants = [name]

    base = re.sub(r"[,\.]", "", name)
    base = re.sub(r"\s+", " ", base).strip()
    variants.append(base)

    words = base.split()
    if not words:
        return sorted(list(variants))

    found_suffix = False

    for i in range(1, len(words) + 1):

        potential_suffix = " ".join(words[-i:]).lower()

        if potential_suffix in reverse_suffix_map:
            base_name = " ".join(words[:-i])
            if not base_name:
                continue

            found_suffix = True

            variants.append(base_name)

            base_words = base_name.split()
            if base_words:
                standardized_base_name = " ".join([w.capitalize() for w in base_words])
                variants.append(standardized_base_name)

            canonical_key = reverse_suffix_map[potential_suffix]

            for suffix_variant in suffix_map[canonical_key]:
                variants.append(f"{base_name} {suffix_variant}")
                variants.append(f"{base_name} {suffix_variant.capitalize()}")
                if capital:
                    variants.append(f"{base_name} {suffix_variant.upper()}")

            break

    if not found_suffix:
        if len(words) > 1:
            base_name = " ".join(words[:-1])
            variants.append(base_name)

    variants.sort(key=str)
    variants.append(variants[0].replace(" ", "").lower())
    if "jointstock" in variants[-1].lower():
        variants.append(variants[-1].replace("jointstock", ""))
    variantsUnique = np.unique(np.array(sorted(variants)))

    return variantsUnique

if __name__ == "__main__":
    # Teszteléshez
    print(generate_name_variants("SJ Group Joint Stock Company",False))