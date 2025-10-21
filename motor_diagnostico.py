#!/usr/bin/env python
# -*- coding: utf-8 -*-

from experta import *

# --- 1. Definição dos Fatos ---
class Sintoma(Fact):
    pass
class Condicao(Fact):
    pass
class Diagnostico(Fact):
    pass
class Alerta(Fact):
    pass

# --- 2. Criação do Motor e da Base de Conhecimento (Regras) ---
class MotorDiagnosticoAgricola(KnowledgeEngine):
    
    @DefFacts()
    def _fatos_iniciais(self):
        yield Fact(acao="buscar_solucao")
        yield Fact(resultados=[]) # Lista para acumular nossos resultados

    def _adicionar_resultado(self, tipo, dados):
        """Helper para adicionar um resultado à nossa lista de fatos."""
        for f in self.facts.values(): 
            if 'resultados' in f: 
                lista_resultados_antiga = f['resultados']
                nova_lista = list(lista_resultados_antiga)
                nova_lista.append({'tipo': tipo, **dados})
                self.modify(f, resultados=nova_lista)
                break

    # --- GRUPO 1: GESTÃO HÍDRICA ---

    @Rule(Condicao(sensor_umidade_solo=P(lambda x: x < 30)), 
          Condicao(tipo_solo='arenoso'))
    def regra_irrigacao_solo_arenoso(self):
        self._adicionar_resultado('Diagnostico', {'recomendacao': 'irrigar_agora_ciclo_curto'})

    @Rule(Condicao(sensor_umidade_solo=P(lambda x: x < 40)), 
          Condicao(tipo_solo='argiloso'))
    def regra_irrigacao_solo_argiloso(self):
        self._adicionar_resultado('Diagnostico', {'recomendacao': 'irrigar_agora_ciclo_longo'})

    @Rule(Sintoma(planta_aparencia='murcha_pela_manha'), 
          Condicao(solo_umido='seco'))
    def regra_estresse_hidrico_severo(self):
        self._adicionar_resultado('Diagnostico', {'causa': 'estresse_hidrico_severo', 'recomendacao': 'irrigar_imediatamente'})

    @Rule(Sintoma(planta_aparencia='murcha_pela_tarde'), 
          Condicao(solo_umido='umido'), 
          Condicao(temperatura_ar=P(lambda x: x > 30)))
    def regra_estresse_termico(self):
        self._adicionar_resultado('Diagnostico', {'causa': 'estresse_termico', 'recomendacao': 'nao_irrigar_agora_verificar_sombreamento'})

    @Rule(Condicao(solo_umido='encharcado'), 
          Sintoma(planta_folhas_baixas='amareladas'))
    def regra_excesso_agua(self):
        self._adicionar_resultado('Diagnostico', {'causa': 'excesso_de_agua_asfixia_radicular', 'recomendacao': 'suspender_irrigacao_e_checar_drenagem'})

    @Rule(Condicao(previsao_tempo='chuva_intensa_proximas_24h'), 
          Condicao(solo_umido='umido'))
    def regra_evitar_irrigacao_chuva(self):
        self._adicionar_resultado('Diagnostico', {'recomendacao': 'cancelar_proximo_ciclo_de_irrigacao'})

    # --- GRUPO 2: DIAGNÓSTICO NUTRICIONAL ---
    
    @Rule(Sintoma(local='folhas_velhas', 
                  cor='amarelada_uniforme'))
    def regra_deficiencia_nitrogenio(self):
        self._adicionar_resultado('Diagnostico', {
            'causa': 'deficiencia_de_nitrogenio_(N)',
            'recomendacao': 'Aplicar fertilizante nitrogenado (ex: ureia, nitrato de amônio).' 
        })

    @Rule(Sintoma(local='folhas_velhas', 
                  cor='verde_escura_com_tons_arroxeados'))
    def regra_deficiencia_fosforo(self):
        self._adicionar_resultado('Diagnostico', {
            'causa': 'deficiencia_de_fosforo_(P)',
            'recomendacao': 'Aplicar fertilizante fosfatado (ex: superfosfato simples/triplo).'
        })

    @Rule(Sintoma(local='folhas_velhas', 
                  aspecto='bordas_queimadas_e_secas'))
    def regra_deficiencia_potassio(self):
        self._adicionar_resultado('Diagnostico', {
            'causa': 'deficiencia_de_potassio_(K)',
            'recomendacao': 'Aplicar fertilizante potássico (ex: cloreto de potássio).'
        })

    @Rule(Sintoma(local='folhas_velhas', 
                  cor='amarelada_entre_nervuras'))
    def regra_deficiencia_magnesio(self):
        # Esta regra declara um Fato, pois ela pode ser usada
        # pela regra de correção de pH (encadeamento)
        self.declare(Diagnostico(
            causa='deficiencia_de_magnesio_(Mg)',
            recomendacao='Aplicar sulfato de magnésio ou calcário dolomítico (se pH baixo).'
        ))

    @Rule(Sintoma(local='folhas_novas', 
                  cor='amarelada_entre_nervuras'))
    def regra_deficiencia_ferro(self):
        self._adicionar_resultado('Diagnostico', {
            'causa': 'deficiencia_de_ferro_(Fe)',
            'recomendacao': 'Aplicar quelato de ferro (Fe-EDTA) no solo ou via foliar.' 
        })

    @Rule(Sintoma(local='folhas_novas', 
                  aspecto='deformadas_ou_retorcidas', 
                  ponto_crescimento='morto'))
    def regra_deficiencia_calcio(self):
        self.declare(Diagnostico(
            causa='deficiencia_de_calcio_(Ca)',
            recomendacao='Aplicar gesso agrícola ou nitrato de cálcio.' 
        ))

    @Rule(Sintoma(local='folhas_novas', 
                  cor='amarelada_uniforme_completa'))
    def regra_deficiencia_enxofre(self):
        self._adicionar_resultado('Diagnostico', {
            'causa': 'deficiencia_de_enxofre_(S)',
            'recomendacao': 'Aplicar sulfato de amônio ou gesso agrícola (fontes de enxofre).' 
        })

    @Rule(OR(Diagnostico(causa='deficiencia_de_calcio_(Ca)'),
             Diagnostico(causa='deficiencia_de_magnesio_(Mg)')),
          Condicao(ph_solo=P(lambda x: x < 5.5)))
    def regra_corrigir_ph_para_Ca_Mg(self):
        self._adicionar_resultado('Diagnostico', {
            'recomendacao_corretiva': 'pH baixo detectado. Aplicar calcário dolomítico (corrige pH e fornece Ca/Mg).'
        })

    # --- GRUPO 3: DIAGNÓSTICO DE DOENÇAS E PRAGAS ---

    @Rule(Sintoma(observacao='po_branco_nas_folhas'))
    def regra_oidio(self):
        self.declare(Diagnostico(
            causa='infeccao_fungica_oidio',
            recomendacao='Aplicar fungicida à base de enxofre ou bicarbonato de potássio.'
        ))

    @Rule(Sintoma(observacao='manchas_amarelas_na_face_superior_folha', 
                  observacao_detalhe='po_marrom_ou_laranja_na_face_inferior'))
    def regra_ferrugem(self):
        self.declare(Diagnostico(
            causa='infeccao_fungica_ferrugem',
            recomendacao='Remover folhas infectadas e aplicar fungicida cúprico ou sistêmico.'
        ))

    @Rule(Sintoma(observacao='manchas_escuras_circulares_com_aneis_concentricos'))
    def regra_alternaria(self):
        self.declare(Diagnostico(
            causa='infeccao_fungica_alternaria_(pinta_preta)',
            recomendacao='Remover folhas afetadas e aplicar fungicida (ex: mancozeb ou cúprico).'
        ))

    @Rule(Sintoma(observacao='substancia_pegajosa_escura_nas_folhas', 
                  observacao_inseto='pequenos_insetos_verdes_ou_pretos_agrupados'))
    def regra_pulgoes(self):
        self.declare(Diagnostico(causa='infestacao_de_pulgoes_(afideos)')) 

    @Rule(AS.d << Diagnostico(causa='infestacao_de_pulgoes_(afideos)'), NOT(Fact(controle_pulgoes=True)))
    def regra_controle_pulgoes(self, d):
        self.modify(d, recomendacao_controle='aplicar_oleo_de_neem_ou_sabao_inseticida')
        self.declare(Fact(controle_pulgoes=True)) 

    @Rule(Sintoma(observacao='furos_irregulares_nas_folhas', 
                  detalhe='presenca_de_lagartas_ou_fezes_escuras'))
    def regra_lagartas(self):
        self.declare(Diagnostico(causa='ataque_de_lagartas')) 

    # --- INÍCIO DA CORREÇÃO ---
    # A condição "Condicao(tipo_cultura='hortalica')" foi REMOVIDA
    # para garantir que a solução SEMPRE seja disparada.
    @Rule(AS.d << Diagnostico(causa='ataque_de_lagartas'), 
          NOT(Fact(controle_lagartas=True)))
    def regra_controle_lagartas(self, d): # Renomeei a função
        self.modify(d, recomendacao_controle='aplicar_bacillus_thuringiensis_(BT)')
        self.declare(Fact(controle_lagartas=True))
    # --- FIM DA CORREÇÃO ---

    @Rule(Sintoma(observacao='folhas_com_pontilhados_prateados_ou_amarelados', 
                  detalhe='teias_finas_sob_as_folhas'), 
          Condicao(clima='seco_e_quente'))
    def regra_acaro_rajado(self):
        self.declare(Diagnostico(causa='infestacao_de_acaro_rajado')) 

    @Rule(AS.d << Diagnostico(causa='infestacao_de_acaro_rajado'), NOT(Fact(controle_acaro=True)))
    def regra_controle_acaro(self, d):
        self.modify(d, recomendacao_controle='aumentar_umidade_relativa_e_aplicar_acaricida')
        self.declare(Fact(controle_acaro=True))

    @Rule(Sintoma(planta_frutos='manchas_circulares_moles_e_escuras_apodrecidas'))
    def regra_antracnose(self):
        self.declare(Diagnostico(
            causa='antracnose',
            recomendacao='Remover frutos/partes afetadas e aplicar fungicida cúprico.' 
        ))

    # --- GRUPO 4: ALERTAS AMBIENTAIS E PREVENTIVOS ---

    @Rule(Condicao(temperatura_ar=P(lambda x: x > 35)), 
          Condicao(umidade_ar=P(lambda x: x < 40)), 
          Condicao(tipo_cultura='hortalica_folhosa'))
    def alerta_escaldadura(self):
        self._adicionar_resultado('Alerta', {'risco': 'Risco alto de escaldadura (queima solar)', 'recomendacao': 'Ativar sombrite ou nebulização'})

    @Rule(Condicao(previsao_tempo='geada_iminente'), 
          Condicao(temperatura_ar=P(lambda x: x < 3)), 
          Condicao(tipo_cultura='sensivel_ao_frio'))
    def alerta_geada(self):
        self._adicionar_resultado('Alerta', {'risco': 'Risco iminente de geada', 'recomendacao': 'Cobrir plantas com manta térmica ou irrigar por aspersão na madrugada'})

    @Rule(Condicao(velocidade_vento=P(lambda x: x > 60)), 
          Condicao(tipo_cultura='porte_alto_ex_milho_ou_banana'))
    def alerta_acamamento(self):
        self._adicionar_resultado('Alerta', {'risco': 'Risco de acamamento (tombamento) pelo vento', 'recomendacao': 'Reforçar estacas ou quebra-ventos'})

    @Rule(Condicao(umidade_ar=P(lambda x: x > 85)), 
          Condicao(periodo_chuvoso=True), 
          Condicao(historico_area='alta_incidencia_fungica'))
    def recomendacao_preventiva_fungo(self):
        self._adicionar_resultado('Diagnostico', {'recomendacao': '[PREVENTIVO] Aplicar fungicida a base de cobre devido à alta umidade'})

    @Rule(Condicao(estacao_ano='inicio_primavera'), 
          Condicao(temperatura_solo=P(lambda x: x > 18)))
    def recomendacao_monitoramento_pragas_solo(self):
        self._adicionar_resultado('Diagnostico', {'recomendacao': '[MONITORAMENTO] Iniciar monitoramento de pragas de solo (ex: larvas)'})

    @Rule(Condicao(cultura_estagio='floracao'), 
          Condicao(previsao_tempo='chuva_forte_ou_granizo'))
    def alerta_perda_floracao(self):
        self._adicionar_resultado('Alerta', {'risco': 'Risco de perda de flores e falha na polinização', 'recomendacao': 'Se possível, proteger estruturas (ex: estufas)'})


    # --- REGRA FINAL: COLETA DE RESULTADOS ---
    
    @Rule(AS.f_acao << Fact(acao='buscar_solucao'),
          Fact(resultados=MATCH.r), 
          salience=-100) 
    def coletar_resultados(self, f_acao, r):
        self.retract(f_acao) 
        
        print("\n--- RELATÓRIO DO SISTEMA ESPECIALISTA ---")
        
        diagnosticos_encontrados = [item for item in r if item['tipo'] == 'Diagnostico']
        alertas_encontrados = [item for item in r if item['tipo'] == 'Alerta']
        
        for f in self.facts.values():
            if isinstance(f, Diagnostico):
                if not any(d.get('causa') == f.get('causa') for d in diagnosticos_encontrados if d.get('causa')):
                    diagnosticos_encontrados.append(f)

        if not diagnosticos_encontrados and not alertas_encontrados:
            print("Nenhuma conclusão pôde ser determinada com os fatos fornecidos.")
            return

        if alertas_encontrados:
            print("\n[ALERTAS PREVENTIVOS]:")
            for i, alerta in enumerate(alertas_encontrados):
                print(f"  Alerta {i+1}: {alerta.get('risco')}")
                print(f"  Ação: {alerta.get('recomendacao')}")

        if diagnosticos_encontrados:
            print("\n[DIAGNÓSTICOS E RECOMENDAÇÕES]:")
            for i, d in enumerate(diagnosticos_encontrados):
                print(f"  Diagnóstico {i+1}:")
                if d.get('causa'):
                    print(f"    Causa Provável: {d.get('causa')}")
                if d.get('recomendacao'):
                    print(f"    Recomendação Imediata: {d.get('recomendacao')}")
                if d.get('recomendacao_controle'):
                    print(f"    Controle Específico: {d.get('recomendacao_controle')}")
                if d.get('recomendacao_corretiva'):
                    print(f"    Correção Específica: {d.get('recomendacao_corretiva')}")

        print("\n--- Fim do Relatório ---")