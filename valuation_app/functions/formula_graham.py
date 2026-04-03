import math

def formula_graham(empresa_data):
    """
    Calcula o Valor Intrínseco pela Fórmula de Graham:
    VI = sqrt(22.5 * LPA * VPA)
    """
    try:
        lpa = empresa_data['lpa']
        cotacao = empresa_data['cotacao']
        pvp = empresa_data['pvp']

        if pvp == 0:
            return {"erro": "P/VP é zero, não é possível calcular o VPA."}

        vpa = cotacao / pvp

        if lpa <= 0:
            return {"erro": "LPA negativo ou zero. A fórmula de Graham não se aplica a empresas com prejuízo."}

        if vpa <= 0:
            return {"erro": "VPA negativo ou zero. A fórmula de Graham não se aplica neste caso."}

        vi = math.sqrt(22.5 * lpa * vpa)
        margem_seguranca = ((vi - cotacao) / vi) * 100

        if cotacao < vi:
            status = "ABAIXO do valor intrínseco (potencial de valorização)"
        else:
            status = "ACIMA do valor intrínseco (possível sobrevalorização)"

        return {
            "lpa": round(lpa, 2),
            "vpa": round(vpa, 2),
            "valor_intrinseco": round(vi, 2),
            "cotacao_atual": round(cotacao, 2),
            "margem_seguranca": round(margem_seguranca, 2),
            "status": status
        }

    except Exception as e:
        return {"erro": f"Erro ao calcular Fórmula de Graham: {str(e)}"}