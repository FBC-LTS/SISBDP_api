import datetime

def re_converter_data(data, formato_antigo, formato_novo="%Y-%m-%d"):
    obj = datetime.datetime.strptime(data, formato_antigo)
    data_mysql = obj.strftime(formato_novo)
    return data_mysql

