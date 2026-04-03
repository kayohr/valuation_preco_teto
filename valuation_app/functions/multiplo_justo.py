def multiplo_justo(empresa_data, rtx):
    roe = empresa_data['roe']  # já vem como fração
    payout = empresa_data['payout'] / 100  # vem como porcentagem, converte para fração
    r = rtx / 100  # retorno exigido

    g = ((1 - payout) * roe) / 100

    try:
        pl_justo = payout * (1 + g) / (r - g)
    except ZeroDivisionError:
        pl_justo = 0

    status = "ABAIXO do justo (barato)" if empresa_data['pl'] < pl_justo else "ACIMA do justo (caro)"

    return {
        "roe": round(roe * 100, 2),
        "payout": round(payout * 100, 2),
        "g": round(g * 100, 2),
        "rtx": round(rtx, 2),
        "pl_justo": round(pl_justo, 2),
        "pl_atual": round(empresa_data['pl'], 2),
        "status": status
    }
