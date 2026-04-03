def modelo_gordon(empresa_data, roe_input, payout_input, rf, b, rm, d1_escolha, dividendo_manual):
    """
    Calcula o preço justo de uma ação segundo o modelo de Gordon.
    Apresenta os comentários explicativos e valida se a fórmula é aplicável (ke > g).

    Parâmetros:
    - empresa_data: dict ou Series com ao menos 'cotacao' e 'dy'
    - roe_input: ROE (%) informado
    - payout_input: payout (%) informado
    - rf: taxa livre de risco (decimal, ex: 0.06)
    - b: beta da empresa
    - rm: retorno do mercado (decimal, ex: 0.09)
    - d1_escolha: 1 para cálculo automático, 2 para manual
    - dividendo_manual: valor do dividendo informado
    """

    # Função para achar a taxa de crescimento "g" / Pegar Roe histórico, pegar no site
    roe = roe_input / 100
    payout = payout_input / 100
    g = roe * (1 - payout)

    # Juros do IPC a longo prazo + inflação atual(IPCA anual)
    # Beta da empresa para analisar
    # Prêmio de Risco (Peguei da tabela do Damodaran de risco no Brasil)

    # Função para achar o ke (Custo de Capital Próprio)
    ke = rf + b * (rm - rf)

    # Função para achar o valor justo
    if d1_escolha == 1:
        d1 = empresa_data['dy'] * empresa_data['cotacao'] * (1 + g)
    else:
        d1 = dividendo_manual

    if ke <= g:
        return {
            "erro": "A fórmula de Gordon não é válida quando o crescimento (g) é maior ou igual ao custo de capital (ke).",
            "ke": round(ke * 100, 2),
            "taxa_crescimento_sustentavel": round(g * 100, 2),
            "cotacao_atual": round(empresa_data['cotacao'], 2),
            "d1": round(d1, 2),
            "preco_justo": None,
            "recomendacao": "INVÁLIDA"
        }

    try:
        p = d1 / (ke - g)
    except ZeroDivisionError:
        p = 0

    abaixo = empresa_data['cotacao'] < p

    return {
        "taxa_crescimento_sustentavel": round(g * 100, 2),
        "ke": round(ke * 100, 2),
        "d1": round(d1, 2),
        "preco_justo": round(p, 2),
        "cotacao_atual": round(empresa_data['cotacao'], 2),
        "recomendacao": "ABAIXO do preço justo" if abaixo else "ACIMA do preço justo"
    }
