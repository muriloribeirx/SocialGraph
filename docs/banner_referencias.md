<!-- Banner: contexto da aplicação — busca de referências usando Wikipedia e CrossRef -->

# BANNER — Contexto da Aplicação (Busca de Referências)

## INTRODUÇÃO

Esta aplicação visa gerar grafos de relacionamento entre páginas e publicações: ela combina buscas por links enciclopédicos (Wikipedia) com buscas de citações científicas (CrossRef). O objetivo é permitir exploração visual de conexões entre entidades (pessoas, temas, artigos acadêmicos) e facilitar a análise de caminhos conceituais e citações entre nós de interesse.

O sistema foi projetado para ser um protótipo extensível: aceita entrada via interface web, resolve títulos ou DOIs, constrói caminhos (BFS) entre pontos e gera visualizações interativas com PyVis.

## PROCEDIMENTOS METODOLÓGICOS

- Fontes de dados:
  - Wikipedia (via MediaWiki / wikipedia-api): extração de links entre artigos para construir arestas enciclopédicas.
  - CrossRef (via REST API) e OpenCitations (COCI, como complemento): resolução de DOIs, extração de referências (outgoing) e, quando disponível, recuperação de citers (incoming).

- Pipeline geral:
  1. Recepção de parâmetros do usuário (start, end, profundidade, número máximo de caminhos, fonte opcional: wikipedia/crossref).
  2. Normalização das entradas (títulos → DOI quando aplicável; limpeza de strings).
  3. Busca por caminhos usando BFS com limites de profundidade e expansão para evitar explosão combinatória.
  4. Extração de arestas (pares de nós) e geração de visualização interativa (HTML) com PyVis.

- Boas práticas implementadas:
  - Cache local para respostas CrossRef (requests-cache) para reduzir número de requisições e respeitar limites.
  - Extração heurística de DOIs a partir de campos “unstructured” em referências quando DOI explícito não está presente.
  - Sanitização de nomes de arquivo para compatibilidade com diferentes sistemas operacionais.

## RESULTADOS

- Artefatos gerados:
  - Arquivos HTML interativos em `static/` com visualizações dos grafos.
  - Funções que retornam arestas (list of tuples) para reutilização em análises programáticas.

- Observações sobre cobertura dos dados:
  - Wikipedia fornece ligações enciclopédicas amplas, porém pouco estruturadas para citações acadêmicas.
  - CrossRef fornece metadados ricos quando referências contêm DOIs; entretanto, muitos registros possuem referências sem DOI explícito — por isso adicionamos heurísticas e fallback.

## DISCUSSÃO

- Limitações atuais:
  - CrossRef nem sempre disponibiliza DOIs em referências; correspondência por título pode ser imprecisa e custosa em requisições.
  - Buscas profundas podem gerar explosão de estados — exigem limites rigorosos e idealmente processamento assíncrono (fila/worker).
  - Cobertura de incoming citations é incompleta sem fontes complementares (ex.: OpenCitations, Dimensions ou bancos comerciais).

- Riscos e cuidados éticos:
  - Respeitar termos de uso das APIs, rate limits e atribuição apropriada (ex.: Attribution para Wikimedia/CrossRef).
  - Evitar scraping agressivo (usar politeness, cache e backoff).

## CONCLUSÃO

O protótipo provê uma base funcional para extrair e visualizar relações tanto de enciclopédias (Wikipedia) quanto de literatura científica (CrossRef). Para evoluir o produto recomenda-se:

1. Implementar fila assíncrona (Celery/RQ) para tarefas longas e geração de artefatos sempre em background.
2. Integrar fontes adicionais (OpenCitations, Dimensions, CrossRef full-text matching) para melhorar recall de citações e cited-by.
3. Implementar estratégias de normalização e entity resolution (Wikidata/QIDs e DOIs canônicos) para reduzir ruído e duplicação.

Com essas melhorias, a plataforma evolui de protótipo de exploração para ferramenta utilizável em contextos de pesquisa, mídia e educação.

---
_Gerado automaticamente para o projeto SocialGraph — fornece um resumo conciso do contexto, métodos e recomendações para uso em exposições, pôsteres ou documentação._
