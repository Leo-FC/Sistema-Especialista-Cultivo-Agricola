// Espera a página carregar
document.addEventListener('DOMContentLoaded', () => {

    // --- Variável de Estado ---
    let fatosAcumulados = [];

    // --- Seletores de Elementos ---
    const btnFolha = document.getElementById('btn-add-folha');
    const btnPraga = document.getElementById('btn-add-praga');
    const btnSolo = document.getElementById('btn-add-solo');
    const btnClima = document.getElementById('btn-add-clima');
    const btnDiagnosticar = document.getElementById('btn-diagnosticar');
    const btnLimpar = document.getElementById('btn-limpar');
    const listaFatosUI = document.getElementById('fatos-acumulados');
    const resultadosUI = document.getElementById('resultados');

    // --- Seletores do Modal ---
    const modalOverlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalOptions = document.getElementById('modal-options');

    // --- Funções de Ajuda ---

    function adicionarFato(tipo, dados, descricao) {
        fatosAcumulados.push({ tipo: tipo, dados: dados });
        const li = document.createElement('li');
        li.textContent = `[${tipo}] ${descricao}`;
        listaFatosUI.appendChild(li);
    }

    function limparSessao() {
        fatosAcumulados = [];
        listaFatosUI.innerHTML = '';
        resultadosUI.innerHTML = '';
    }

    /**
     * NOVA FUNÇÃO DE MODAL (Substitui o prompt)
     * Mostra um modal com opções e espera o clique do usuário.
     * @param {string} title - O título da pergunta.
     * @param {Object} options - Um objeto onde {chave: 'valor_exibido'}
     * @returns {Promise<string|null>} - A CHAVE da opção clicada (ex: '1') ou null.
     */
    function askQuestion(title, options) {
        // Retorna uma Promessa que será resolvida quando o usuário clicar
        return new Promise(resolve => {
            modalTitle.textContent = title;
            modalOptions.innerHTML = ''; // Limpa botões antigos

            // Cria um botão para cada opção
            for (const [key, value] of Object.entries(options)) {
                const btn = document.createElement('button');
                btn.textContent = value;
                btn.onclick = () => {
                    modalOverlay.classList.add('hidden'); // Esconde o modal
                    resolve(key); // Resolve a promessa com a CHAVE (ex: '1', 'v')
                };
                modalOptions.appendChild(btn);
            }
            
            modalOverlay.classList.remove('hidden'); // Mostra o modal
        });
    }

    // --- Funções de Menu (Agora são 'async' para usar 'await') ---

    // async/await permite que o código "espere" o usuário clicar no modal
    async function menuFolha() {
        const local = await askQuestion("Onde é o sintoma?", {
            '1': 'Folhas Velhas (na base)',
            '2': 'Folhas Novas (no topo)',
            'v': 'Voltar'
        });
        if (local === 'v') return;

        let dados = {};
        let descricao = "";

        if (local === '1') {
            dados.local = 'folhas_velhas';
            descricao = "Local: Folhas Velhas, ";
            const aspecto = await askQuestion("Qual a aparência?", {
                '1': 'Amarelada uniforme',
                '2': 'Bordas queimadas',
                '3': 'Amarelada entre nervuras',
                '4': 'Cor verde-escura/arroxeada',
                'v': 'Voltar'
            });
            if (aspecto === 'v') return;
            
            if (aspecto === '1') { dados.cor = 'amarelada_uniforme'; descricao += "Cor: Amarelada uniforme"; }
            else if (aspecto === '2') { dados.aspecto = 'bordas_queimadas_e_secas'; descricao += "Aspecto: Bordas queimadas"; }
            else if (aspecto === '3') { dados.cor = 'amarelada_entre_nervuras'; descricao += "Cor: Amarelada entre nervuras"; }
            else if (aspecto === '4') { dados.cor = 'verde_escura_com_tons_arroxeados'; descricao += "Cor: Verde-escura/arroxeada"; }

        } else if (local === '2') {
            dados.local = 'folhas_novas';
            descricao = "Local: Folhas Novas, ";
            const aspecto = await askQuestion("Qual a aparência?", {
                '1': 'Amarelada entre nervuras',
                '2': 'Amarelada uniforme completa',
                '3': 'Folhas deformadas e ponto morto',
                'v': 'Voltar'
            });
            if (aspecto === 'v') return;

            if (aspecto === '1') { dados.cor = 'amarelada_entre_nervuras'; descricao += "Cor: Amarelada entre nervuras"; }
            else if (aspecto === '2') { dados.cor = 'amarelada_uniforme_completa'; descricao += "Cor: Amarelada uniforme"; }
            else if (aspecto === '3') { 
                dados.aspecto = 'deformadas_ou_retorcidas'; 
                dados.ponto_crescimento = 'morto';
                descricao += "Aspecto: Deformadas/Ponto morto";
            }
        }
        
        if (Object.keys(dados).length > 0) { // Só adiciona se um fato foi criado
            adicionarFato('Sintoma', dados, descricao);
        }
    }

    async function menuSolo() {
        const opcao = await askQuestion("Qual a condição do Solo/Água?", {
            '1': 'Solo seco, planta murcha',
            '2': 'Solo encharcado',
            '3': 'Inserir pH (Manual)',
            'v': 'Voltar'
        });
        if (opcao === 'v') return;

        if (opcao === '1') {
            adicionarFato('Condicao', { solo_umido: 'seco' }, 'Solo: Seco');
            adicionarFato('Sintoma', { planta_aparencia: 'murcha_pela_manha' }, 'Planta: Murcha pela manhã');
        } else if (opcao === '2') {
            adicionarFato('Condicao', { solo_umido: 'encharcado' }, 'Solo: Encharcado');
            adicionarFato('Sintoma', { planta_folhas_baixas: 'amareladas' }, 'Planta: Folhas baixas amareladas');
        } else if (opcao === '3') {
            // Para inserção manual, o prompt ainda é a ferramenta mais rápida
            const ph = parseFloat(prompt("Digite o valor do pH (ex: 5.5):"));
            if (ph) {
                adicionarFato('Condicao', { ph_solo: ph }, `Solo: pH ${ph}`);
            }
        }
    }

    async function menuPraga() {
        const opcao = await askQuestion("O que você vê na planta?", {
            '1': 'Pó branco (talco) nas folhas',
            '2': 'Insetos pequenos e folhas grudentas',
            '3': 'Furos de lagartas',
            '4': 'Pontos prateados e teias finas',
            'v': 'Voltar'
        });
        if (opcao === 'v') return;

        let dadosSintoma = {};
        let descricao = "";

        if (opcao === '1') {
            dadosSintoma.observacao = 'po_branco_nas_folhas';
            descricao = "Sintoma: Pó branco nas folhas";
            adicionarFato('Sintoma', dadosSintoma, descricao);
        } else if (opcao === '2') {
            dadosSintoma.observacao = 'substancia_pegajosa_escura_nas_folhas';
            dadosSintoma.observacao_inseto = 'pequenos_insetos_verdes_ou_pretos_agrupados';
            descricao = "Sintoma: Insetos pequenos e folhas grudentas";
            adicionarFato('Sintoma', dadosSintoma, descricao);
        } else if (opcao === '3') {
            dadosSintoma.observacao = 'furos_irregulares_nas_folhas';
            dadosSintoma.detalhe = 'presenca_de_lagartas_ou_fezes_escuras';
            descricao = "Sintoma: Furos de lagartas";
            adicionarFato('Sintoma', dadosSintoma, descricao);
        } else if (opcao === '4') {
            dadosSintoma.observacao = 'folhas_com_pontilhados_prateados_ou_amarelados';
            dadosSintoma.detalhe = 'teias_finas_sob_as_folhas';
            descricao = "Sintoma: Pontos prateados e teias";
            adicionarFato('Sintoma', dadosSintoma, descricao);
            adicionarFato('Condicao', { clima: 'seco_e_quente' }, "Condição: Clima seco e quente");
        }
    }

    async function menuClima() {
        const opcao = await askQuestion("Qual a condição climática?", {
            '1': 'Risco de Geada (temp < 3°C)',
            '2': 'Onda de Calor (temp > 35°C e ar seco)',
            '3': 'Vento Forte (risco de tombar)',
            'v': 'Voltar'
        });
        if (opcao === 'v') return;

        let dadosCondicao = {};
        let descricao = "";

        if (opcao === '1') {
            dadosCondicao.previsao_tempo = 'geada_iminente';
            dadosCondicao.temperatura_ar = 2;
            dadosCondicao.tipo_cultura = 'sensivel_ao_frio';
            descricao = "Clima: Risco de Geada";
        } else if (opcao === '2') {
            dadosCondicao.temperatura_ar = 36;
            dadosCondicao.umidade_ar = 30;
            dadosCondicao.tipo_cultura = 'hortalica_folhosa';
            descricao = "Clima: Onda de Calor";
        } else if (opcao === '3') {
            dadosCondicao.velocidade_vento = 70;
            dadosCondicao.tipo_cultura = 'porte_alto_ex_milho_ou_banana';
            descricao = "Clima: Vento Forte";
        }

        if (descricao) {
            adicionarFato('Condicao', dadosCondicao, descricao);
        }
    }
    
    // --- Função Principal: Chamar a API ---
    
    async function executarDiagnostico() {
        if (fatosAcumulados.length === 0) {
            alert("Por favor, adicione pelo menos um fato antes de diagnosticar.");
            return;
        }
        resultadosUI.innerHTML = "Processando...";

        try {
            const resposta = await fetch('/diagnosticar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(fatosAcumulados)
            });

            if (!resposta.ok) {
                const erro = await resposta.json();
                throw new Error(`Erro na API: ${erro.erro || resposta.statusText}`);
            }

            const resultados = await resposta.json();
            
            resultadosUI.innerHTML = '';
            if (resultados.length === 0) {
                resultadosUI.innerHTML = "<div>Nenhuma conclusão pôde ser determinada.</div>";
                return;
            }

            resultados.forEach(res => {
                const div = document.createElement('div');
                if (res.tipo === 'Alerta') {
                    div.className = 'alerta';
                    div.innerHTML = `<strong>ALERTA:</strong> ${res.risco}<br><strong>Ação:</strong> ${res.recomendacao}`;
                } else if (res.tipo === 'Diagnostico') {
                    div.className = 'diagnostico';
                    let html = '<strong>DIAGNÓSTICO:</strong><br>';
                    if(res.causa) html += `<strong>Causa:</strong> ${res.causa}<br>`;
                    if(res.recomendacao) html += `<strong>Recomendação:</strong> ${res.recomendacao}<br>`;
                    if(res.recomendacao_controle) html += `<strong>Controle:</strong> ${res.recomendacao_controle}<br>`;
                    if(res.recomendacao_corretiva) html += `<strong>Correção:</strong> ${res.recomendacao_corretiva}<br>`;
                    div.innerHTML = html;
                }
                resultadosUI.appendChild(div);
            });

        } catch (erro) {
            resultadosUI.innerHTML = `<div class="alerta">Erro ao processar: ${erro.message}</div>`;
        }
    }

    // --- Conectar Botões às Funções ---
    btnFolha.addEventListener('click', menuFolha);
    btnSolo.addEventListener('click', menuSolo);
    btnPraga.addEventListener('click', menuPraga);
    btnClima.addEventListener('click', menuClima);

    btnDiagnosticar.addEventListener('click', executarDiagnostico);
    btnLimpar.addEventListener('click', limparSessao);
});