import geonamescache

gc = geonamescache.GeonamesCache()

countries = gc.get_countries()
cities = gc.get_cities()

def imp_geolocations():
    selected_country_codes = ["US", "IN", "KR", "BR", "JP", "DE", "GB", "FR", "CA", "AU"]
    country_code_name_map = {code: data['name'] for code, data in countries.items()}
    country_cities = {country_code_name_map[code]: [] for code in selected_country_codes}

    for city in cities.values():
        code = city['countrycode']
        if code in selected_country_codes:
            country_name = country_code_name_map[code]
            country_cities[country_name].append(city)

    result = {}
    for country_code in selected_country_codes:
        country_name = country_code_name_map[country_code]
        sorted_cities = sorted(
            country_cities[country_name],
            key=lambda x: x.get('population', 0),
            reverse=True
        )
        top_city_names = [city['name'] for city in sorted_cities[:10]]
        result[country_name] = top_city_names

    return result

# Example usage
print(imp_geolocations())
