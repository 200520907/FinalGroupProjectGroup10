def covidData_serializer(item) -> dict:
    return {
        "id":str(item["_id"]),
        "data":item["data"]
    }

def covidDatas_serializer(items) -> list:
    return [covidData_serializer(item) for item in items]
