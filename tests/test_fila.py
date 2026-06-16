from services.fila import FilaPrioridade
from models.chamado import Chamado


def criar_chamado_teste(
    severidade: int,
    cliente: str = "Teste"
) -> Chamado:

    return Chamado(
        prioridade=-(severidade * 100),
        cliente=cliente,
        categoria="Teste",
        severidade=severidade,
        descricao="Descrição de teste"
    )


def test_fila_inicia_vazia():

    fila = FilaPrioridade()

    assert fila.esta_vazia() is True
    assert fila.obter_tamanho_fila() == 0


def test_adicionar_chamado():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(3)

    fila.adicionar_chamado(chamado)

    assert fila.esta_vazia() is False
    assert fila.obter_tamanho_fila() == 1


def test_visualizar_proximo():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(
        4,
        "Pedro"
    )

    fila.adicionar_chamado(chamado)

    proximo = fila.visualizar_proximo()

    assert proximo.cliente == "Pedro"
    assert proximo.severidade == 4


def test_prioridade_maior_sai_primeiro():

    fila = FilaPrioridade()

    baixo = criar_chamado_teste(
        1,
        "Baixa"
    )

    alto = criar_chamado_teste(
        5,
        "Alta"
    )

    fila.adicionar_chamado(baixo)
    fila.adicionar_chamado(alto)

    atendido = fila.atender_proximo()

    assert atendido.cliente == "Alta"
    assert atendido.severidade == 5


def test_atender_fila_vazia():

    fila = FilaPrioridade()

    resultado = fila.atender_proximo()

    assert resultado is None


def test_remover_reduz_tamanho():

    fila = FilaPrioridade()

    fila.adicionar_chamado(
        criar_chamado_teste(3)
    )

    fila.atender_proximo()

    assert fila.obter_tamanho_fila() == 0