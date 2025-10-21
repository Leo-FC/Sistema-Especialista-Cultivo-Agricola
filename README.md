# Sistema Especialista para Diagnóstico Agrícola

Uma aplicação web que implementa um Sistema Especialista para o diagnóstico de problemas em cultivos agrícolas. O sistema utiliza um motor de inferência baseado em regras (Python/Experta) e uma interface web (Flask/HTML/JS) para coletar sintomas e fornecer diagnósticos e soluções.

## Recursos

  * **Interface Web Amigável:** Uma aplicação de página única servida por Flask.
  * **Interface por Menus:** O usuário seleciona opções em menus (modais) em vez de digitar, evitando erros.
  * **Acúmulo de Fatos:** Permite ao usuário adicionar múltiplos fatos de diferentes categorias (folhas, pragas, solo, clima) antes de pedir um diagnóstico.
  * **Diagnósticos Múltiplos:** O motor de inferência pode retornar múltiplos diagnósticos e alertas baseados na combinação de fatos fornecida.
  * **Motor Baseado em Regras:** Utiliza a biblioteca `experta` para uma lógica de encadeamento de regras (inferência).
  * **API Backend:** O frontend (JavaScript) se comunica com um backend (Flask) que executa a lógica de diagnóstico.

## Tecnologias Utilizadas

  * **Backend:** Python 3
  * **Servidor Web:** Flask
  * **Motor de Inferência:** Experta
  * **Frontend:** HTML5, CSS3 e JavaScript (Vanilla)

## Como Rodar o Projeto

Siga estes 5 passos para configurar e executar o projeto localmente.

### 1\. Clonar o Repositório

Primeiro, clone este repositório para a sua máquina local e entre na pasta do projeto.

```bash
git clone https://github.com/Leo-FC/Sistema-Especialista-Cultivo-Agricola
cd Sistema-Especialista-Cultivo-Agricola
```

### 2\. Criar e Ativar o Ambiente Virtual (Obrigatório)

É altamente recomendado usar um ambiente virtual (`venv`) para isolar as dependências deste projeto.

```bash
# Crie o ambiente
python -m venv venv

# Ative o ambiente (Windows PowerShell)
.\venv\Scripts\Activate
```

*(Se estiver usando CMD, o comando é: `.\venv\Scripts\activate.bat`)*
*(Se estiver usando Linux/Mac, o comando é: `source venv/bin/activate`)*

### 3\. Instalação de Dependências (em 2 Etapas)

Este projeto possui uma peculiaridade de instalação devido a um conflito de dependências na biblioteca `experta`.

**Etapa A: Instalar as Dependências Principais**

Instale todas as dependências do `requirements.txt`. Este arquivo **não contém** o `experta` propositalmente, para que possamos instalar suas dependências corrigidas primeiro.

```bash
pip install -r requirements.txt
```

*(Isso irá instalar o `Flask` e, mais importante, uma versão moderna do `frozendict` que é compatível com Python 3.10+).*

**Etapa B: Instalar o 'Experta' (com --no-dependencies)**

Agora, forçamos a instalação do `experta` (na versão que usamos), dizendo a ele para ignorar suas próprias regras de dependência (que estão desatualizadas) e usar as bibliotecas que acabamos de instalar na Etapa A.

```bash
pip install experta==1.9.4 --no-dependencies
```

### 4\. Executar o Servidor

Com o ambiente virtual ainda ativo e todas as bibliotecas instaladas, inicie o servidor Flask:

```bash
python app.py
```

O terminal mostrará que o servidor está rodando, geralmente em:
`* Running on http://127.0.0.1:5000`

### 5\. Acessar a Aplicação

Abra seu navegador e acesse a URL:
[http://127.0.0.1:5000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000)

-----

## Estrutura do Projeto

```
/
|-- app.py                # O servidor web Flask (Backend API)
|-- motor_diagnostico.py  # O motor de inferência (Todas as regras @Rule)
|-- requirements.txt      # Dependências (usadas na Etapa 3-A)
|-- /templates/
|   |-- index.html        # A estrutura da página web (HTML)
|-- /static/
    |-- app.js            # O cérebro da interface (Frontend JS)
```
