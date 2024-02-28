import datetime

def stringToDatetime(string):
    """Transforma la fecha en formato dia/mes/año al objeto datetime"""
    return datetime.datetime.strptime(string, "%d/%m/%Y")

def subtract30Days(date):
    """Resta a la fecha pasada un intervalo de 30 días"""
    return date - datetime.timedelta(days=30)