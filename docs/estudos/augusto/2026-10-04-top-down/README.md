# Estudo do fork SimplesVet — v0.1

Data: 04/10/2026. Responsável pelo estudo: Codex, a pedido de Augusto. Projeto original: [luabelo/automacao-simplesvet](https://github.com/luabelo/automacao-simplesvet), autoria registrada no histórico: Luana Belo. Fork estudado: [adaserpa/scraper-simplesvet](https://github.com/adaserpa/scraper-simplesvet).

**Conclusão:** o projeto é uma referência útil de extração híbrida: Selenium autentica; uma requisição HTTP com cookies baixa a agenda; vendas e eventos clínicos usam exportações da interface. Seu resumo final é específico da Catland e contém limitações de confiabilidade e interpretação dos dados. Não é uma automação Playwright implementada, apesar da descrição atual do fork.

## Ordem de leitura

1. [Método, versão e limites](01-metodo-e-escopo.md).
2. [Arquitetura e fluxos](02-arquitetura-e-fluxos.md).
3. [Interações e dados](03-interacoes-e-dados.md).
4. [Revisão crítica](04-revisao-critica.md).
5. [Reaproveitamento e proposta Playwright](05-reaproveitamento-e-playwright.md).
6. [Registro da publicação e continuidade](06-registro-e-continuidade.md).

## Inventários reutilizáveis

- [Arquivos](inventario-arquivos.csv): todos os 21 arquivos versionados na base.
- [Símbolos](inventario-simbolos.csv): classes e funções, com linhas.
- [Interações](inventario-interacoes.csv): seletores, URLs e literais relevantes; inventário automatizado com revisão humana, incluindo caminhos auxiliares.
- [Dicionário de dados](dicionario-dados.csv): campos efetivamente usados e significado.
- [Achados](achados.csv): evidências, prioridade e recomendação.
- [Manifesto](manifesto.json): commit, hashes e verificações.
- [Verificador](verificar_estudo.py): verifica fontes, sintaxe e inventários sem importar ou executar a automação.

A pasta `docs/estudos/augusto/2026-10-04-top-down/` é documentação do fork. Não altera o código original e não contém credenciais, cookies, downloads clínicos ou dados reais de tutores. Referências de código apontam para a versão fixa 563e4ae84ccd1d60ddf166ad93a08041a4f637c9, evitando que mudanças futuras alterem a evidência.

