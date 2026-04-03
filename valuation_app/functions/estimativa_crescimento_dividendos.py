def estimar_crescimento_dividendos(empresa_data, lucro_atual, lucro_passado, anos, payout_percentual):
    """
    Calcula:
    - Crescimento sustentável com base no ROE e Payout.
    - Crescimento histórico com base nos lucros passados.
    
    Parâmetros:
    empresa_data: dict ou Series com pelo menos a chave 'roe'
    lucro_atual: lucro mais recente (float ou int)
    lucro_passado: lucro de n anos atrás (float ou int)
    anos: intervalo em anos entre os lucros (int)
    payout_percentual: payout em % (ex: 92.28)
    """
    roe = empresa_data['roe'] * 100
    payout = payout_percentual / 100

    g_sustentavel = roe * (1 - payout)

    g_historico = ((lucro_atual / lucro_passado) ** (1 / (anos - 1)) - 1) * 100

    return {
        "crescimento_sustentavel": round(g_sustentavel, 2),
        "crescimento_historico": round(g_historico, 2)
    }

# Exemplo de uso:
# resultado = estimar_crescimento_dividendos(df.loc['B3SA3'], 4132512000, 2713507000, 5, 92.28)
# print(resultado)  # {'crescimento_sustentavel': ..., 'crescimento_historico': ...} 
