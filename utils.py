from model_data import ModelData


def data2csv(data: ModelData, filename: str, separator: str, encoding: str):
    txt = separator.join(data.headers) + "\n"
    for line in data.rows:
        txt += separator.join([str(i) for i in line]) + "\n"
    with open(filename, "w", encoding=encoding) as fil:
        fil.write(txt)


def grnum(num):
    if num == 0:
        return ""
    return f"{num:,.2f}".replace(",", "|").replace(".", ",").replace("|", ".")
