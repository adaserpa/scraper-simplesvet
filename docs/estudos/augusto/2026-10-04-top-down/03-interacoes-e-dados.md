# 3. Interações e dados

## Endpoints conhecidos e desconhecidos

“Endpoint” é o endereço que recebe uma solicitação. Nem todo endpoint retorna JSON: este projeto conhece uma rota que entrega relatório PDF.

| Recurso | Caminho/contrato visto no código | Evidência e limite |
|---|---|---|
| Login | https://app.simples.vet/login/login.php | URL no template; envio do formulário pelo Selenium. Método/payload HTTP do login não reconstruídos. |
| Agenda | /agenda/agenda_relatorio_v2.php | GET direto. Query: tipo=lista; data=DD/MM/YYYY-DD/MM/YYYY. Corpo esperado: PDF. |
| Vendas | /principal/venda/venda.php | Navegação do navegador. Exportação acionada por link rel=xls_vendas; URL/payload real desconhecidos. |
| Atendimentos | /consulta/atendimento/atendimento.php | Navegação do navegador. Evento value=5 ou 7; link rel=xls; URL/payload real desconhecidos. |

A única chamada HTTP explícita à aplicação fora do navegador é session.get do relatório da agenda. Não há descoberta de endpoints JSON, cliente genérico da aplicação, tokens CSRF ou documentação do servidor. Não se deve inventar o endpoint de vendas com base no valor “xls_vendas”.

Evidência do contrato da agenda: [src/scraper/appointment_extractor.py:78–142](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/src/scraper/appointment_extractor.py#L78-L142).

### Solicitação da agenda

- O navegador deve existir e o fluxo principal exige is_logged_in.
- Cookies são copiados só por nome e valor; escopo domain/path e demais atributos não são preservados explicitamente.
- User-Agent vem de navigator.userAgent; Referer é raiz da aplicação.
- requests segue seu comportamento padrão de redirects; não há timeout configurado, nem conferência de URL final, Content-Type ou assinatura PDF.
- O status 200 é usado como critério para salvar. Uma página HTML de login/erro retornada com 200 pode ser gravada como .pdf.
- O arquivo é gravado diretamente no destino; interrupção pode deixar arquivo incompleto.
- Requisição observada no código não comprova que cookies bastam hoje, que permissões sejam iguais em outras contas ou que os parâmetros permaneçam válidos.

## Seletores principais

| Operação | Evidências da interface |
|---|---|
| Login | l_usu_var_email; l_usu_var_senha; btn_login; alternativas genéricas por type. |
| Confirmação | dashboard, main-content, user-menu, sidebar e título/URL sem login. |
| Período vendas | p__ven_dat_data_text; texto “Selecionar período”. |
| Período eventos | p__eve_dat_data_text; p__tev_int_codigo. |
| Calendários | .calendar.left/right; th[colspan='5']; th.next/prev; td.available. |
| Relatórios | p__btn_relatorio. |
| Exportação vendas | a.p__btn_exportar[rel='xls_vendas']. |
| Exportação eventos | a.p__btn_exportar[rel='xls']. |

Inventário detalhado com arquivo/linha em [inventario-interacoes.csv](inventario-interacoes.csv). Seletores dinâmicos aparecem como modelos, não como observação de DOM atual. O projeto lê cabeçalhos/texto de calendário, cookies, User-Agent, URL e título; não mapeia atributos ocultos de animais/clientes. Não extrai IDs de prontuário nem reconstrói abertura de ficha.

## Contratos de arquivos

| Artefato | Origem | Unidade e conteúdo |
|---|---|---|
| YYYYMM-agendamentos.pdf | GET relatório | Documento visual, não modelo de entidades. |
| YYYYMM-agendamentos.xlsx | Conversor | Uma linha interpretada de agendamento; sete campos textuais. |
| CSV de vendas | Exportação UI | Linhas exportadas; colunas sugerem itens de venda. Granularidade precisa de amostra. |
| YYYYMM-vendas.xlsx | Transformação CSV | Subconjunto de 14 campos, cinco numéricos. |
| YYYYMM-vacina.xls/.xlsx | Exportação evento 5 | Eventos com Animal, Usuario e Resumo usados pelo processador. |
| YYYYMM-exames.xls/.xlsx | Exportação evento 7 | Eventos; apenas testes FIV/FeLV entram nas contagens específicas. |
| YYYYMM-formatado.xlsx | Regras Catland | Agregados Item/Valor; não mantém rastreabilidade individual. |

A agenda não oferece ID estável no conjunto extraído. Venda é preservado no XLSX, mas não usado para reconciliar procedimento clínico e financeiro. O código não demonstra ID de evento/item nem CPF/ID do tutor. Clientes/animais aparecem principalmente por nomes.

## Transformações e perdas

Agenda: cabeçalhos reconhecidos por palavras; sem cabeçalho assume posições cliente, animal, tipo, data, hora, status. Veterinário é inferido de linhas maiúsculas com filtros e propagado entre tabelas/páginas. Observações são excluídas por expressões como valor, observ, v4, v5 e queixa. Tabelas com menos de duas linhas são ignoradas antes do parser. Não há relatório estruturado de linhas rejeitadas nem contagem esperada do servidor. Erros podem retornar registros parciais já coletados.

Vendas: colunas ausentes são silenciosamente omitidas. Pontos são removidos, vírgulas viram pontos e caracteres não numéricos são retirados; valores inválidos viram NaN. É apropriado apenas se a entrada seguir o formato brasileiro presumido. A limpeza pode mudar valores já numéricos em outro padrão.

Eventos: o comentário diz “HTML disfarçado de XLS”, mas a implementação usa read_excel com xlrd. Sem arquivo real não podemos determinar se é XLS binário, HTML ou outro formato. Assume linhas específicas de cabeçalho e apenas extensão .xls no processador, embora o coletor aceite .xlsx.

Resumo: contagens de castração usam número de linhas, não soma de Quantidade; padrões de texto podem misturar itens. Totais iguais não provam correspondência por paciente, serviço ou data. “Valor arrecadado” soma Líquido das vendas; não consulta caixa, pagamentos ou conciliação.

## Implicação para o HUVet

Agenda, evento clínico, item de venda e pagamento são registros diferentes. A automação própria precisa preservá-los separadamente e criar vínculos por identificadores quando disponíveis. Um mesmo animal pode ter vários serviços, várias vendas e pagamentos posteriores. Nome igual não é identidade suficiente; valor de venda não é comprovante de recebimento.

O [dicionário](dicionario-dados.csv) distingue campos de origem, derivados e metadados, incluindo ausências. O passo futuro é confirmar IDs e relações nas respostas reais, sem presumir que este repositório já as documentou.

