import datetime

def stringToDatetime(string):
    """Transforma la fecha en formato dia/mes/año al objeto datetime"""
    return datetime.datetime.strptime(string, "%d/%m/%Y")
