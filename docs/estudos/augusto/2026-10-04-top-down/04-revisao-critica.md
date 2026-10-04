# 4. Revisão crítica

As prioridades abaixo são de confiabilidade para um futuro coletor. São diagnósticos da fonte e riscos deduzidos, sem testes no SimplesVet.

| ID | Prioridade | Achado e consequência | Evidência |
|---|---|---|---|
| A01 | Alta | Sucesso global não representa sucesso de todos os meses. Erros mensais são registrados, mas run pode retornar True; ausência/falha de extração pode virar “nenhum encontrado”. | [src/scraper/scraper.py:104–166](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/scraper.py#L104-L166) |
| A02 | Alta | main só avisa se format_data retorna False; não muda success nesse caso. A saída pode ser 0 mesmo com resumo ausente. Há ainda input(), que bloqueia uso não interativo. | [main.py:33–53](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/main.py#L33-L53) |
| A03 | Alta | Valor positivo de qualquer venda para animal de mesmo nome é chamado pago/externo. Não verifica recebimento, status da venda, serviço ou tutor; homônimos e serviços distintos contaminam classificação. | [src/formatter/vaccine_test_processor.py:154–191](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/vaccine_test_processor.py#L154-L191) |
| A04 | Alta | Receita é soma de Líquido por padrões amplos; não é pagamento conciliado. Status da venda e filtro dos usuários clínicos não são usados nessa soma. | [src/formatter/vaccine_test_processor.py:291–360](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/vaccine_test_processor.py#L291-L360) |
| A05 | Alta | Vendas pode seguir após falha do período. Calendário usa while True e dia por texto sem confirmar mês da célula. Risco de período incorreto ou loop sem limite. | [src/scraper/venda_extractor.py:56–114](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/venda_extractor.py#L56-L114) |
| A06 | Alta | Procura CSV mais recente entre todos, sem baseline ou vínculo à ação. Um arquivo antigo ou de outra tarefa pode ser aceito. | [src/scraper/venda_extractor.py:118–150](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/venda_extractor.py#L118-L150) |
| A07 | Alta | HTTP sem timeout e PDF aceito por status 200; não valida conteúdo/redirect. HTML de login pode virar PDF; conexão pode ficar esperando. | [src/scraper/appointment_extractor.py:108–140](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/appointment_extractor.py#L108-L140) |
| A08 | Alta | Resumo de vacinas falho pode continuar e apresentar zero. Zero significa ausência? dado indisponível? Aqui os estados se confundem. | [src/formatter/data_formatter.py:324–343](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/data_formatter.py#L324-L343); [src/formatter/data_formatter.py:455–483](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/data_formatter.py#L455-L483) |
| A09 | Média | Login por URL/título sem login ou seletores genéricos pode aceitar página indevida; estado não é revalidado durante coleta. | [src/scraper/simplesvet_actions.py:171–209](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/simplesvet_actions.py#L171-L209) |
| A10 | Média | Coletor mantém extensão .xlsx, mas processador exige .xls; layout/engine/cabeçalhos não validados. Comentário HTML não prova formato. | [src/scraper/procedure_extractor.py:306–336](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/procedure_extractor.py#L306-L336); [src/formatter/vaccine_test_processor.py:54–117](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/vaccine_test_processor.py#L54-L117) |
| A11 | Média | Correção do chromedriver força chromedriver.exe quando o caminho não termina em .exe; tende a quebrar Linux/macOS. Firefox não configura mesma política de downloads. | [src/scraper/webdriver_manager.py:81–119](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/webdriver_manager.py#L81-L119) |
| A12 | Média | PDFs usam heurísticas de nomes e descarte por palavras; tabela de uma linha pode desaparecer, erros podem produzir saída parcial. | [src/scraper/pdf_converter.py:98–139](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/pdf_converter.py#L98-L139); [src/scraper/pdf_converter.py:142–283](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/pdf_converter.py#L142-L283) |
| A13 | Média | Contagem de linhas de venda ignora Quantidade e cancelamento; totais iguais não validam os mesmos registros. | [src/formatter/data_formatter.py:42–75](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/data_formatter.py#L42-L75); [src/formatter/data_formatter.py:259–271](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/data_formatter.py#L259-L271) |
| A14 | Média | Limpeza e nomes fixos removem/sobrescrevem arquivos sem confirmar identidade; não há histórico ou execução isolada. | [src/scraper/appointment_extractor.py:237–263](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/appointment_extractor.py#L237-L263); [src/scraper/procedure_extractor.py:240–336](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/procedure_extractor.py#L240-L336) |
| A15 | Média | Seleção do calendário de eventos pode parar antes do mês correto; retornos da seleção do dia são ignorados. | [src/scraper/procedure_extractor.py:122–196](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/procedure_extractor.py#L122-L196) |
| A16 | Média | Colunas esperadas não são exigidas; conversão numérica pode produzir NaN e perda silenciosa. | [src/scraper/venda_extractor.py:152–188](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/venda_extractor.py#L152-L188) |
| A17 | Baixa | logging do JSON não chega ao logger global; get_logging_config não é chamado. Configuração aparenta efeito que não tem no fluxo. | [src/scraper/config.py:167–174](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/config.py#L167-L174); [src/scraper/logger.py:9–35](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/logger.py#L9-L35); [src/scraper/logger.py:90–91](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/logger.py#L90-L91) |
| A18 | Média | Meses/arquivos não têm checkpoint, hash, validação de completude ou manifesto por execução. Dados velhos podem participar de relatório novo. | [main.py:30–39](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/main.py#L30-L39); [src/formatter/data_formatter.py:214–257](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/formatter/data_formatter.py#L214-L257) |

## Pontos positivos

- Configuração separada, intervalo mensal calculado com calendar.monthrange e validação antes de abrir navegador.
- Coletores separados para agenda, vendas e eventos; fachada evita sobrecarregar main.
- Fechamento em finally e logs com rotação.
- Compartilhamento de sessão entre navegador e HTTP: reduz cliques no fluxo da agenda.
- Preservação do PDF de agenda e exportações estruturadas quando disponíveis.
- Tentativa de tratar tabelas entre páginas e comparar fontes independentes.
- Categorias de castração centralizadas, em vez de duplicar toda a lógica por modalidade.
- .gitignore exclui configuração real, logs e downloads. Isso previne inclusão normal pelo Git; não apaga arquivos previamente versionados nem substitui proteção local.

## Acoplamento ao contexto Catland

Dois usuários específicos, padrões de produtos/procedimentos, modalidades de castração, classificação interno/externo e formato do resumo fazem parte da regra local. Não são comportamentos universais do SimplesVet. INTERNAL_CLIENTS está definido, mas não é usado para classificar. Algumas constantes de tipos não dirigem todas as chamadas, que repetem literais.

## O que não foi comprovado

- Nenhum dos achados demonstra falha ocorrida em produção; cenários são derivados da fonte.
- Sintaxe válida não verifica imports, dependências, compatibilidade de versões ou navegador.
- Não há testes versionados, workflow CI ou amostras de dados na árvore examinada.
- Não foi feita varredura de segredos de todo o histórico; a configuração atual contém placeholders.
- Não sabemos quantidade real de registros, precisão das heurísticas nem disponibilidade atual das rotas.

Prioridade prática: primeiro impedir falso sucesso e perda de identidade; depois controlar sessão/downloads e formato; só então adaptar indicadores.

