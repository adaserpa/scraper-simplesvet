# Estudo complementar — zRyyH/robo_simplesvet

Data: 04/10/2026. Base: commit 0f893c32eed9d83f94e367712fd37bcf139f1dc0. Método: leitura integral dos nove arquivos da árvore principal, inspeção dos scripts e análise estrutural dos quatro JSONs via GitHub. Nenhum programa executado, serviço autenticado acessado, credencial utilizada ou endpoint chamado.

Comparação com o [estudo top-down anterior](../2026-10-04-top-down/README.md). Este documento e o esquema associado foram produzidos no fork de Augusto; os dados e código deste segundo projeto não foram copiados para implementação.

## Conclusão

O maior complemento está nos JSONs financeiros: revelam rotas relativas e vínculos entre conciliação, lançamento, baixa e venda. Os scripts Playwright/requests, porém, apontam para Evoluservices, não para SimplesVet. Não existe código conectando esses scripts às amostras financeiras. O nome do repositório não comprova uma automação completa do SimplesVet.

## Inventário e fluxo

| Arquivo | Conteúdo | Contribuição |
|---|---|---|
| README.md | Só título. | Sem instruções ou objetivos detalhados. |
| .gitignore | Apenas meu_perfil. | Não exclui dumps ou configurações sensíveis. |
| scrap.py | Login Playwright em signin.evoluservices.com; fallback manual; dump de sessão. | Experimento de captura de sessão. |
| req.py | requests.Session com cookies e tentativa de Bearer; busca de pagamentos em app.evoluservices.com. | Experimento de reutilização de sessão HTTP. |
| test.py | GET de eventos de futebol no Sofascore. | Não testa a automação SimplesVet. |
| session_dump.json | Sessão Evoluservices; 16 cookies; localStorage/sessionStorage vazios na amostra. | Estrutura, sem reprodução dos valores. |
| conci.json | Envelope links/meta/data com um ConciliacaoCartaoLancamento. | Rota e vínculos financeiros. |
| conciliacao.json | Recurso do mesmo tipo, sem envelope. | Segunda amostra; não é cópia idêntica do recurso de conci.json. |
| lanca.json | Envelope com 11 LancamentoCategoria. | Categorias e vínculo com lançamento. |

Metadados: criado e último push em 05/10/2025; main é a branch padrão; nenhuma licença indicada pelo GitHub e nenhum LICENSE na árvore. Não presumir permissão irrestrita para copiar. Histórico completo e outras branches não foram auditados.

scrap.py abre Chromium visível → acessa login → tenta preencher username/password e submeter → em exceção permite login manual e espera Enter → aguarda 2s → captura cookies de todo o contexto e storages da página atual → grava session_dump.json → fecha.

req.py lê dump → copia cookies incluindo domain/path → monta User-Agent/Accept/Referer/Origin → procura nomes candidatos de token nos storages → se encontra, tenta Authorization Bearer → faz GET de pagamentos com timeout=20 → imprime corpo. O período, start e limit são fixos; não há loop de paginação.

Os scripts não carregam os três JSONs financeiros nem executam conciliação. Evidências: [scrap.py](https://github.com/zRyyH/robo_simplesvet/blob/0f893c32eed9d83f94e367712fd37bcf139f1dc0/scrap.py), [req.py](https://github.com/zRyyH/robo_simplesvet/blob/0f893c32eed9d83f94e367712fd37bcf139f1dc0/req.py), [test.py](https://github.com/zRyyH/robo_simplesvet/blob/0f893c32eed9d83f94e367712fd37bcf139f1dc0/test.py).

## Rotas financeiras nas amostras

Encontradas em links.self. São relativas: não há domínio registrado nesses JSONs. A associação ao SimplesVet é inferência pelo contexto e nomenclatura; precisa de confirmação na aplicação atual. O método HTTP, headers, autenticação e permissões não estão registrados.

| Fonte | Caminho | Query decodificada |
|---|---|---|
| conci.json | /app/v3/financeiro/conciliacao-cartao-lancamentos | _ordenarPor[baixa.incluidoEm]=asc; _ordenarPor[baixaMultipla.incluidoEm]=asc; _paginacao=false; conciliacao.id={conciliacao_id}. |
| lanca.json | /app/v3/financeiro/lancamentos-categoria | _paginacao=false; categoria.tipoInterno[]=TAN; categoria.tipoInterno[]=TOC; lancamento.conciliacaoCartaoLancamento.conciliacao.id={conciliacao_id}. |

TAN e TOC são códigos de filtro com significado ainda desconhecido. _paginacao=false sugere solicitação sem paginação; não prova ausência de limites. totalItems coincide com o número de itens nessas amostras, não estabelece completude em outros casos.

Fontes: [conci.json](https://github.com/zRyyH/robo_simplesvet/blob/0f893c32eed9d83f94e367712fd37bcf139f1dc0/conci.json), [lanca.json](https://github.com/zRyyH/robo_simplesvet/blob/0f893c32eed9d83f94e367712fd37bcf139f1dc0/lanca.json). IDs reais não reproduzidos.

## Modelo financeiro

A forma id/type/attributes/data lembra JSON:API; conformidade com o padrão não foi estabelecida.

| Recurso | Campos/vínculos relevantes | Aprendizado |
|---|---|---|
| ConciliacaoCartaoLancamento | conciliacao, lancamento, baixa, baixaMultipla, adiantamento, vendaBaixa. | Existe uma associação entre entidades distintas. |
| ConciliacaoCartao | tipo/status, bandeira, integrador, transferência origem/destino, valor, taxas, arredondamento e data. | Conciliação tem contexto e valores próprios. |
| Lancamento | conta, venceEm, incluidoEm, valor, parcela, pagoEm, bandeiraTipo, formaRecebimento, formaPagamento. | Vencimento e pagamento têm campos separados. |
| Baixa | baixadaEm, venda, caixa, nsu, valor, valorLiquido, taxas, numeroParcelas, vendaBaixaId e parcelamento. | Há registro de baixa ligado à venda. |
| Venda dentro de Baixa | id, status, incluidoEm, animal, cliente. | Cliente tem identificação própria; vínculo não depende apenas do nome. |
| LancamentoCategoria | id, valor, natureza, categoria e lancamentoId. | Categoria está associada ao lançamento por ID. |
| FormaRecebimento e tipos | baixaAutomatica, parcelamentos, conta/integrador, aceitaPix, prazos e taxas. | Configuração financeira também integra o modelo. |

baixaMultipla, adiantamento e vendaBaixa estão nulos nas amostras; animal da venda está vazio: sua estrutura útil não é conhecida. Não inventar atributos ou cardinalidades para esses campos.

[esquema-campos.json](esquema-campos.json) contém apenas caminhos e tipos encontrados: 518 em conci.json, 512 em conciliacao.json e 21 em lanca.json. Inclui containers e repetições estruturais em caminhos diferentes; não são contagens de entidades independentes ou campos únicos do sistema. Nenhum valor financeiro, nome de cliente, ID, conta bancária ou sessão foi copiado.

## Comparação com o primeiro estudo

| Dimensão | Primeiro projeto | Este projeto | Complemento |
|---|---|---|---|
| Organização | Classes, configuração, coletores, formatador e logs. | Scripts e amostras avulsas. | Primeiro serve melhor como referência de organização. |
| Navegador | Selenium no SimplesVet. | Playwright na Evoluservices. | Pista de captura de sessão, não login SimplesVet validado. |
| Cookies para requests | Nome/valor explicitamente. | Também domain/path. | Melhoria parcial na transferência da sessão. |
| HTTP | PDF da agenda SimplesVet. | Pagamentos Evoluservices. | Combinação navegador/HTTP em serviços diferentes. |
| Financeiro | Vendas exportadas; classificação por nome/valor positivo. | IDs, baixas, lançamentos e conciliação em JSON. | Principal novidade: registros financeiros relacionados. |
| Endpoints | Relatório agenda e telas vendas/eventos. | Duas rotas relativas nas amostras. | Novos candidatos a validar, sem contrato completo. |
| Evidência | Código não executado. | Código e amostras sem proveniência documentada. | Nenhuma execução atual comprovada. |

Para o HUVet, investigar venda → baixa → lançamento → conciliação é mais promissor do que assumir que venda positiva significa pagamento recebido. Mas estas amostras são de conciliação de cartão: não demonstram integração com GRU/SisGRU ou regras para Pix/boleto. Mesmo pagoEm/baixadaEm exigem confirmação de significado e preenchimento.

## Revisão crítica

1. Há credencial embutida no código e dump de sessão versionado. Não utilizados nem reproduzidos. A existência é observada; validade atual não foi testada.
2. Não há confirmação de identidade, empresa ou login antes de salvar. Enter manual não é prova de autenticação.
3. Cookies cobrem o contexto, mas storages apenas a origem atual; autenticação entre domínios pode ter estado não capturado.
4. IndexedDB aparece só comentado. Storages vazios não validam a tentativa de usar Bearer.
5. Procurar token/auth_token/access_token/id_token/jwt/authorization é heurística; não demonstra o contrato de autenticação do serviço. id_token não deve ser presumido equivalente a access_token.
6. Cópia de cookies mantém domain/path, mas não preserva explicitamente secure/expires e todos os atributos.
7. GET possui timeout, mas não exige status correto, JSON válido, esquema, sessão válida ou completude. Imprimir todo o corpo pode expor dados nos logs.
8. Não há paginação, reconciliação, checkpoint, relatório de falhas ou testes de aplicação.
9. networkidle e sleep não comprovam conclusão do login nem de operações de negócio.
10. Não há requirements/lockfile ou configuração externa; só instruções de instalação em comentários.
11. test.py consulta outro serviço e assume data[0]; não oferece cobertura da automação.
12. JSONs não documentam request completo, domínio de origem, processo de coleta ou timestamp de extração. A origem é pendente.

## Continuidade sugerida

- Registrar as duas rotas como candidatos com evidência de amostra, não endpoints validados.
- Observar chamadas legítimas no SimplesVet para confirmar domínio, método, parâmetros, sessão e schema.
- Confirmar vínculos por IDs de venda, baixa, cliente, lançamento e conciliação.
- Estudar exemplos com os campos atualmente nulos preenchidos.
- Distinguir valor de venda, baixa, líquido e recebimento conciliado.
- Mapear meios de pagamento não cartão e integração GRU/SisGRU.
- Implementar somente após critérios de identidade, completude e falha definidos.

O estudo foi registrado apenas nesta pasta de documentação do fork. As fontes originais e a automação anterior permanecem preservadas. Não houve utilização de credenciais públicas nem acesso a contas de terceiros.
