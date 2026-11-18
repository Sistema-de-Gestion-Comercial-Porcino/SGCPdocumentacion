rows = {
0: {"COT": 5, "DETCOT": 7, "PRECIO": 10},
1: {"CLIENTE": 3, "INCID": 6, "PRODUCTO": 9},
2: {"CARGO": 2, "PEDIDO": 5, "DETPED": 7, "RESERVA": 8, "EXIST": 9, "CLASIF": 10},
3: {"APLIC": 3, "PAGO": 4, "ACUERDO": 6, "SEGUI": 7, "PREV": 8, "LOTE": 10},
4: {"COMPROB": 6, "FAEN": 7, "ANIMAL": 8, "CSAN": 9, "UBIC": 10},
5: {"EVID": 1, "ENTREGA": 2, "OP": 6, "FABR": 8, "CFRIO": 10},
6: {"OPPEND": 2, "USUARIO": 4, "PESAJE": 6, "CONS": 9, "MOV": 10},
7: {"TRANSP": 0, "RUTA": 1, "SESION": 3, "RES": 7},
8: {"PERMISO": 2, "ROL": 3, "AUDIT": 4, "RECUP": 5},
}
INIT = {k: (c, r) for r, d in rows.items() for k, c in d.items()}
COH = 40
T0 = 60.0
