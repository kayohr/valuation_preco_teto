def pl_bonds(ativo, titulo_public):
    try:
        pl_inverso = (1 / ativo['pl']) * 100
        bonds = pl_inverso - titulo_public

        explicacao = f"""
DY estimado pelo P/L Inverso: {pl_inverso:.2f}%
Taxa do título público usada: {titulo_public:.2f}%
Spread da ação: {bonds:.2f}%
        """

        status = (
            f"PL_Bonds: Taxa de retorno superior com spread de {bonds:.2f}%"
            if bonds > 0 else
            f"PL_Bonds: Taxa de retorno inferior com spread de {bonds:.2f}%"
        )

        return explicacao + "\n" + status

    except Exception as e:
        return f"Erro ao calcular PL_Bonds: {str(e)}"
