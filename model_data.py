from dataclasses import dataclass


@dataclass
class ModelData:
    """
    headers : ['label1', 'label2', ...]
    rows    : [[val1, val1, ..], [val1, val2, ..], ...]
    aligns  : list of (1=left, 2=center, 3=right)
    isgrnum : list of (0=notGrNum, 1=GrNum)
    typos   : 1=str, 2=integer, 3=decimal, 4=date
    """

    headers: list[str]
    rows: list
    aligns: list[int]
    isgrnum: list[int]
    typos: list[int]
