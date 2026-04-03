# functions/valuation_damodaran.py

def valuation_damodaran(ativo, lpa, payout, anos, capital):
    try:
        roe_atual = ativo['roe']
        capital = capital / 100  # converter para decimal
        roe_esperado = roe_atual / (1 + capital)
        tx_cresc_esperado = (roe_esperado * (1 - payout / 100)) / 100

        tabela = [(0, lpa, lpa * (1 + tx_cresc_esperado), lpa * (payout / 100))]
        for ano in range(1, anos):
            lpa_futuro = tabela[-1][1] * (1 + tx_cresc_esperado)
            dy_futuro = lpa_futuro * (payout / 100)
            tabela.append((ano, lpa_futuro, lpa_futuro * (1 + tx_cresc_esperado), dy_futuro))

        resultado_formatado = "Ano     LPA Futuro   DY Futuro\n"
        for ano, lpa_futuro, _, dy_futuro in tabela:
            resultado_formatado += f"{ano:<7} R$ {lpa_futuro:.2f}     R$ {dy_futuro:.2f}\n"

        return resultado_formatado

    except Exception as e:
        return f"Erro ao calcular Valuation Damodaran: {str(e)}"