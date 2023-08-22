'''Info Header Start
Name : tableUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
import td
import typing

def tableToDict( tableOperator:td.tableDAT ) -> typing.List[typing.Dict[str,str]]:
    rows = tableOperator.rows()
    header = [ cell.val for cell in rows.pop(0) ]
    return [
        { header[index] : cell.val for cell in row} for row in rows
    ]

def getHeader(tableOperator:td.tableDAT) -> typing.List[str]:
    return [ cell.val for cell in tableOperator.row(0) ]