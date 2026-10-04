# 1. Método, versão e limites

## Pergunta do estudo

O que podemos aprender com esta automação para criar uma solução própria, inicialmente com Playwright e endpoints internos do SimplesVet?

O estudo seguiu oito etapas: identidade; arquitetura; fluxos; interações com SimplesVet; dados; revisão crítica; tradução para uma automação própria; registro dos resultados no fork.

## Base examinada

- Commit: `563e4ae84ccd1d60ddf166ad93a08041a4f637c9`, de 27/04/2026, mensagem “fix: update requirements and improve webdriver path handling”.
- Branch de origem: `main`; fork público de `luabelo/automacao-simplesvet`.
- 21 arquivos versionados; 15 arquivos Python, aproximadamente 3.300 linhas, incluindo comentários e linhas vazias. Contagens precisas estão nos inventários.
- Árvore completa retornada pelo GitHub, sem truncamento. Conteúdo integral dos arquivos obtido pelo conector GitHub e conferido por hashes de blobs.
- Leitura integral das fontes, acompanhamento manual das chamadas e análise da árvore sintática Python (AST): uma representação do código que permite listar funções sem executá-las.
- Metadados do original consultados: inclui a indicação `wip-do-not-use`. Isso é um sinal declarado pelo mantenedor, não uma prova de falha.
- Histórico examinado: dez commits recentes; mostra evolução de exportação de vendas, eventos, resumo e correções de PDFs multipágina. A coleção de issues do original retornou três itens, todos pull requests. Não foi realizada auditoria de todo o histórico nem de todas as branches.

## Classes de evidência

| Classe | Significado |
|---|---|
| DOC | Declaração do README, comentários ou metadados; pode divergir da implementação. |
| CODE | Comportamento observado na fonte fixa; não implica funcionamento atual no serviço. |
| INF | Consequência ou risco deduzido da fonte, com cenário explicado. |
| PEND | Precisa de arquivos reais, observação de rede ou execução futura. |

Não houve execução do programa, importação de seus módulos, instalação de suas dependências, login no SimplesVet ou chamada a endpoints do SimplesVet. As verificações locais foram parsing sintático, inventários, referências e integridade de arquivos. Portanto não há evidência EXEC de funcionamento da automação.

Não foram fornecidos PDFs/CSVs/XLS de exemplo. A qualidade real da extração, formato real dos arquivos e comportamento atual das telas permanecem pendentes. Não temos PHP de servidor: caminhos terminados em .php aqui são URLs consumidas pelo cliente.

## Licença e atribuição

[LICENSE:1–41](https://github.com/adaserpa/scraper-simplesvet/blob/563e4ae84ccd1d60ddf166ad93a08041a4f637c9/LICENSE#L1-L41) declara Creative Commons Atribuição–NãoComercial 4.0 e restringe uso comercial sem autorização do autor. O estudo preserva a autoria e não redefine a licença. O GitHub identifica a licença como “Other”; não se deve presumir MIT ou liberdade irrestrita de copiar.

A reutilização de trechos deve considerar os termos registrados. Uma implementação própria pode aproveitar os aprendizados técnicos, mas copiar/adaptar código precisa manter atribuição e observar a licença. Este estudo registra o conteúdo do arquivo, sem fazer parecer jurídico sobre o enquadramento do uso institucional.

## Fontes externas de apoio

Documentação oficial consultada em 04/10/2026, para fundamentar propostas, sem afirmar que o SimplesVet implementa esses recursos:

- [Playwright APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext): requisições e compartilhamento de cookies com o contexto do navegador.
- [Downloads](https://playwright.dev/python/docs/downloads): captura do download associado à ação.
- [Auto-waiting](https://playwright.dev/python/docs/actionability): verificações automáticas antes de interações.
- [Authentication](https://playwright.dev/python/docs/auth): reutilização e proteção do estado autenticado.

