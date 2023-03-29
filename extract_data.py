import re
from collections import namedtuple

from model_data import ModelData

HEAD = (
    "z",
    "date",
    "desc",
    "fpa1",
    "fpa2",
    "fpa3",
    "fpa4",
    "val1",
    "val2",
    "val3",
    "val4",
    "val5",
    # "mark",
)


ZDATA = namedtuple("ZDATA", HEAD)


def read_html(filename):
    pattern = r"\[(.*?)\]"
    lines = []
    with open(filename, encoding="utf8") as file:
        for line in file.readlines():
            if line.startswith("{ id:"):
                matches = re.findall(pattern, line)
                lines.append(matches)
    return lines


def remove_quotes(val):
    return val.replace('"', "").strip()


def edit_lines(lines: list):
    final = []
    for line in lines:
        clin = []
        lin = line[0].split(",")
        clin = ZDATA(
            remove_quotes(lin[0]),
            remove_quotes(lin[1]),
            remove_quotes(lin[2]),
            float(remove_quotes(lin[3])),
            float(remove_quotes(lin[4])),
            float(remove_quotes(lin[5])),
            float(remove_quotes(lin[6])),
            float(remove_quotes(lin[7])),
            float(remove_quotes(lin[8])),
            float(remove_quotes(lin[9])),
            float(remove_quotes(lin[10])),
            float(remove_quotes(lin[11])),
        )
        if sum(clin[3:]) != 0 or clin[0] != "":
            final.append(clin)
            # print(clin)
    return final


def add_values(key: str, adic: dict, val: ZDATA):
    "val1 fpa1 val2 fpa2 val3 fpa3 val4 fpa4 val5 tval tfpa"

    adic[key] = adic.get(key, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    adic[key][0] = round(adic[key][0] + val.val1, 2)
    adic[key][1] = round(adic[key][1] + val.fpa1, 2)

    adic[key][2] = round(adic[key][2] + val.val2, 2)
    adic[key][3] = round(adic[key][3] + val.fpa2, 2)

    adic[key][4] = round(adic[key][4] + val.val3, 2)
    adic[key][5] = round(adic[key][5] + val.fpa3, 2)

    adic[key][6] = round(adic[key][6] + val.val4, 2)
    adic[key][7] = round(adic[key][7] + val.fpa4, 2)

    adic[key][8] = round(adic[key][8] + val.val5, 2)

    adic[key][9] = round(adic[key][9] + sum(val[7:]), 2)
    adic[key][10] = round(adic[key][10] + sum(val[3:7]), 2)


TRIMINO = {
    "01": "Α",
    "02": "Α",
    "03": "Α",
    "04": "Β",
    "05": "Β",
    "06": "Β",
    "07": "Γ",
    "08": "Γ",
    "09": "Γ",
    "10": "Δ",
    "11": "Δ",
    "12": "Δ",
}


def calc_totals(zlines: list[ZDATA]):
    etisia = {}
    trim = {}
    mina = {}
    for lin in zlines:
        etos, month, _ = lin.date.split("-")
        trv = f"{etos}-{TRIMINO[month]}"
        add_values(etos, etisia, lin)
        add_values(trv, trim, lin)
        add_values(f"{etos}-{month}", mina, lin)

    return etisia, trim, mina


def model_data(htmlfile):
    dnames = [
        "Αξία1",
        "ΦΠΑ1",
        "Αξία2",
        "ΦΠΑ2",
        "Αξία3",
        "ΦΠΑ3",
        "Αξία4",
        "ΦΠΑ4",
        "Αξία5",
        "Αξία",
        "ΦΠΑ",
    ]
    align = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    typo1 = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    zdata_lines = edit_lines(read_html(htmlfile))
    etisia, trim, mina = calc_totals(zdata_lines)
    etisialist = [[key, *val] for key, val in etisia.items()]
    trimlist = [[key, *val] for key, val in trim.items()]
    minalist = [[key, *val] for key, val in mina.items()]
    labels_etos = ["Έτος", *dnames]
    labels_trimino = ["Τρίμηνο", *dnames]
    labels_minas = ["Μήνας", *dnames]

    etisiadata = ModelData(labels_etos, etisialist, align, typo1)
    trimdata = ModelData(labels_trimino, trimlist, align, typo1)
    minaadata = ModelData(labels_minas, minalist, align, typo1)
    anl = [
        [
            i.date,
            i.z,
            i.val1,
            i.fpa1,
            i.val2,
            i.fpa2,
            i.val3,
            i.fpa3,
            i.val4,
            i.fpa4,
            i.val5,
            sum(i[7:]),
            sum(i[3:7]),
        ]
        for i in zdata_lines
    ]
    HEAD2 = ["Ημ/νία", "Ζ", *dnames]
    typo2 = [4, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    align2 = [1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    analytika = ModelData(HEAD2, anl, align2, typo2)
    return etisiadata, trimdata, minaadata, analytika
