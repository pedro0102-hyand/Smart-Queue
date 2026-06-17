from services.logger import configurar_logger


def test_logger_registra_mensagens(tmp_path):

    log_file = tmp_path / "smartqueue.log"

    logger = configurar_logger(str(log_file))

    logger.info("Chamado criado: id=abc123, cliente=Maria")
    logger.info("Chamado atendido: id=abc123, cliente=Maria")
    logger.error("Erro ao salvar chamados: disco cheio")

    conteudo = log_file.read_text(encoding="utf-8")

    assert "INFO - Chamado criado: id=abc123, cliente=Maria" in conteudo
    assert "INFO - Chamado atendido: id=abc123, cliente=Maria" in conteudo
    assert "ERROR - Erro ao salvar chamados: disco cheio" in conteudo
