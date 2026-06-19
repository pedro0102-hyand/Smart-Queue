# 📋 SmartQueue

Um **sistema inteligente de gerenciamento de fila de atendimento** que prioriza chamados por severidade, mantendo ordem FIFO entre solicitações de mesma prioridade.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0+-red.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Pytest-8.0.0+-green.svg)](https://pytest.org/)

---

## 🎯 Sobre o Projeto

SmartQueue resolve o problema de **organizar e priorizar solicitações de atendimento** em centrais de suporte, help desk, clínicas ou qualquer ambiente que necessite gerenciar múltiplos chamados com diferentes níveis de urgência.

### Problema Abordado

Em um sistema FIFO tradicional:
- Cliente A (problema crítico) chega às 10:05
- Cliente B (dúvida simples) chega às 10:00
- Cliente B é atendido primeiro ❌

**Com SmartQueue:**
- Cliente A é atendido primeiro (maior severidade) ✅
- Mantém ordem de chegada como desempate ✅

---

## ✨ Características Principais

- ✅ **Fila de Prioridade Eficiente** - Min-heap binária com O(log n)
- ✅ **Priorização por Severidade** - Níveis 1-5, customizáveis
- ✅ **FIFO como Desempate** - Ordem de chegada preservada
- ✅ **Persistência em CSV** - Dados salvos entre sessões
- ✅ **Logging Estruturado** - Auditoria completa de operações
- ✅ **Relatórios e Estatísticas** - Visualização de dados
- ✅ **Duas Interfaces** - CLI interativa e Dashboard Web
- ✅ **Testes Abrangentes** - 100% de cobertura de casos críticos

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes)

### Passos

1. **Clone ou baixe o repositório**
```bash
cd smartqueue
```

2. **Crie um ambiente virtual** (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Verifique a instalação**
```bash
pytest tests/
```

---

## 📖 Como Usar

### Opção 1: Interface CLI (Terminal)

Ideal para automação e integração com scripts.

```bash
python main.py
```

**Menu disponível:**
```
1 - Criar chamado
2 - Atender próximo
3 - Listar fila
4 - Ver próximo
5 - Quantidade de chamados
6 - Top chamados críticos
7 - Buscar chamado por ID
8 - Cancelar chamado
9 - Estatísticas
0 - Sair
```

#### Exemplo de uso:
```bash
$ python main.py
📂 2 chamado(s) carregado(s).

===================================
         SMARTQUEUE
===================================
1 - Criar chamado
...
Escolha: 1

=== NOVO CHAMADO ===
Cliente: João Silva
Categoria: Suporte Técnico
Severidade (1-5): 5
Descrição: Sistema fora do ar

✅ Chamado criado com sucesso!
```

---

### Opção 2: Interface Web (Streamlit)

Ideal para visualização e uso por não-técnicos.

```bash
streamlit run app.py
```

Abre automaticamente em `http://localhost:8501`

**Funcionalidades do Dashboard:**
- 📊 Métricas em tempo real (total, média de severidade, categorias)
- ➕ Formulário para criar novos chamados
- ▶️ Botão "Atender próximo"
- 🔍 Busca e cancelamento de chamados
- 📈 Gráfico de chamados por categoria
- ⭐ Ranking dos 5 chamados mais críticos

---

## 📁 Estrutura do Projeto

```
smartqueue/
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── .gitignore                         # Arquivos ignorados pelo Git
│
├── main.py                            # Interface CLI
├── app.py                             # Interface Web (Streamlit)
│
├── models/
│   ├── __init__.py
│   └── chamado.py                     # Modelo de dados (Dataclass)
│
├── services/
│   ├── __init__.py
│   ├── fila.py                        # Lógica da fila (Min-Heap)
│   ├── persistence.py                 # Persistência em CSV
│   ├── logger.py                      # Sistema de logging
│   └── reports.py                     # Relatórios e estatísticas
│
├── data/
│   └── chamados.csv                   # Dados persistidos
│
├── logs/
│   └── smartqueue.log                 # Arquivo de logs
│
└── tests/
    ├── __init__.py
    ├── conftest.py                    # Configuração do pytest
    ├── test_fila.py                   # Testes da fila
    ├── test_persistence.py            # Testes de persistência
    ├── test_reports.py                # Testes de relatórios
    └── test_logger.py                 # Testes de logging
```

---

## 🔧 Arquitetura e Componentes

### 1. **models/chamado.py** - Modelo de Dados

```python
@dataclass(order=True)
class Chamado:
    prioridade: int        # Calculada de severidade (-500 a -100)
    ordem_chegada: int     # Desempate (FIFO)
    id: str                # UUID truncado
    cliente: str           # Nome do cliente
    categoria: str         # Ex: "Suporte", "Vendas"
    severidade: int        # 1-5 (entrada do usuário)
    descricao: str         # Detalhes
    criado_em: str         # Timestamp
```

### 2. **services/fila.py** - Fila de Prioridade (Min-Heap)

```python
class FilaPrioridade:
    def __init__(self)
    def adicionar_chamado(chamado: Chamado) -> None
    def atender_proximo() -> Chamado | None
    def cancelar_chamado(id_chamado: str) -> bool
    def buscar_por_id(id_chamado: str) -> Chamado | None
    def listar_fila() -> list[Chamado]
    def obter_todos() -> list[Chamado]
    def esta_vazia() -> bool
```

**Algoritmo de priorização:**
- Usa `heapq` (Min-Heap binária)
- Prioridade negativa inverte ordem: -500 < -100
- `ordem_chegada` funciona como desempate automático

### 3. **services/persistence.py** - Persistência

```python
salvar_chamados(chamados: list[Chamado]) -> None      # Salva em CSV
carregar_chamados() -> list[Chamado]                  # Carrega do CSV
```

**Arquivo: `data/chamados.csv`**
```csv
id,cliente,categoria,severidade,descricao,prioridade,ordem_chegada,criado_em
81cecf81,artur,lazer,2,adicionar netflix a tela principal,-200,4,2026-06-17 18:34:26
8cc4b952,caio,lazer,2,comprar ingresso de cinema,-200,6,2026-06-17 18:45:22
```

### 4. **services/reports.py** - Relatórios

```python
heapsort(chamados: list[Chamado]) -> list[Chamado]    # O(n log n)
top_chamados(chamados: list[Chamado], n=5) -> list    # Top N críticos
calcular_estatisticas(chamados: list) -> dict         # Totais e médias
```

### 5. **services/logger.py** - Logging

```python
configurar_logger(log_file: str | None) -> logging.Logger
get_logger() -> logging.Logger
```

Logs salvos em `logs/smartqueue.log`:
```
2026-06-17 18:34:26 - INFO - Chamado criado: id=81cecf81, cliente=artur
2026-06-17 18:45:22 - INFO - Chamado atendido: id=81cecf81, cliente=artur
```

---

## 📊 Exemplos de Uso

### CLI: Criar e Atender Chamado

```bash
$ python main.py

===================================
         SMARTQUEUE
===================================
Escolha: 1

=== NOVO CHAMADO ===
Cliente: Maria Silva
Categoria: Suporte Crítico
Severidade (1-5): 5
Descrição: Banco de dados indisponível

✅ Chamado criado com sucesso!

Escolha: 2

=== ATENDENDO CHAMADO ===
Chamado(id=abc12345, cliente=Maria Silva, categoria=Suporte Crítico, 
severidade=5, prioridade=-500, criado_em=2026-06-17 19:00:00)
```

### Código: Usar FilaPrioridade Programaticamente

```python
from models.chamado import Chamado
from services.fila import FilaPrioridade

# Criar fila
fila = FilaPrioridade()

# Adicionar chamados
chamado1 = Chamado(
    prioridade=-100,          # Severidade 1
    ordem_chegada=1,
    cliente="João",
    categoria="Dúvida",
    severidade=1,
    descricao="Como usar?"
)

chamado2 = Chamado(
    prioridade=-500,          # Severidade 5
    ordem_chegada=2,
    cliente="Maria",
    categoria="Crítico",
    severidade=5,
    descricao="Sistema fora"
)

fila.adicionar_chamado(chamado1)
fila.adicionar_chamado(chamado2)

# Atender: Maria (severidade 5) sai primeiro
proximo = fila.atender_proximo()
print(f"Atendendo: {proximo.cliente}")  # Maria

# Listar ordenado
for chamado in fila.listar_fila():
    print(f"  - {chamado.cliente} (sev {chamado.severidade})")
```

---

## 🧪 Testes

Cobertura completa de testes com pytest.

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar testes específicos

```bash
pytest tests/test_fila.py -v              # Testes da fila
pytest tests/test_persistence.py -v       # Testes de persistência
pytest tests/test_reports.py -v           # Testes de relatórios
pytest tests/test_logger.py -v            # Testes de logging
```

### Gerar relatório de cobertura

```bash
pytest tests/ --cov=services --cov=models --cov-report=html
```

### Testes Principais

| Teste | Propósito |
|-------|-----------|
| `test_prioridade_maior_sai_primeiro` | Valida que severidade 5 sai antes de 1 |
| `test_fifo_em_empate` | Chamados com mesma severidade mantêm FIFO |
| `test_cancelar_chamado` | Remoção preserva propriedade de heap |
| `test_round_trip_preserva_dados` | CSV salva/carrega corretamente |
| `test_carregar_csv_legado_na_fila` | Compatibilidade com CSVs antigos |
| `test_heapsort_por_prioridade` | Ordenação por prioridade funciona |
| `test_estatisticas_por_categoria` | Contagem de categorias está correta |

---

## 📈 Complexidade de Tempo

Análise algorítmica das operações principais:

| Operação | Complexidade | Nota |
|----------|-------------|------|
| `adicionar_chamado` | **O(log n)** | heappush |
| `atender_proximo` | **O(log n)** | heappop |
| `buscar_por_id` | **O(n)** | busca linear |
| `cancelar_chamado` | **O(n)** | busca + heapify |
| `listar_fila` | **O(n log n)** | sorted (heapsort) |
| `calcular_estatisticas` | **O(n)** | um loop |
| `top_chamados(n)` | **O(n log n)** | heapsort completo |

---

## 🔍 Exemplo: Fluxo Completo

```
1. INICIALIZAÇÃO
   ├─ Carrega chamados de data/chamados.csv
   └─ Reconstrói fila (heapify)

2. USUÁRIO CRIA CHAMADO
   ├─ Input: cliente, categoria, severidade (1-5), descrição
   ├─ Calcula: prioridade = -(severidade * 100)
   ├─ Adiciona à heap: heappush(heap, chamado)
   └─ Salva: CSV atualizado

3. USUÁRIO ATENDE PRÓXIMO
   ├─ Retira: chamado = heappop(heap)
   ├─ Log: "Chamado atendido: id=..., cliente=..."
   └─ Salva: fila atualizada

4. USUÁRIO CONSULTA TOP 5
   ├─ Cria cópia da heap
   ├─ Ordena com heapsort: O(n log n)
   ├─ Retorna primeiros 5
   └─ Heap original inalterada

5. ENCERRAMENTO
   └─ Salva fila em CSV
```

---

## 🛠️ Configuração Avançada

### Alterar Arquivo de Log

Edite `services/logger.py`:

```python
LOG_FILE = "meus_logs/custom.log"  # Padrão: "logs/smartqueue.log"
```

### Alterar Arquivo de Dados

Edite `services/persistence.py`:

```python
ARQUIVO_CSV = "meus_dados/chamados.csv"  # Padrão: "data/chamados.csv"
```

### Customizar Cálculo de Prioridade

Em `main.py` ou `app.py`:

```python
def calcular_prioridade(severidade: int) -> int:
    # Padrão: -(severidade * 100)
    # Customizado:
    return -(severidade ** 2) * 10  # Mais agressivo
```

---

## 📝 Requisitos

```txt
streamlit>=1.32.0   # Interface web
pytest>=8.0.0       # Testes automatizados
```

**Compatibilidade:**
- Python 3.10+
- Funciona em Windows, Mac, Linux
- Sem dependências externas além das listadas

---

## 📚 Documentação Adicional

### Modelo de Dados Detalhado

**Prioridade = -(Severidade × 100)**

| Severidade | Prioridade | Significado |
|-----------|-----------|------------|
| 5 | -500 | Crítico (sistema fora, perda de dados) |
| 4 | -400 | Alto (funcionalidade principal afetada) |
| 3 | -300 | Médio (funcionalidade secundária) |
| 2 | -200 | Baixo (dúvida, sugestão) |
| 1 | -100 | Trivial (informação geral) |

**Ordem de Chegada (ordem_chegada)**

Incrementa automaticamente: 1, 2, 3, 4...  
Funciona como desempate quando `prioridade` é igual.

```python
Chamado(prioridade=-300, ordem_chegada=5)  # Mais antigo
Chamado(prioridade=-300, ordem_chegada=6)  # Mais novo
# Com mesma prioridade, o 5 sai primeiro (FIFO)
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para melhorias:

1. Crie uma branch: `git checkout -b feature/melhoria`
2. Commit suas mudanças: `git commit -m 'Adiciona X'`
3. Push: `git push origin feature/melhoria`
4. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto. Use livremente para fins educacionais e comerciais.

---

## 💬 Suporte

Para dúvidas ou problemas:

1. Verifique a seção de [Testes](#-testes) - pode haver teste similar
2. Revise os [Exemplos de Uso](#-exemplos-de-uso)
3. Consulte a [Documentação Adicional](#-documentação-adicional)
4. Verifique os logs em `logs/smartqueue.log`

---

## 🎓 Conceitos Aprendidos

Este projeto exemplifica:

- ✅ **Estruturas de Dados** - Min-heap binária
- ✅ **Algoritmos** - Heapsort O(n log n)
- ✅ **Padrões de Design** - Service Layer, Persistence
- ✅ **Python Avançado** - Dataclasses, type hints, context managers
- ✅ **Testes Unitários** - pytest, fixtures, mocking
- ✅ **Persistência** - CSV, serialização
- ✅ **Logging** - Auditoria e rastreabilidade
- ✅ **Interfaces** - CLI e Web

---

**Última atualização:** Junho de 2026

Aproveite! 🚀