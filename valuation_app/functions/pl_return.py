def pl_return(ativo_data):
    pl = ativo_data['pl']
    payout = ativo_data['payout'] / 100

    pl_inverso = 1 / pl * 100
    pl_inverso2 = pl_inverso * payout
    retorno_pl_inverso2 = (pl_inverso * pl) / pl_inverso2 if pl_inverso2 != 0 else 0

    explicacao = f"""
    Price to Earnings do PL inverso do ativo {ativo_data['ticker']} é {pl_inverso:.2f}%.
    E seu PL é {pl:.2f}, então levaria {pl:.2f} anos pagando 100% do seu lucro com DY de {pl_inverso:.2f}% ao ano para
    ter seu retorno total investido na ação.
    Porém, se ela não paga isso, se paga um payout de {payout * 100:.2f}% ela vai demorar {retorno_pl_inverso2:.2f} anos para devolver
    o capital com {pl_inverso2:.2f}% DY ao ano.
    """

    return {
        "pl_inverso": round(pl_inverso, 2),
        "pl": round(pl, 2),
        "dy_completo": round(pl_inverso2, 2),
        "payout": round(payout * 100, 2),
        "anos_para_retorno": round(retorno_pl_inverso2, 2),
        "explicacao": explicacao.strip()
    }
