import streamlit as st

from models.chamado import Chamado
from services.fila import FilaPrioridade
from services.logger import get_logger
from services.persistence import (
    carregar_chamados,
    salvar_chamados,
)
from services.reports import (
    calcular_estatisticas,
    top_chamados,
)

logger = get_logger()


def calcular_prioridade(severidade: int) -> int:
    return -(severidade * 100)


def carregar_fila() -> FilaPrioridade:

    fila = FilaPrioridade()

    for chamado in carregar_chamados():
        fila.carregar_chamado(chamado)

    return fila


def salvar_fila(fila: FilaPrioridade) -> None:

    salvar_chamados(fila.obter_todos())


def chamados_para_tabela(
    chamados: list[Chamado],
) -> list[dict]:

    return [
        {
            "ID": chamado.id,
            "Cliente": chamado.cliente,
            "Categoria": chamado.categoria,
            "Severidade": chamado.severidade,
            "Descrição": chamado.descricao,
            "Criado em": chamado.criado_em,
        }
        for chamado in chamados
    ]


def inicializar_sessao() -> None:

    if "fila" not in st.session_state:
        st.session_state.fila = carregar_fila()


def main() -> None:

    st.set_page_config(
        page_title="SmartQueue",
        page_icon="📋",
        layout="wide",
    )

    inicializar_sessao()
    fila: FilaPrioridade = st.session_state.fila

    st.title("📋 SmartQueue Dashboard")
    st.caption(
        "Painel web da fila de chamados com prioridade"
    )

    stats = calcular_estatisticas(
        fila.obter_todos()
    )

    col_total, col_media, col_categorias = st.columns(3)

    col_total.metric(
        "Total de chamados",
        stats["total"],
    )

    col_media.metric(
        "Média de severidade",
        (
            f"{stats['media_severidade']:.2f}"
            if stats["total"]
            else "—"
        ),
    )

    col_categorias.metric(
        "Categorias",
        len(stats["por_categoria"]),
    )

    with st.sidebar:
        st.header("Ações")

        with st.form("novo_chamado"):
            st.subheader("Novo chamado")

            cliente = st.text_input("Cliente")
            categoria = st.text_input("Categoria")
            severidade = st.slider(
                "Severidade",
                min_value=1,
                max_value=5,
                value=3,
            )
            descricao = st.text_area("Descrição")

            criar = st.form_submit_button(
                "Criar chamado",
                use_container_width=True,
            )

        if criar:
            if not cliente.strip() or not categoria.strip():
                st.error(
                    "Cliente e categoria são obrigatórios."
                )
            else:
                try:
                    chamado = Chamado(
                        prioridade=calcular_prioridade(
                            severidade
                        ),
                        ordem_chegada=0,
                        cliente=cliente.strip(),
                        categoria=categoria.strip(),
                        severidade=severidade,
                        descricao=descricao.strip(),
                    )

                    fila.adicionar_chamado(chamado)
                    salvar_fila(fila)

                    logger.info(
                        "Chamado criado: id=%s, "
                        "cliente=%s",
                        chamado.id,
                        chamado.cliente,
                    )

                    st.success(
                        f"Chamado {chamado.id} criado!"
                    )
                    st.rerun()
                except Exception as erro:
                    logger.error(
                        "Erro ao criar chamado: %s",
                        erro,
                    )
                    st.error("Erro ao criar chamado.")

        st.divider()

        if st.button(
            "Atender próximo",
            use_container_width=True,
        ):
            try:
                chamado = fila.atender_proximo()

                if chamado is None:
                    st.warning("Fila vazia.")
                else:
                    salvar_fila(fila)

                    logger.info(
                        "Chamado atendido: id=%s, "
                        "cliente=%s",
                        chamado.id,
                        chamado.cliente,
                    )

                    st.success(
                        f"Atendido: {chamado.cliente} "
                        f"({chamado.id})"
                    )
                    st.rerun()
            except Exception as erro:
                logger.error(
                    "Erro ao atender chamado: %s",
                    erro,
                )
                st.error("Erro ao atender chamado.")

        st.divider()
        st.subheader("Cancelar chamado")

        id_cancelar = st.text_input("ID do chamado")

        if st.button(
            "Cancelar",
            use_container_width=True,
        ):
            if not id_cancelar.strip():
                st.error("Informe o ID do chamado.")
            elif fila.cancelar_chamado(
                id_cancelar.strip()
            ):
                salvar_fila(fila)
                st.success("Chamado cancelado.")
                st.rerun()
            else:
                st.error("Chamado não encontrado.")

        st.divider()

        if st.button(
            "Recarregar dados",
            use_container_width=True,
        ):
            st.session_state.fila = carregar_fila()
            st.rerun()

    col_fila, col_top = st.columns([2, 1])

    with col_fila:
        st.subheader("Fila de chamados")

        chamados = fila.listar_fila()

        if chamados:
            st.dataframe(
                chamados_para_tabela(chamados),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Nenhum chamado na fila.")

    with col_top:
        st.subheader("Top críticos")

        criticos = top_chamados(
            fila.obter_todos(),
            n=5,
        )

        if criticos:
            st.dataframe(
                chamados_para_tabela(criticos),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Nenhum chamado na fila.")

    st.subheader("Chamados por categoria")

    if stats["por_categoria"]:
        st.bar_chart(stats["por_categoria"])
    else:
        st.info("Sem dados para exibir.")


if __name__ == "__main__":
    main()
