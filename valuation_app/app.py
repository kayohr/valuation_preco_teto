from flask import Flask, render_template, request
import pandas as pd
import os
import requests
import requests_cache

headers = {
    "User-Agent": "Mozilla/5.0"
}
session = requests.Session()
session.headers.update(headers)

# Remove o arquivo de cache do fundamentus se existir
cache_file = os.path.join(os.path.dirname(__file__), 'http_cache.sqlite')
if os.path.exists(cache_file):
    os.remove(cache_file)

# Desativa o cache e substitui a sessão do fundamentus por uma sessão limpa
requests_cache.disabled()

import fundamentus
# Substitui a sessão interna do fundamentus por requests puro (sem cache)
fundamentus.fundamentus.session = session

from functions.estimativa_crescimento_dividendos import estimar_crescimento_dividendos
from functions.modelo_gordon import modelo_gordon
from functions.multiplo_justo import multiplo_justo
from functions.pl_return import pl_return
from functions.pl_bonds import pl_bonds
from functions.valuation_damodaran import valuation_damodaran
from functions.formula_graham import formula_graham

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dados = None
    erro = None
    resultado_crescimento = None
    resultado_gordon = None
    resultado_multiplo = None
    resultado_pl_inverso = None
    resultado_pl_bonds = None
    resultado_damodaran = None
    resultado_graham = None
    ticker_input = ""

    modelos = [
        {"nome": "Estimando o crescimento dos dividendos", "descricao": "Função do crescimento com base no histórico dos dividendos."},
        {"nome": "Modelo de Gordon / Análise Individual", "descricao": "Calcula o preço justo com base no DY e crescimento esperado."},
        {"nome": "Modelo de Gordon com Múltiplos Justos (P/L)", "descricao": "Compara o P/L atual com o P/L justo baseado em ROE e taxa exigida (rtx)."},
        {"nome": "PL Inverso", "descricao": "Inverte o P/L para estimar o retorno esperado do mercado."},
        {"nome": "Spread: retorno da ação - título público", "descricao": "Calcula a diferença entre o retorno da ação e a taxa livre de risco."},
        {"nome": "Lucro e dividendo - Valuation do Damodaran", "descricao": "Modelo com base nos conceitos do livro Valuation do Damodaran."},
        {"nome": "Fórmula de Graham", "descricao": "A fórmula de Graham é mais adequada para empresas tradicionais e indústrias. Ela pode não funcionar bem para empresas de crescimento rápido (\"growth\"), setores de serviços, bancos, ou empresas asset light (que possuem poucos ativos físicos)."}
    ]

    if request.method == 'POST':
        ticker_input = request.form.get('ticker', '').upper()

        try:
            df = fundamentus.get_resultado()

            if ticker_input in df.index:
                dados_ticker = df.loc[ticker_input]

                try:
                    lpa = round(dados_ticker['cotacao'] / dados_ticker['pl'], 2) if dados_ticker['pl'] != 0 else 0
                except:
                    lpa = 0

                try:
                    dividendo_acao = round(dados_ticker['dy'] * dados_ticker['cotacao'], 2)
                except:
                    dividendo_acao = 0

                try:
                    payout = round((dividendo_acao / lpa) * 100, 2) if lpa != 0 else 0
                except:
                    payout = 0

                dados = {
                    'ticker': ticker_input,
                    'cotacao': dados_ticker['cotacao'],
                    'pl': dados_ticker['pl'],
                    'pvp': dados_ticker['pvp'],
                    'psr': dados_ticker['psr'],
                    'dy': dados_ticker['dy'],
                    'pa': dados_ticker['pa'],
                    'pcg': dados_ticker['pcg'],
                    'pebit': dados_ticker['pebit'],
                    'pacl': dados_ticker['pacl'],
                    'evebit': dados_ticker['evebit'],
                    'evebitda': dados_ticker['evebitda'],
                    'mrgebit': dados_ticker['mrgebit'],
                    'mrgliq': dados_ticker['mrgliq'],
                    'roic': dados_ticker['roic'],
                    'roe': dados_ticker['roe'],
                    'liqc': dados_ticker['liqc'],
                    'liq2m': dados_ticker['liq2m'],
                    'patrliq': dados_ticker['patrliq'],
                    'divbpatr': dados_ticker['divbpatr'],
                    'lpa': lpa,
                    'dividendo_acao': dividendo_acao,
                    'payout': payout
                }

                modelo = request.form.get('modelo')

                if modelo == 'estimar_crescimento_dividendos':
                    try:
                        payout_user = float(request.form.get('payout'))
                        lucro1 = float(request.form.get('lucro1'))
                        lucro2 = float(request.form.get('lucro2'))
                        anos = int(request.form.get('anos'))

                        resultado_crescimento = estimar_crescimento_dividendos(
                            dados_ticker, lucro1, lucro2, anos, payout_user
                        )
                    except Exception as e:
                        erro = f"Erro no cálculo do crescimento: {str(e)}"

                elif modelo == 'modelo_gordon':
                    try:
                        roe = float(request.form.get('roe')) / 100
                        payout = float(request.form.get('payout')) / 100
                        rf = float(request.form.get('rf')) / 100
                        b = float(request.form.get('beta'))
                        rm = float(request.form.get('rm')) / 100
                        d1_tipo = int(request.form.get('d1_tipo'))

                        d1_valor_str = request.form.get('d1_valor')
                        d1_valor = float(d1_valor_str) if d1_tipo == 2 and d1_valor_str else 0

                        resultado_gordon = modelo_gordon(
                            dados_ticker, roe * 100, payout * 100, rf, b, rm, d1_tipo, d1_valor
                        )
                    except Exception as e:
                        erro = f"Erro no cálculo do Modelo de Gordon: {str(e)}"

                elif modelo == 'multiplo_justo':
                    try:
                        rtx = float(request.form.get('rtx'))
                        resultado_multiplo = multiplo_justo(dados, rtx)
                    except Exception as e:
                        erro = f"Erro no modelo de múltiplos justos: {str(e)}"

                elif modelo == 'pl_inverso':
                    try:
                        resultado_pl_inverso = pl_return(dados)
                    except Exception as e:
                        erro = f"Erro no modelo de PL Inverso: {str(e)}"

                elif modelo == 'pl_bonds':
                    try:
                        titulo_public = float(request.form.get('titulo_public'))
                        resultado_pl_bonds = pl_bonds(dados, titulo_public)
                    except Exception as e:
                        erro = f"Erro no modelo de Spread PL-Bonds: {str(e)}"

                elif modelo == 'valuation_damodaran':
                    try:
                        payout = float(request.form.get('payout'))
                        lpa = float(request.form.get('lpa'))
                        anos = int(request.form.get('anos'))
                        capital = float(request.form.get('capital'))

                        resultado_damodaran = valuation_damodaran(dados, lpa, payout, anos, capital)
                    except Exception as e:
                        erro = f"Erro no modelo de Valuation Damodaran: {str(e)}"


                elif modelo == 'formula_graham':
                    try:
                        resultado_graham = formula_graham(dados)
                    except Exception as e:
                        erro = f"Erro na Fórmula de Graham: {str(e)}"
            else:
                erro = f'Ticker "{ticker_input}" não encontrado.'

        except Exception as e:
            erro = f'Erro ao buscar dados: {str(e)}'

    return render_template(
        'index.html',
        dados=dados,
        erro=erro,
        modelos=modelos,
        resultado_crescimento=resultado_crescimento,
        resultado_gordon=resultado_gordon,
        resultado_multiplo=resultado_multiplo,
        resultado_pl_inverso=resultado_pl_inverso,
        resultado_pl_bonds=resultado_pl_bonds,
        resultado_damodaran=resultado_damodaran,
        resultado_graham=resultado_graham,
        ticker=ticker_input
    )

# ✅ NOVA ROTA: Décio Bazin
@app.route('/bazin', methods=['GET', 'POST'])
def bazin():
    erro = None
    resultado_bazin_custom = None

    dy_min = 6.00
    divbpatr_max = 1.50
    evebitda_max = 5.00
    pl_max = 10.00
    pl_min = 0.00

    if request.method == 'POST':
        try:
            dy_min = float(request.form.get('dy_min', dy_min))
            divbpatr_max = float(request.form.get('divbpatr_max', divbpatr_max))
            evebitda_max = float(request.form.get('evebitda_max', evebitda_max))
            pl_max = float(request.form.get('pl_max', pl_max))
            pl_min = float(request.form.get('pl_min', pl_min))

            df = fundamentus.get_resultado()

            df_filtrado = df[
                (df['dy'] * 100 >= dy_min) &
                (df['divbpatr'] <= divbpatr_max) &
                (df['evebitda'] <= evebitda_max) &
                (df['pl'] <= pl_max) &
                (df['pl'] >= pl_min) &
                (df['evebit'] >= 0) &
                (df['evebitda'] >= 0)
            ].copy()

            # Mover ticker do índice para coluna explícita
            df_filtrado.index.name = 'ticker'
            df_filtrado = df_filtrado.reset_index()

            # Converter colunas percentuais para exibição em %
            for col in ['dy', 'mrgebit', 'mrgliq', 'roic', 'roe']:
                if col in df_filtrado.columns:
                    df_filtrado[col] = (df_filtrado[col] * 100).round(2)

            # Arredondar todas as colunas numéricas para 2 casas
            for col in df_filtrado.select_dtypes(include='number').columns:
                df_filtrado[col] = df_filtrado[col].round(2)

            # Selecionar e reordenar colunas (ticker primeiro)
            colunas = ['ticker', 'cotacao', 'pl', 'pvp', 'psr', 'dy', 'p/cap.giro', 'pebit',
                       'evebit', 'evebitda', 'mrgebit', 'mrgliq',
                       'roic', 'roe', 'liq.corrente', 'liq2m', 'divbpatr']
            colunas_existentes = [c for c in colunas if c in df_filtrado.columns]
            df_filtrado = df_filtrado[colunas_existentes]

            resultado_bazin_custom = df_filtrado.sort_values(by='dy', ascending=False).head(10)
        except Exception as e:
            erro = f"Erro ao filtrar os dados: {str(e)}"

    return render_template(
        'index2.html',
        erro=erro,
        resultado_bazin_custom=resultado_bazin_custom,
        dy_min=dy_min,
        divbpatr_max=divbpatr_max,
        evebitda_max=evebitda_max,
        pl_max=pl_max,
        pl_min=pl_min
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
