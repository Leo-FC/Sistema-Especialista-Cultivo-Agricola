#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
from motor_diagnostico import MotorDiagnosticoAgricola, Sintoma, Condicao, Diagnostico, Fact

# Inicializa o aplicativo Flask
app = Flask(__name__)

# --- Helper de Formatação ---
def formatar_texto(texto):
    """
    Formata o texto interno do motor para algo legível.
    Ex: 'deficiencia_de_magnesio_(Mg)' vira 'Deficiencia de magnesio (mg)'
    """
    if not texto:
        return None # Retorna None se o texto for vazio
    
    # Primeiro, substitui underscores
    texto_formatado = texto.replace('_', ' ')
    
    # Coloca em maiúscula apenas a primeira letra da string inteira
    return texto_formatado.capitalize()

# --- Rota 1: Servir a Página Web ---
@app.route('/')
def index():
    """Renderiza o nosso frontend (o index.html)"""
    return render_template('index.html')

# --- Rota 2: A API de Diagnóstico (VERSÃO 100% FORMATADA) ---
@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    """
    Recebe os fatos do frontend, executa o motor 
    e retorna os resultados como JSON.
    """
    fatos_json = request.json
    engine = MotorDiagnosticoAgricola()
    engine.reset()
    
    try:
        # 1. Declarar os fatos no motor
        for fato_info in fatos_json:
            tipo_fato = fato_info.get('tipo')
            dados_fato = fato_info.get('dados', {})
            
            if tipo_fato == 'Sintoma':
                engine.declare(Sintoma(**dados_fato))
            elif tipo_fato == 'Condicao':
                engine.declare(Condicao(**dados_fato))
        
        # 2. Executar o motor
        engine.run()
        
        # 3. Coletar os resultados (de AMBAS as fontes)
        causas_ja_adicionadas = set() 
        resultados_finais = []

        for f in engine.facts.values():
            
            # Fonte 1: Pega a lista principal de resultados (de _adicionar_resultado)
            if 'resultados' in f:
                for res in f['resultados']:
                    
                    # --- APLICA FORMATAÇÃO COMPLETA AQUI ---
                    res_formatado = {
                        'tipo': res.get('tipo'),
                        'causa': formatar_texto(res.get('causa')),
                        'risco': formatar_texto(res.get('risco')),
                        'recomendacao': formatar_texto(res.get('recomendacao')),
                        'recomendacao_controle': formatar_texto(res.get('recomendacao_controle')),
                        'recomendacao_corretiva': formatar_texto(res.get('recomendacao_corretiva'))
                    }
                    # Remove chaves que são None (limpa o JSON)
                    res_formatado = {k: v for k, v in res_formatado.items() if v is not None}
                    
                    resultados_finais.append(res_formatado)
                    
                    if res_formatado.get('causa'):
                        causas_ja_adicionadas.add(res_formatado.get('causa')) 
            
            # Fonte 2: Pega os diagnósticos de encadeamento (de self.declare)
            if isinstance(f, Diagnostico):
                causa_original = f.get('causa')
                causa_formatada = formatar_texto(causa_original)
                
                # Adiciona só se essa causa ainda não foi adicionada pela Fonte 1
                if causa_formatada and causa_formatada not in causas_ja_adicionadas:
                    
                    # --- APLICA FORMATAÇÃO COMPLETA AQUI TAMBÉM ---
                    diag_dict = {
                        'tipo': 'Diagnostico',
                        'causa': causa_formatada,
                        'recomendacao': formatar_texto(f.get('recomendacao')),
                        'recomendacao_controle': formatar_texto(f.get('recomendacao_controle')),
                        'recomendacao_corretiva': formatar_texto(f.get('recomendacao_corretiva'))
                    }
                    # Remove chaves que são None (limpa o JSON)
                    diag_dict = {k: v for k, v in diag_dict.items() if v is not None}

                    resultados_finais.append(diag_dict)
                    causas_ja_adicionadas.add(causa_formatada) # Marca como adicionada
                
        # 5. Retornar a lista final e formatada
        return jsonify(resultados_finais)

    except Exception as e:
        # Captura erros e os envia como JSON para o frontend
        return jsonify({"erro": str(e)}), 400

# --- Comando para rodar o servidor ---
if __name__ == '__main__':
#     Roda o app em modo de debug
    app.run(debug=True, port=5000)

