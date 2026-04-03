def metodo_bazin(dataframe, filtros_customizados=None):
    filtros = {
        'divbpatr': 1.5,
        'dy': 0.06,
        'evebitda': 5,
        'pl_min': 0,
        'pl_max': 10
    }

    if filtros_customizados:
        filtros.update(filtros_customizados)

    filtrado = dataframe[
        (dataframe['divbpatr'] < filtros['divbpatr']) &
        (dataframe['dy'] > filtros['dy']) &
        (dataframe['evebitda'] < filtros['evebitda']) &
        (dataframe['pl'] > filtros['pl_min']) &
        (dataframe['pl'] < filtros['pl_max'])
    ]

    ordenado = filtrado.sort_values(by='dy', ascending=False).head(10)
    return ordenado
