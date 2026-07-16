Today 8:30 PM
first_prompts_to_ai(31).zip
Zip Archive
prompt_library(31).zip
Zip Archive
tell_AI_read_before_all(31).md
File
zz_read_only_if_modifying_startup_delivery(12).md
File

kanda_reasoner__source_archive_part01_of_01(32).zip
Zip Archive
kanda_reasoner__png_assets_part01_of_01(31).zip
Zip Archive
kanda_reasoner__error_memory_manifest(32).json
File
kanda_reasoner__error_memory_full(32).zip
Zip Archive
kanda_reasoner__error_memory_ai_prompt(32).md
File
kanda_reasoner__error_lessons_compact(32).json
File
kanda_reasoner__ai_handoff_upload_readme(32).txt
Document
kanda_reasoner__ai_handoff_upload(32).zip
Zip Archive
kanda_reasoner__ai_handoff_all_in_one(31).zip
Zip Archive
_RUN_COLLECTOR_STATUS(32).txt
Document

000 HOW TO(1).md
File
chat 056-075.md
File
continue

A sequência 080–086 foi confirmada pelo ponto de parada anterior e pela ordem atual das Classes 08 e 09. O próximo alvo após este ciclo é anti_hallucination_master_protocol_full.md.
ADAPTIVE CYCLE RESULT — PROMPTS 080–086

Os sete prompts foram auditados sequencialmente. Cada alvo primário foi formalmente encerrado antes da abertura do seguinte.

Total de fonte canônica auditada:

    Prompt 080: 244 linhas

    Prompt 081: 449 linhas

    Prompt 082: 226 linhas

    Prompt 083: 35 linhas

    Prompt 084: 24 linhas

    Prompt 085: 187 linhas

    Prompt 086: 31 linhas

    Total: 1.196 linhas

As cópias presentes no Prompt Library ZIP e no source archive são byte a byte idênticas para os sete prompts.

Nenhum arquivo foi modificado.

Nenhum validador foi executado.

Nenhum resultado de validação foi reivindicado.
PROMPT AUDIT REPORT 080
Identity

AUDIT_ID:

A080-20260715-REVIEW

PROMPT:

python_refactoring.md

CANONICAL ID:

python_refactoring

DISPLAY NAME:

Python Refactoring

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/08_python_engineering_core/python_refactoring.md

SOURCE SHA-256:

4600a2361197b8eaad632d7fd1b1f6f80c1b0c2aeb16d5ace3ac32b0ba8b15bd

METADATA SHA-256:

e28477608eeb7a5e15be1781416ca5222564d07c6749fbe738569c7b59c0051d

SOURCE SIZE:

9.510 bytes

SOURCE LENGTH:

244 linhas

SOURCE VERSION:

ausente

SOURCE STATUS:

não declarado

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

08_python_engineering_core

PRIORITY:

50

PROMPT CODE:

ausente

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

FIRST-PROMPTS STARTUP COPY:

ausente, corretamente on request

DIRECT REFERENCE SURFACES:

aproximadamente 22 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 50

GENERATED MANIFEST CANONICAL PATH:

em branco

ACTIVE DUPLICATE SOURCE:

não encontrado

FOCUSED WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

Manter o Prompt 080 como autoridade geral para refatoração Python pequena e média, orientada por comportamento, smells e transformações rastreáveis.

Sua responsabilidade é legítima e distinta.

O prompt atual, porém, transforma boas recomendações de Fowler em proibições absolutas, exige operações de VCS que a IA não possui autorização para realizar, permite alegações de preservação comportamental sem execução real e sobrepõe-se a:

    Legacy Code Workflow;

    Large Module Refactor Protocol;

    Python Clean Code;

    Python Clean Architecture;

    Pytest;

    Brick Wall;

    Patch Delivery.

Deve ser modernizado e reduzido.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

Prompt 080 deve possuir:

    distinção entre refatoração e mudança comportamental;

    identificação de smells;

    seleção de refatorações nomeadas;

    planejamento de transformações pequenas e rastreáveis;

    preservação de contratos públicos;

    validação proporcional ao risco;

    stopping criteria;

    registro de dívida descoberta fora do escopo;

    despacho para Legacy Code ou Large Module Refactor quando necessário.

Não deve possuir:

    autorização para commits;

    política geral de testes;

    arquitetura de caixas completa;

    entrega de patch;

    freeze;

    protocolo de módulos grandes;

    autorização de escrita;

    afirmações de testes não executados.

Positive findings
P080-001 — Preservação de comportamento é tratada como conceito central

A distinção entre refatoração e alteração funcional é correta e deve permanecer.
P080-002 — Smells são usados como motivação concreta

O prompt evita refatoração apenas por moda ou preferência estética.
P080-003 — Refatorações pequenas e reversíveis são favorecidas

Isso melhora a capacidade de revisão e rollback.
P080-004 — O Two-Hat Rule é útil

Separar explicitamente FEATURE e REFACTOR reduz alterações comportamentais acidentais.
P080-005 — Há reconhecimento de código sem proteção

O prompt encaminha código sem testes para characterization tests.
P080-006 — Os stopping criteria são úteis

A regra de parar quando o problema que motivou a refatoração foi resolvido evita expansão infinita.
P080-007 — Dívida encontrada fora do escopo não deve ser corrigida silenciosamente

Esse princípio está alinhado com o controle de escopo.
P080-008 — Compatibilidade pública é mencionada

Mover ou renomear símbolos deve considerar call sites e ciclos de depreciação.
P080-009 — Refatoração de módulo grande pode ser distinguida de refatoração comum

Há base suficiente para uma fronteira clara com Prompt 056.
P080-010 — Não há uma segunda fonte canônica ativa

Prompt Library e source archive apresentam a mesma identidade.
Critical and high-severity findings
F080-001 — A fonte não possui identidade operacional completa

Faltam no corpo:

    prompt_id;

    versão semântica;

    status;

    load type;

    owner;

    histórico de versão;

    statement de não autorização.

F080-002 — A persona de “20+ years of experience” deve ser removida

A capacidade deve ser descrita como método de análise, não como experiência pessoal inventada.
F080-003 — “Commit after each successful step” é uma instrução não autorizada

A IA não deve criar commits no VCS do usuário sem pedido explícito.

O prompt deve usar:

    transformation unit;

    checkpoint;

    candidate diff;

    validation boundary.

Commit é uma ação separada e humana ou explicitamente autorizada.
F080-004 — “Never batch multiple refactorings into one change” é absoluto demais

Uma alteração coerente pode exigir várias transformações pequenas, como:

    Rename;

    Extract Function;

    Update Call Sites;

    Remove Compatibility Alias.

O requisito correto é preservar rastreabilidade e não misturar mudanças sem relação.
F080-005 — “Do not fix forward” é excessivamente rígido

Quando um pequeno passo introduz uma falha trivial e claramente localizada, corrigir o próprio passo antes do checkpoint pode ser mais seguro do que restaurar toda a alteração.

O prompt deve distinguir:

    correção do mesmo transformation unit;

    expansão de escopo;

    nova mudança comportamental.

F080-006 — A execução exige alegações de testes sem evidência

O fluxo manda escrever:

“Tests still pass.”

Isso é proibido quando os testes não foram realmente executados.

Os estados permitidos devem incluir:

    EXECUTED_PASS;

    EXECUTED_FAIL;

    NOT_EXECUTED;

    STATIC_REASONING_ONLY;

    BLOCKED_BY_MISSING_TEST_ENVIRONMENT.

F080-007 — “Assert behaviour is unchanged by reasoning” é incorreto

Raciocínio pode aumentar confiança, mas não prova equivalência comportamental.

O termo correto seria:

“Expected behavior preservation based on static reasoning; not execution-verified.”
F080-008 — “Comprehensive tests” não é um gate operacional definido

A palavra comprehensive não possui critério mensurável.

A proteção deve depender de:

    contrato alterado;

    risco;

    caminhos de falha;

    consumidores;

    side effects;

    regressões relevantes.

F080-009 — A exceção de código trivial com “one line” é arbitrária

Uma linha pode:

    deletar dados;

    alterar autorização;

    modificar estado global;

    executar um comando;

    mudar persistência.

Trivialidade deve ser avaliada por impacto, não por quantidade de linhas.
F080-010 — O exemplo de Replace Conditional with Polymorphism é simplista

O exemplo omite:

    construção dos subtipos;

    contrato abstrato;

    tipos desconhecidos;

    comportamento padrão;

    migração de consumidores;

    possibilidade de mapping ou Strategy ser mais simples.

Polimorfismo não deve ser o destino automático de qualquer condicional.
F080-011 — Introduce Parameter Object após três parâmetros é uma regra arbitrária

Quatro parâmetros independentes podem ser claros.

Dois parâmetros fortemente relacionados podem justificar um objeto.

O critério deve ser coesão conceitual e evolução conjunta.
F080-012 — Move Function seguido de “Delete original” pode quebrar API pública

Quando o símbolo é consumido externamente, pode ser necessário:

    re-export;

    forwarding facade;

    deprecated alias;

    staged migration.

F080-013 — Type hint obrigatório após rename não possui relação causal

Renomear um símbolo e adicionar tipagem são alterações distintas.

Podem ser feitas juntas quando justificadas, mas não devem ser acopladas por regra.
F080-014 — “Comments as crutches” é generalizado demais

Comentários podem documentar:

    invariantes;

    decisões arquiteturais;

    workarounds externos;

    segurança;

    comportamento não óbvio;

    origem regulatória.

O problema é comentário que substitui nome ou estrutura clara, não todo comentário explicativo.
F080-015 — “One session, one smell, one fix” não serve para todos os casos

Um smell pode exigir múltiplas transformações.

Vários smells podem ter uma única causa.

A regra correta é uma mudança coerente e limitada por escopo.
F080-016 — O output obrigatório é muito interativo

Mostrar cada passo com before/after e aguardar implicitamente torna a execução longa e fragmentada.

O usuário pode preferir:

    plano completo;

    patch completo;

    diff;

    apenas a versão final;

    relatório resumido.

F080-017 — Não há modos operacionais

O prompt deveria distinguir:

    EXPLANATION;

    SMELL_AUDIT;

    REFACTOR_PLAN;

    SOURCE_GROUNDED_REVIEW;

    IMPLEMENTATION_CANDIDATE;

    AUTHORIZED_IMPLEMENTATION.

F080-018 — Source identity e freshness não são exigidos

Antes de alterar código real, faltam:

    caminho exato;

    SHA-256;

    consumidores;

    API pública;

    estado de testes;

    frozen behavior;

    invalidation conditions.

F080-019 — Error Memory não aparece no preflight

Refatorações frequentemente repetem falhas envolvendo:

    import context;

    public API;

    estado oculto;

    contratos dinâmicos;

    validação frágil.

F080-020 — Box Logic é carregada incondicionalmente

Uma explicação sobre Extract Function não exige Box Boundary Audit.

Box Architecture deve ser condicionada a trabalho source-grounded ou com risco de boundary.
F080-021 — Os companion prompts são excessivos

Todo pedido de refatoração atualmente carrega:

    Box Architecture;

    Roadmap Builder;

    Pytest;

    Implementation and Delivery.

Isso é desnecessário para leitura, explicação ou análise pequena.
F080-022 — Routing triggers podem competir com Prompt 056 e Prompt 078

“safe refactoring” e “refactor python” não distinguem:

    refatoração comum;

    módulo grande;

    legacy sem testes;

    reparo AST;

    arquitetura ampla.

F080-023 — A integração com Clean Code e Clean Architecture é bidirecionalmente ambígua

Prompt 080 diz aplicar todos os três, mas não define qual prompt prevalece em caso de conflito.
F080-024 — A regra de funções pequenas pode gerar microfragmentação

Extract Function deve criar uma responsabilidade real, não apenas diminuir quantidade de linhas.
F080-025 — O validador semântico atual é ausente

Não há prova automatizada de que o prompt:

    não autorize commits;

    não invente teste executado;

    preserve API;

    despache legacy e large-module corretamente;

    não aplique regras numéricas arbitrárias;

    use source freshness.

Current owner model

Prompt 080 deve possuir:

    refatoração Python geral;

    smell-to-transformation mapping;

    transformação rastreável;

    stopping criteria;

    preservação comportamental esperada.

Prompt 078 deve possuir:

    estabilização de legacy;

    characterization;

    seams;

    ausência de testes confiáveis.

Prompt 056 deve possuir:

    decomposição de módulos grandes;

    source family;

    public facade;

    arquitetura de split.

Pytest deve possuir:

    estratégia detalhada de testes.

Brick Wall deve possuir:

    autorização de implementação.

Class 05 deve possuir:

    entrega e validação de release.

Recommended final structure

    Identity and version

    Purpose

    When to load

    Operational mode

    Exact source and consumer evidence

    Refactor versus feature classification

    Smell assessment

    Candidate transformation units

    Public-contract preservation

    Legacy and large-module dispatch

    Validation evidence states

    Rollback and checkpoints

    Stopping criteria

    Out-of-scope debt record

    Non-authorization statement

    Version history

Final disposition

CLASSIFICATION:

General behavior-preserving Python refactoring specialist

ACTION:

KEEP, MODERNIZE, REMOVE VCS AUTHORITY, REMOVE UNVERIFIED TEST CLAIMS, AND DEFINE CLEAR BOUNDARIES WITH LEGACY AND LARGE-MODULE WORK

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_unverified_test_claims_vcs_authority_absolute_mechanics_and_refactor_owner_overlap

EXPECTED FINAL STATUS:

active

FINAL LOAD TYPE:

on_request for bounded Python refactoring or smell analysis

PROMPT CODE:

assign only after Class 08 identity reconciliation

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 080 was fully audited and formally closed.

No prompt source, metadata, source code, tests, VCS state, routing, validator, Error Memory, Project state, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 081
Identity

AUDIT_ID:

A081-20260715-REVIEW

PROMPT:

software_engineering_books_master.md

METADATA CANONICAL ID:

software_engineering_books_master

SOURCE-DECLARED PROMPT ID:

A027

SOURCE TITLE:

Master Reasoner Engineering Prompt v1.1 Candidate

DISPLAY NAME:

Software Engineering Books Master

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/08_python_engineering_core/software_engineering_books_master.md

SOURCE SHA-256:

2dc812d308a47194b204b5018b758f244af3ee46e63518bf72084f79a923ded5

METADATA SHA-256:

290d939f957ead53b4cd66a5eb57d47c5676b2b517baebcb230578c25335875b

SOURCE SIZE:

20.072 bytes

SOURCE LENGTH:

449 linhas

SOURCE VERSION:

1.1-candidate

SOURCE STATUS:

candidate_not_active_without_human_approval

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

08_python_engineering_core

PRIORITY:

50

PROMPT CODE:

ausente

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

FIRST-PROMPTS STARTUP COPY:

ausente

DIRECT REFERENCE SURFACES:

aproximadamente 11 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 27

GENERATED MANIFEST CANONICAL PATH:

em branco

ACTIVE DUPLICATE SOURCE:

não encontrado

FOCUSED WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

O corpo atual do Prompt 081 não deve permanecer como master prompt operacional.

Ele se declara explicitamente:

    candidate;

    not active;

    dependent on human approval;

    not a replacement for current governance.

Entretanto, sua metadata o registra como active e on_request.

Além disso, ele contém uma cópia extensa e obsoleta de:

    startup routing;

    prompt load order;

    Folder Structure;

    Box Architecture;

    Universal Delivery;

    Large Module law;

    testing;

    freeze;

    docstrings;

    SRE;

    Peopleware;

    DDD;

    performance;

    legacy;

    refactoring;

    Clean Code;

    Clean Architecture.

A capacidade útil restante é apenas:

    sintetizar conceitos;

    comparar especialistas;

    apontar qual especialista deve ser carregado;

    explicar conflitos entre princípios de livros.

O corpo de “Master Reasoner Engineering Prompt” deve ser aposentado.

O ID software_engineering_books_master pode sobreviver apenas se for transformado em um mapa curto de síntese e roteamento, sem autoridade de implementação.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

parcial

Útil após redução:

    síntese comparativa entre livros;

    identificação do especialista apropriado;

    explicação de tensões entre princípios;

    visão geral para tarefas educacionais;

    dispatch para prompts específicos.

Não deve possuir:

    startup;

    implementação;

    Box audit;

    entrega;

    freeze;

    module-size law;

    testing policy;

    docstring policy;

    governance;

    root ownership;

    autorização.

Positive findings
P081-001 — A própria fonte admite que não deve substituir o stack atual

Isso fornece base explícita para a correção.
P081-002 — O prompt reconhece que várias disciplinas são distintas

Clean Code, DDD, Refactoring, SRE e Peopleware aparecem como fontes separadas.
P081-003 — Há intenção de evitar aplicação cega de patterns

A síntese reconhece pragmatismo e proporcionalidade.
P081-004 — Freeze permanece humano

Mesmo no corpo antigo, não há autorização explícita para auto-freeze.
P081-005 — Build output, secrets e evidência são distinguidos de source

O princípio de limpeza de árvore é útil, embora pertença a outro owner.
P081-006 — A fonte declara ser candidate

Isso reduz ambiguidade sobre a falta de autoridade pretendida originalmente.
P081-007 — A síntese pode ter valor educacional

Um mapa curto dos diferentes lenses de engenharia é justificável.
P081-008 — Nenhuma segunda fonte ativa foi encontrada

A inconsistência principal é interna, entre source e metadata.
Critical and high-severity findings
F081-001 — Canonical identity é inválida no source

prompt_id: A027 é identidade histórica de auditoria.

O ID operacional deve ser:

software_engineering_books_master
F081-002 — Nome, filename recomendado e nome atual discordam

A fonte contém:

    Software Engineering Books Master;

    Master Reasoner Engineering Prompt;

    000 25 MASTER REASONER ENGINEERING PROMPT v1.1 CANDIDATE.md;

    canonical filename atual diferente.

F081-003 — Lifecycle é diretamente contraditório

Source:

candidate_not_active_without_human_approval

Metadata:

active

Isso é um conflito material, não uma diferença editorial.
F081-004 — A metadata descreve consolidação, mas não registra candidate status

Um prompt explicitamente não ativo não deve aparecer como active sem uma etapa de reconciliação.
F081-005 — Startup load order está obsoleto

A fonte exige arquivos antigos, incluindo:

    old stack load order;

    Universal Delivery Protocol;

    Reasoner Startup Canon;

    Daily Loader;

    cinco arquivos de governance fixos;

    handoff com nomes antigos.

O startup atual é gerado e usa o pacote de três arquivos e os numbered startup files atuais.
F081-006 — Há dependência explícita de nomes PyArchitect antigos

A fonte preserva:

    PyArchitect;

    old Reasoner prompt stack;

    nomes com numeração histórica;

    source maps já substituídos.

F081-007 — O prompt copia e contradiz o delivery atual

A seção diz:

    one ZIP;

    no install script;

    extract directly to project root;

    no temporary staging.

Isso conflita com o contrato atual de:

    drive-root staging;

    project-linked daily-work;

    installer;

    validation;

    receiver contract;

    Pre-Output.

F081-008 — O prompt copia um Box Boundary Audit completo

Box Architecture deve ser o único owner desse contrato.
F081-009 — A fonte exige pelo menos 12 patches

Esse número é histórico e arbitrário.

Um projeto pode necessitar de:

    nenhum patch;

    um patch;

    várias unidades independentes.

F081-010 — A fonte exige aprovação humana antes de criar qualquer arquivo

A necessidade de aprovação depende do modo e da autorização já concedida.

Não deve haver um segundo sistema de aprovação concorrente com Brick Wall.
F081-011 — “All source books are loaded into your context” é falso

O conteúdo integral dos livros não está presente.

O prompt apresenta familiaridade ou disponibilidade que não foi provada.
F081-012 — A persona de 25+ anos deve ser removida

Ela não adiciona precisão e simula experiência pessoal.
F081-013 — “Never write code without a test” é absoluto demais

Há tarefas legítimas como:

    documentação;

    metadata;

    correção de typo;

    generated source;

    build file;

    test-enabling seam;

    diagnóstico read-only.

F081-014 — “One assertion per test” não é regra universal

Um teste pode verificar um único conceito lógico com várias assertions relacionadas.
F081-015 — Mutation score ≥80% é um threshold arbitrário

Mutation testing pode ser caro, incompatível ou desnecessário para muitos módulos.
F081-016 — “Never mock what you own” é dogmático

Mocks ou spies internos podem ser apropriados para:

    failure injection;

    timing;

    callbacks;

    rare transitions;

    isolation temporária.

F081-017 — A Identity Map com weakref repete orientação tecnicamente insegura

Esse problema já foi identificado no Prompt 076.
F081-018 — O prompt repete regras de performance não verificadas

Inclui:

    __slots__;

    NumPy/Numba;

    multiprocessing;

    asyncio;

    memoryview;

sem perfil de workload ou benchmark.
F081-019 — O prompt repete a definição estreita de legacy code

Código com testes inadequados também pode ser legacy-risk.
F081-020 — “Fix broken windows immediately” promove scope creep

Problemas fora do escopo devem ser registrados e roteados, não automaticamente corrigidos.
F081-021 — SRE é aplicado universalmente

Nem todo script, GUI desktop ou ferramenta local necessita:

    SLO;

    Prometheus;

    OpenTelemetry;

    canary;

    chaos engineering.

F081-022 — “Start with chaos monkey” é inadequado como conselho geral

Chaos engineering requer:

    sistema resiliente;

    blast-radius control;

    observability;

    rollback;

    ambiente seguro;

    objetivo experimental.

F081-023 — Peopleware é tratado como regra operacional absoluta

Afirmações como equipes pequenas, estáveis ou collocated podem ser úteis, mas dependem de contexto.
F081-024 — A regra de docstrings é excessiva

Exigir docstring para:

    todo método privado;

    __init__;

    toda property;

    toda função trivial;

pode gerar documentação redundante e piorar a legibilidade.
F081-025 — A fonte duplica integralmente os Prompts 070–080

O master contém resumos prescritivos de todos os especialistas recém-auditados.
F081-026 — A fonte duplica Prompts de outras classes

Também invade:

    startup;

    routing;

    folder structure;

    Box;

    delivery;

    validation;

    freeze;

    governance.

F081-027 — A abertura obrigatória é ruído

O prompt exige uma longa declaração de identidade e stack a cada ativação.
F081-028 — O folder contract não suporta um master operacional

Class 08 deve ser selecionada para Python code reasoning, não para substituir todas as classes.
F081-029 — Os companion prompts são desnecessários

Um prompt de síntese educacional não precisa sempre carregar:

    Roadmap Builder;

    Pytest;

    Delivery;

    Box Architecture.

F081-030 — A fonte registra GPT-5.5 como updater operacional

Esse dado pertence a histórico de revisão, não ao comportamento ativo.
F081-031 — Não existe current whole-prompt validator

Nenhum validador prova:

    candidate versus active;

    remoção do startup antigo;

    ausência de delivery obsoleto;

    ausência de master authority;

    roteamento correto;

    delegação aos especialistas.

Current owner model

O eventual Prompt 081 reduzido deve possuir apenas:

    tabela de livros e áreas;

    comparação de princípios;

    resolução explicativa de tensões;

    seleção do especialista;

    visão geral educacional;

    síntese não autoritativa.

Prompt Navigation deve possuir:

    roteamento real.

Cada specialist prompt deve possuir:

    seu domínio técnico.

Brick Wall deve possuir:

    implementação.

Startup deve possuir:

    load order.

Class 05 deve possuir:

    entrega.

Freeze owners devem possuir:

    freeze.

Recommended final structure

    Identity and lifecycle

    Purpose

    Explicit non-master status

    When to use

    When not to use

    Book-to-specialist map

    Principle conflict table

    Applicability and trade-off guidance

    Specialist dispatch

    Current project evidence precedence

    Non-authorization statement

    Historical candidate note

    Version history

Final disposition

CLASSIFICATION:

Historical master-prompt candidate with a potentially useful synthesis and routing map

ACTION:

DEPRECATE THE CURRENT MASTER BODY; RETAIN THE ID ONLY IF IT IS REWRITTEN AS A THIN NON-AUTHORITATIVE SYNTHESIS AND SPECIALIST-DISPATCH PROMPT

DELETE IMMEDIATELY:

no

INTERMEDIATE STATUS:

deprecated_candidate

EXPECTED FINAL STATUS:

active thin synthesis map or historical reference

CURRENT IMPLEMENTATION AUTHORITY:

none

PROMPT CODE:

defer until the survival of the reduced identity is confirmed

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 081 was fully audited and formally closed.

No prompt source, metadata, startup file, routing file, specialist prompt, application code, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 082
Identity

AUDIT_ID:

A082-20260715-REVIEW

PROMPT:

anti_hallucination_book_literature_audit_full.md

PROMPT CODE:

KPR-09-005

CANONICAL ID:

anti_hallucination_book_literature_audit_full

DISPLAY NAME:

Anti-Hallucination Book Literature Audit Full

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_book_literature_audit_full.md

SOURCE SHA-256:

5528fdffe6d49a35fd081627630b73adae9d709eede09ae58383ba45c6ac80a8

METADATA SHA-256:

12b4cf9ee552676983afe029a398917705471ba97983db0b74e431d1f10c2e4c

SOURCE SIZE:

6.860 bytes

SOURCE LENGTH:

226 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

SOURCE STAGE:

anti-hallucination-prompt-groups-show-project-copy-buttons-v1

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

ACTIVE DUPLICATE SOURCE:

não encontrado

DIRECT REFERENCE SURFACES:

5 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 12

FEATURE-SPECIFIC VALIDATOR:

presente

VALIDATOR PATH:

tools/validate_anti_hallucination_prompt_groups_show_project_buttons_v1.py

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

Manter KPR-09-005 como especialista condicional de auditoria arquitetural por livros e literatura publicada.

A capacidade é útil quando há incerteza real sobre:

    modularidade;

    ownership;

    arquitetura;

    evolução;

    testabilidade;

    failure containment.

O prompt acerta ao dizer que livros não verificam:

    API atual;

    versões;

    flags;

    comportamento runtime.

Porém, o prompt ainda pode gerar hallucination de literatura, força um relatório e roadmap excessivos e invade delivery, install, Error Memory e freeze.

Deve ser reduzido a um owner de evidência literária verificável e aplicabilidade arquitetural.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

KPR-09-005 deve possuir:

    decisão sobre necessidade de literatura;

    seleção de fontes relevantes;

    registro bibliográfico verificável;

    extração limitada de princípios;

    avaliação de aplicabilidade;

    classificação ADOPT/ADAPT/REJECT;

    conflitos entre literatura e source truth;

    contribuição literária para uma síntese já existente.

Não deve possuir:

    implementação roadmap completo;

    delivery;

    instalação;

    freeze;

    module-size law;

    Error Memory workflow;

    final authorization.

Positive findings
P082-001 — A auditoria pode ser recusada

O prompt permite concluir que livros não são úteis para a tarefa.
P082-002 — Literatura não é usada para API e versão atuais

Essa fronteira é correta.
P082-003 — Fama não é suficiente para seleção

A fonte deve ser relevante para o problema.
P082-004 — Princípios precisam produzir ganho concreto

O prompt rejeita pesquisa decorativa.
P082-005 — Há classificação explícita das ideias

ADOPT, ADAPT, REJECT, NOT_APPLICABLE, ALREADY_SATISFIED e UNVERIFIED_APPLICATION são úteis.
P082-006 — Project source truth permanece superior

Livros não substituem o comportamento atual do projeto.
P082-007 — Conflitos entre fontes devem ser mostrados

Isso evita consenso artificial.
P082-008 — Module boundaries não são definidos apenas por linha

O texto prioriza ownership, cohesion e information hiding.
P082-009 — A literatura é colocada depois de evidência mais direta

Essa hierarquia é adequada.
P082-010 — Há implementação e integração real da família

O prompt possui code, metadata, folder registration, clipboard wrapper e validador focado.
Critical and high-severity findings
F082-001 — A fonte não possui versão semântica

O code KPR existe, mas o contrato de conteúdo não tem versão.
F082-002 — O termo “anti-hallucination” promete mais do que pode garantir

Literatura reduz determinadas incertezas, mas não elimina hallucination.

Um nome conceitual mais preciso seria:

    literature evidence audit;

    published-source architecture audit.

O code histórico pode permanecer.
F082-003 — O prompt assume que três estágios anteriores já ocorreram

Ele declara que já existem:

    plano;

    auditoria independente;

    web audit;

    Claim Ledger.

Uso isolado ou incompleto não possui comportamento definido.
F082-004 — “Final literature audit” cria falsa sensação de maturidade

Uma auditoria de livros não torna uma lógica automaticamente madura.
F082-005 — Até dez livros pode ser excessivo

A quantidade deve depender da decisão que precisa ser resolvida.

Uma única fonte primária ou um único livro diretamente aplicável pode ser suficiente.
F082-006 — O prompt não exige prova de que o conteúdo do livro foi realmente acessado

A IA pode conhecer apenas:

    título;

    descrição editorial;

    resenhas;

    memória parcial.

Isso não autoriza atribuir um princípio específico ao livro.
F082-007 — Falta uma classe de evidência bibliográfica

Cada princípio deveria indicar:

    FULL_TEXT_INSPECTED;

    CHAPTER_OR_EXCERPT_INSPECTED;

    OFFICIAL_PUBLISHER_DESCRIPTION;

    AUTHOR_SUMMARY;

    RELIABLE_SECONDARY_SUMMARY;

    MEMORY_ONLY_NOT_ACCEPTABLE.

F082-008 — Não há referência a capítulo, página ou localização verificável

Quando possível e permitido, a atribuição precisa de provenance.

Não é necessário fornecer longas citações, mas a origem deve ser rastreável.
F082-009 — Livros e “published literature” são misturados

Há diferenças de autoridade entre:

    livros;

    standards;

    research papers;

    conference papers;

    industry reports;

    publisher descriptions.

F082-010 — Data e edition relevance são insuficientes

Princípios estáveis podem vir de edições antigas.

Informações de tecnologia, plataforma ou ferramentas podem envelhecer.
F082-011 — “Recognized authors” e “professional recurrence” não provam aplicabilidade

Popularidade não substitui evidência técnica.
F082-012 — Reader reputation é uma base fraca

Avaliação de leitores pode ajudar descoberta, mas não deve entrar como evidência de correção.
F082-013 — Senior judgment continua como uma fonte não estruturada

Julgamento deve ser identificado como inferência e não colocado como equivalente a evidência publicada.
F082-014 — A seção Architecture Fitness Check invade owners existentes

Ela repete:

    module boundaries;

    dependency direction;

    evidence stages;

    human approval;

    validation sequencing.

Esses contratos já possuem owners.
F082-015 — O roadmap “How Deliver Project to AI Use” é scope sprawl

Uma auditoria de literatura deveria produzir:

    findings;

    aplicabilidade;

    alterações propostas;

    evidência restante.

Não deve obrigatoriamente definir 26 fases de entrega e freeze.
F082-016 — Delivery, install e freeze estão fora de escopo

Itens 21–26 pertencem às Classes 03 e 05.
F082-017 — Module-size law é duplicada

O prompt deve consumir a regra ativa do projeto, não manter outra cópia.
F082-018 — O formato obrigatório pode forçar pesquisa desnecessária

Se a decisão for:

BOOK_AUDIT_NOT_WARRANTED

o retorno deve ser curto.
F082-019 — Metadata routing intents são genéricos e iguais aos outros nove prompts

Todos respondem a:

    anti hallucination;

    avoid hallucination;

    evidence first coding;

    verify AI code claims.

Isso não seleciona o literature specialist diretamente.
F082-020 — Não há route condition específica para book audit

Deveria usar sinais como:

    architecture literature;

    book audit;

    published principles;

    compare architecture books;

    literature-level design review.

F082-021 — O validador atual não prova correção semântica

O validador verifica:

    arquivo;

    code;

    metadata;

    folder reference;

    UI;

    wrapper;

    ordem;

    line count.

Ele não verifica:

    provenance literária;

    não fabricação de conteúdo;

    conditional use;

    não ownership de delivery/freeze;

    source hierarchy.

F082-022 — O prompt não define comportamento quando web não está disponível

Seleção e verificação bibliográfica podem depender de pesquisa externa atual.
F082-023 — A saída não registra limitações de copyright

O prompt deve resumir e atribuir princípios, não reproduzir extensamente livros protegidos.
F082-024 — Não há non-authorization statement explícito

Aceitar uma ideia de livro não autoriza alteração do projeto.
Current owner model

KPR-09-005 deve possuir:

    auditoria de literatura;

    provenance;

    aplicabilidade;

    contribuição para Claim Ledger.

Web Evidence Audit deve possuir:

    documentação atual;

    APIs;

    versões;

    disconfirmation externa.

Independent Audit deve possuir:

    adversarial plan review.

Master Protocol deve possuir:

    síntese final e estado de evidência.

Class 05 deve possuir:

    delivery.

Freeze owners devem possuir:

    freeze.

Recommended final structure

    Identity and version

    Purpose

    Admission decision

    Evidence availability

    Literature source classes

    Bibliographic provenance

    Principle extraction rules

    Applicability test

    Decision table

    Conflict handling

    Accepted plan deltas

    Unverified literature claims

    Synthesis handoff

    Non-authorization statement

    Version history

Final disposition

CLASSIFICATION:

Conditional published-literature architecture evidence specialist

ACTION:

KEEP KPR-09-005, NARROW TO VERIFIED LITERATURE EVIDENCE, REMOVE DELIVERY/FREEZE ROADMAP OWNERSHIP, AND ADD BIBLIOGRAPHIC PROVENANCE

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_literature_provenance_gap_forced_roadmap_scope_sprawl_and_generic_routing

EXPECTED FINAL STATUS:

active

FINAL LOAD TYPE:

on_request only when genuine literature-level architecture uncertainty exists

PROMPT CODE:

retain KPR-09-005

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 082 was fully audited and formally closed.

No prompt source, metadata, book source, web result, routing, UI, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 083
Identity

AUDIT_ID:

A083-20260715-REVIEW

PROMPT:

anti_hallucination_book_literature_audit_short.md

PROMPT CODE:

KPR-09-009

CANONICAL ID:

anti_hallucination_book_literature_audit_short

DISPLAY NAME:

Anti-Hallucination Book Literature Audit Short

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_book_literature_audit_short.md

SOURCE SHA-256:

473ace4b0f856128b5ca6e318fdce78d0f47d680dd6593bdef151dc2a738d87e

METADATA SHA-256:

ccada14786a9ec1b3644ad9a515fd3f10cbebd3df31ab1b121a48fd4d9508c3c

SOURCE SIZE:

1.957 bytes

SOURCE LENGTH:

35 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

4 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 11

FEATURE-SPECIFIC VALIDATOR:

presente

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter KPR-09-009 apenas como perfil compacto derivado do Prompt 082.

Ele é curto e funcional, mas hoje é uma segunda fonte canônica escrita manualmente.

Isso cria risco de drift entre full e short.

O conteúdo compacto não deve evoluir independentemente do contrato full.
Unique capability assessment

UNIQUE CANONICAL CAPABILITY:

não

UNIQUE DELIVERY PROFILE:

sim

A capacidade é:

    fornecer versão compacta para uso de baixa complexidade;

    manter os mesmos estados essenciais;

    reduzir custo de contexto.

Positive findings
P083-001 — O texto é curto e operacional

Não contém o mega-canon encontrado em outros prompts.
P083-002 — Preserva a decisão de não usar livros quando desnecessário
P083-003 — Mantém a fronteira entre literatura e API atual
P083-004 — Mantém ADOPT/ADAPT/REJECT e estados de incerteza
P083-005 — Preserva prioridade do project source
P083-006 — O wrapper curto possui ordem determinística implementada
Critical and high-severity findings
F083-001 — O short prompt é uma cópia paralela manual

Não há:

    full_prompt_version;

    derived_from_hash;

    schema version;

    generation mechanism;

    compatibility record.

F083-002 — O prompt repete os principais problemas do full

Inclui:

    até dez livros;

    roadmap obrigatório;

    module-size law;

    delivery-oriented title.

F083-003 — Não há comportamento explícito de escalonamento

O próprio prompt não define quando parar e carregar o full.
F083-004 — Não há provenance bibliográfica
F083-005 — Não há proteção contra atribuir conteúdo não inspecionado a um livro
F083-006 — A metadata usa routing intents genéricos
F083-007 — A versão curta pode omitir uma regra nova do full

Sem geração ou validator semântico, futuras correções podem ficar apenas em um dos dois.
F083-008 — O validador prova apenas presença e ordem
F083-009 — Não há non-authorization statement
F083-010 — A module-size law não pertence ao perfil compacto
Current owner model

Prompt 082:

    contrato semântico completo.

Prompt 083:

    compact profile derivado.

Short Group:

    decisão de usar o perfil curto.

Recommended final structure

    Compact profile identity

    Derived-from full prompt ID and minimum version

    Admission rule

    Verified literature provenance rule

    Compact decision table

    Escalation conditions

    Synthesis handoff

    Non-authorization statement

Final disposition

CLASSIFICATION:

Derived compact profile of the full literature audit

ACTION:

KEEP KPR-09-009 AS A DERIVED OR GENERATED SHORT PROFILE; DO NOT TREAT IT AS AN INDEPENDENT CANONICAL OWNER

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_manual_full_short_duplication_no_version_binding_and_shared_scope_sprawl

EXPECTED FINAL STATUS:

active derived profile

PROMPT CODE:

retain KPR-09-009

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 083 was fully audited and formally closed.

No source, metadata, compact generator, wrapper, routing, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 084
Identity

AUDIT_ID:

A084-20260715-REVIEW

PROMPT:

anti_hallucination_full_group.md

PROMPT CODE:

KPR-09-001

CANONICAL ID:

anti_hallucination_full_group

DISPLAY NAME:

Anti-Hallucination Full Group

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_full_group.md

SOURCE SHA-256:

4ef1dd8b7d44dcd73216c9931de53bf4b9e946a1370ed6d80ffb603252850920

METADATA SHA-256:

de68b2a1ee0d1f28be742b11c03ccbfa8a71e122f6c3dffe103139cae864ef0d

SOURCE SIZE:

1.159 bytes

SOURCE LENGTH:

24 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

routed

CATEGORY:

09_python_quality_security_observability

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

6 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 14

FOCUSED FEATURE VALIDATOR:

presente

WHOLE-GROUP SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter KPR-09-001 como roteador e orquestrador fino da família full.

A necessidade de um único entrypoint para trabalho de alto risco é legítima.

O grupo, porém, precisa de:

    admission criteria mais precisos;

    contratos de handoff entre estágios;

    stop conditions;

    definição de independência;

    redução de duplicação com Master Protocol Full.

O grupo deve coordenar prompts, não repetir comportamento.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

KPR-09-001 deve possuir:

    seleção do train full;

    ordem dos estágios;

    condições de pular literature audit;

    handoff record;

    stop/escalation conditions;

    declaração de que os estágios são evidência, não autoridade.

Positive findings
P084-001 — O grupo é curto
P084-002 — A ordem é explícita
P084-003 — Literature audit é condicional
P084-004 — AI agreement não é tratado como prova
P084-005 — Generated plan não se torna source truth
P084-006 — O grupo não substitui validação determinística
P084-007 — A integração de UI usa arquivos canônicos
P084-008 — A ordem do wrapper é testada pelo validador focado
Critical and high-severity findings
F084-001 — O nome implica eliminação de hallucination

A função real é evidence-first verification e uncertainty control.
F084-002 — Os critérios de full group são muito amplos

A lista inclui quase todo trabalho não trivial:

    multi-file;

    architecture;

    dependency;

    concurrency;

    security;

    unfamiliar;

    difficult rollback.

Isso pode transformar o full group em companion quase obrigatório.
F084-003 — Não há threshold operacional de risco

Deveria existir um record como:

    impact if wrong;

    reversibility;

    uncertainty;

    evidence availability;

    public contract impact;

    security/concurrency impact.

F084-004 — Não há comportamento quando um estágio fica bloqueado

Exemplos:

    sem web;

    sem source;

    sem independent reviewer;

    literature não acessível;

    Claim Ledger incompleto.

F084-005 — Não há handoff schema entre os quatro prompts

Independent Audit, Web Audit, Literature Audit e Master Protocol usam estruturas parecidas, mas não existe uma identidade comum de operação.
F084-006 — Master Protocol Full repete os outros estágios

O grupo chama:

    Independent Full;

    Web Full;

    Book Full;

    Master Full.

O Master Full também contém adversarial review, web verification e book audit.

Isso cria dupla aplicação e contexto inflado.
F084-007 — A independência do Independent AI não é demonstrada

Se o mesmo modelo, mesmo contexto e mesma conversa executarem o estágio, trata-se de adversarial second pass, não auditor independente.
F084-008 — Não há operation ID ou plan hash

O grupo pode auditar uma versão de plano e sintetizar outra sem detectar mudança.
F084-009 — Source freshness não é parte do group record
F084-010 — O grupo não exige Error Memory aplicável
F084-011 — Não há stop condition após finding crítico

Um conflito de source identity ou ownership deveria interromper os estágios seguintes.
F084-012 — A metadata usa routing intents idênticos aos subprompts

Isso dificulta distinguir entrypoint de stage.
F084-013 — O router bridge pode carregar o grupo excessivamente

Ele recomenda full para praticamente qualquer tarefa arquitetural.
F084-014 — O validador é de integração, não de semântica

Ele prova:

    codes;

    files;

    routes;

    UI;

    order.

Não prova:

    critérios de seleção;

    handoff;

    bloqueio;

    não duplicação com Master;

    source freshness.

F084-015 — Não há versão do train

Os quatro estágios podem evoluir de forma incompatível.
Current owner model

KPR-09-001 deve possuir:

    group admission;

    stage order;

    handoff identity;

    stop/escalation state.

Os quatro subprompts devem possuir:

    seus respectivos estágios.

Master Protocol Full deve ser reduzido a:

    síntese;

    evidence state;

    final verification contract.

Recommended final structure

    Group identity and version

    Admission record

    Full versus short decision

    Required operation identity

    Required input state

    Stage order

    Stage handoff schema

    Optional literature rule

    Stop and block conditions

    Final synthesis handoff

    Non-authorization statement

    Compatibility matrix

Final disposition

CLASSIFICATION:

Full evidence-verification train router and orchestrator

ACTION:

KEEP KPR-09-001, ADD RISK ADMISSION AND STAGE HANDOFF CONTRACTS, AND REMOVE DUPLICATION WITH MASTER PROTOCOL FULL

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_overbroad_admission_no_handoff_identity_and_master_stage_duplication

EXPECTED FINAL STATUS:

active routed group

PROMPT CODE:

retain KPR-09-001

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 084 was fully audited and formally closed.

No source, metadata, group wrapper, router bridge, UI, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 085
Identity

AUDIT_ID:

A085-20260715-REVIEW

PROMPT:

anti_hallucination_independent_ai_audit_full.md

PROMPT CODE:

KPR-09-003

CANONICAL ID:

anti_hallucination_independent_ai_audit_full

DISPLAY NAME:

Anti-Hallucination Independent AI Audit Full

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_independent_ai_audit_full.md

SOURCE SHA-256:

882347b78f65f2c04774ced8055866e5083f79aeb74cd88afc1ff6518ee89ae9

METADATA SHA-256:

a2e402d4e7ed288d5b14d883aaa4e3bbb13edfc5ff480531adb55b545a297b18

SOURCE SIZE:

6.174 bytes

SOURCE LENGTH:

187 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

5 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 12

FEATURE-SPECIFIC VALIDATOR:

presente

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter KPR-09-003 como especialista de revisão adversarial pré-implementação.

A capacidade é forte e distinta:

    desafiar o primeiro plano;

    separar fatos de inferências;

    procurar failure modes;

    propor alternativa;

    registrar claims;

    reduzir confiança não suportada.

O maior defeito é exigir pelo menos três weaknesses, o que cria incentivo para fabricar críticas.

Também é inadequado chamar o estágio de independent quando ele pode ser executado pelo mesmo modelo e contexto.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

KPR-09-003 deve possuir:

    adversarial second-pass review;

    Assumption Register;

    structural review;

    failure-mode analysis;

    counter-design quando justificável;

    Claim Ledger;

    self-hallucination check;

    evidence-needed record.

Não deve possuir:

    module-size law;

    web research;

    literature;

    implementation;

    delivery;

    authorization.

Positive findings
P085-001 — O plano é tratado como hipótese
P085-002 — Project facts não devem ser inventados
P085-003 — Fatos, constraints, inference e assumptions são separados
P085-004 — Agreement entre AIs não é evidência
P085-005 — Nova abstração precisa resolver problema concreto
P085-006 — Failure modes são amplos

Incluem:

    cancellation;

    retries;

    stale evidence;

    persistence;

    ownership;

    generated artifacts.

P085-007 — Alternative design não é automaticamente preferido
P085-008 — Claim Ledger registra ganho, risco, evidência e incerteza
P085-009 — O prompt proíbe revelar private chain-of-thought
P085-010 — Há self-audit contra símbolos e APIs inventados
Critical and high-severity findings
F085-001 — “Assume at least three weaknesses” cria viés de fabricação

Uma análise honesta pode encontrar:

    zero problemas materiais;

    um problema;

    dois problemas;

    várias incertezas sem defeito demonstrado.

O prompt deve exigir busca adversarial, não quantidade mínima de críticas.
F085-002 — “Independent AI” pode ser uma descrição falsa

Independência exige ao menos um dos seguintes:

    outro modelo;

    contexto separado;

    blind review;

    reviewer identity distinta;

    input control.

Caso contrário, deve ser chamado:

adversarial review pass
F085-003 — A persona de senior engineer com deep experience deve ser removida
F085-004 — O prompt presume que a auditoria ocorre antes de qualquer código

Também pode ser útil para:

    revisar implementação existente;

    revisar patch;

    revisar código gerado;

    post-implementation audit.

F085-005 — Os dez inputs obrigatórios podem não existir

O prompt precisa definir comportamento para input parcial.
F085-006 — PROJECT_CONSTRAINT é misturado com evidence status

Ser constraint não significa estar verificado.

Deve haver campos separados:

    claim type;

    evidence status;

    authority.

F085-007 — REASONABLE_INFERENCE não informa confiança ou consequência
F085-008 — Claim Ledger é exigido para toda recomendação

Isso pode gerar relatório enorme e reduzir foco.

Deveria ser obrigatório apenas para claims materiais.
F085-009 — Counter-design pode ser artificial

Mesmo com a condição “when credible”, o output obrigatório sempre exige COUNTER-DESIGN.

Deve haver:

NO_CREDIBLE_ALTERNATIVE_IDENTIFIED
F085-010 — File-size constraint é duplicada
F085-011 — Não há current source identity record

Faltam:

    project identity;

    plan hash;

    target source hashes;

    operation ID;

    reviewed-at;

    invalidation conditions.

F085-012 — A review pode ficar stale se o plano mudar

Não há mecanismo de invalidation.
F085-013 — Não há relação explícita com Error Memory
F085-014 — Não há severidade por finding

Um typo e um risco de data loss podem aparecer no mesmo nível.
F085-015 — Não há disposition para ALREADY_SATISFIED

Um item pode ter sido considerado e corretamente resolvido pelo plano.
F085-016 — “Unsupported assumption” e “missing evidence” podem ser tratados como defeito arquitetural

O relatório deve distinguir:

    design defect;

    evidence gap;

    implementation risk;

    unresolved decision;

    non-applicable concern.

F085-017 — Security review é ampla mas sem perfil de ameaça
F085-018 — Windows compatibility é sempre exigida

Isso é apropriado para KANDA, mas o prompt se apresenta como especialista genérico.

Deve consumir platform profile.
F085-019 — O formato exatamente fixo pode ser excessivo

Um plano pequeno pode não exigir onze seções completas.
F085-020 — Routing intents são genéricos

O prompt deveria ter sinais diretos como:

    adversarial plan audit;

    independent architecture review;

    challenge implementation plan;

    second-opinion technical audit.

F085-021 — O validador não prova conteúdo semântico
F085-022 — Não há versão semântica
F085-023 — Não há statement de que findings não autorizam mudança
F085-024 — Há overlap com Brick Wall Q01 e Q03

Ambos procuram:

    real problem;

    duplication risk;

    alternatives;

    evidence;

    blockers.

A relação precisa ser explícita:

    Brick Wall governa;

    KPR-09-003 fornece evidence input.

Current owner model

KPR-09-003 deve possuir:

    adversarial technical review;

    evidence gaps;

    counter-design;

    failure modes;

    Claim Ledger input.

Brick Wall deve possuir:

    admission and implementation authority.

Web Audit deve possuir:

    external evidence.

Master Protocol deve possuir:

    final synthesis and evidence status.

Recommended final structure

    Identity and version

    Review independence classification

    Input completeness

    Operation and plan identity

    Fact/constraint/inference model

    Structural audit

    Failure modes

    Alternative search

    Material findings

    Claim Ledger

    Evidence gaps

    Invalidation conditions

    Governance handoff

    Non-authorization statement

Final disposition

CLASSIFICATION:

Adversarial implementation-plan and architecture review specialist

ACTION:

KEEP KPR-09-003, REMOVE THE THREE-WEAKNESS QUOTA, DISTINGUISH TRUE INDEPENDENCE FROM SELF-REVIEW, AND ADD PLAN IDENTITY/FRESHNESS

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_forced_criticism_quota_false_independence_risk_and_missing_plan_freshness

EXPECTED FINAL STATUS:

active

FINAL LOAD TYPE:

on_request for deep adversarial review of consequential plans or implementations

PROMPT CODE:

retain KPR-09-003

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 085 was fully audited and formally closed.

No source, metadata, implementation plan, routing, wrapper, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 086
Identity

AUDIT_ID:

A086-20260715-REVIEW

PROMPT:

anti_hallucination_independent_ai_audit_short.md

PROMPT CODE:

KPR-09-007

CANONICAL ID:

anti_hallucination_independent_ai_audit_short

DISPLAY NAME:

Anti-Hallucination Independent AI Audit Short

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_independent_ai_audit_short.md

SOURCE SHA-256:

f0c222d8b53ba8a6522e86f87d556e834f6b82a850e5cb6d327ac8f130a3d1b6

METADATA SHA-256:

111f3036e86efafcb608b7f57382fc08774d2e975a0da45e11f711967ef0a351

SOURCE SIZE:

1.677 bytes

SOURCE LENGTH:

31 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

4 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 11

FEATURE-SPECIFIC VALIDATOR:

presente

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter KPR-09-007 somente como perfil compacto derivado de KPR-09-003.

O conteúdo básico é útil, mas repete o principal defeito do full prompt:

“actively look for at least three meaningful weaknesses.”

A versão curta precisa ser vinculada semanticamente à versão full e possuir critérios próprios de escalonamento.
Unique capability assessment

UNIQUE CANONICAL CAPABILITY:

não

UNIQUE COMPACT PROFILE:

sim
Positive findings
P086-001 — A versão curta preserva não invenção
P086-002 — Mantém Assumption Register
P086-003 — Mantém failure-mode review
P086-004 — Mantém alternativa quando credible
P086-005 — Mantém Claim Ledger
P086-006 — Mantém evidence-needed state
P086-007 — O tamanho é proporcional a um compact companion
Critical and high-severity findings
F086-001 — Mantém a quota artificial de três problemas
F086-002 — Mantém a alegação de independência sem prova
F086-003 — É uma segunda fonte escrita manualmente

Não há:

    derived_from;

    minimum compatible full version;

    full source hash;

    generation rule.

F086-004 — Não define quando escalar para o full
F086-005 — Não possui operation ID ou plan hash
F086-006 — Não possui invalidation conditions
F086-007 — A regra de 500 linhas é duplicada
F086-008 — Não distingue design defect de evidence gap
F086-009 — Não permite explicitamente concluir que o plano está adequado
F086-010 — Metadata routing intents são genéricos
F086-011 — O validador atual não verifica compatibilidade full-short
F086-012 — Não há non-authorization statement
F086-013 — Não há versão semântica
F086-014 — Não há vínculo explícito com Short Group escalation rules
Current owner model

Prompt 085:

    contrato adversarial completo.

Prompt 086:

    compact profile derivado.

Short Group:

    admission e escalation.

Recommended final structure

    Compact profile identity

    Derived-from full contract

    Review independence classification

    Minimum input

    Material weakness search without quota

    Compact assumption and risk record

    Escalation triggers

    Evidence needed

    Non-authorization statement

Final disposition

CLASSIFICATION:

Derived compact adversarial-review profile

ACTION:

KEEP KPR-09-007 AS A DERIVED SHORT PROFILE, REMOVE THE FORCED FINDING COUNT, AND ADD ESCALATION AND VERSION BINDING

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_manual_full_short_duplication_forced_weakness_quota_and_no_escalation_contract

EXPECTED FINAL STATUS:

active derived profile

PROMPT CODE:

retain KPR-09-007

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 086 was fully audited and formally closed.

No source, metadata, compact profile, wrapper, routing, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
CONSOLIDATED CHECKPOINT — PROMPTS 080–086
Audited and closed
080 — python_refactoring.md

Disposition:

Manter como especialista geral de refatoração Python. Remover autoridade de VCS, alegações de testes não executados, regras absolutas e overlap com Legacy e Large Module.
081 — software_engineering_books_master.md

Disposition:

Deprecar o corpo master atual. Preservar o ID somente se for reescrito como um mapa curto, não autoritativo, de síntese e dispatch para especialistas.
082 — anti_hallucination_book_literature_audit_full.md

Disposition:

Manter KPR-09-005 como auditoria condicional de literatura verificável. Adicionar provenance bibliográfica e remover roadmap de delivery/freeze.
083 — anti_hallucination_book_literature_audit_short.md

Disposition:

Manter KPR-09-009 apenas como perfil curto derivado do full prompt.
084 — anti_hallucination_full_group.md

Disposition:

Manter KPR-09-001 como roteador fino do train full. Adicionar admission, handoff, operation identity e stop conditions.
085 — anti_hallucination_independent_ai_audit_full.md

Disposition:

Manter KPR-09-003 como revisão adversarial. Remover quota de três problemas e distinguir auditoria realmente independente de self-review adversarial.
086 — anti_hallucination_independent_ai_audit_short.md

Disposition:

Manter KPR-09-007 como perfil curto derivado. Remover quota de findings e adicionar escalation/version binding.
Newly confirmed cross-prompt conflicts
Prompt 080

Sobrepõe-se a:

    Python Legacy Code Workflow;

    Large Module Refactor Protocol;

    Python Clean Code;

    Python Clean Architecture;

    Pytest;

    Brick Wall;

    Class 05 delivery.

Prompt 081

Sobrepõe-se a:

    todos os Prompts 070–080;

    startup;

    routing;

    Box Architecture;

    Folder Structure;

    delivery;

    freeze;

    SRE;

    Peopleware;

    testing;

    documentation.

Prompt 082

Sobrepõe-se a:

    Web Evidence Audit;

    Software Engineering Books Master;

    Implementation Roadmap Builder;

    delivery;

    freeze.

Prompt 083

Duplica Prompt 082 de forma manual.
Prompt 084

Sobrepõe-se ao próprio Master Protocol Full, que já reproduz o train inteiro.
Prompt 085

Sobrepõe-se parcialmente a:

    Brick Wall verified-problem admission;

    architecture triage;

    Master Protocol Full.

Prompt 086

Duplica Prompt 085 e depende de Short Group para critérios que não aparecem em sua própria fonte.
Highest-priority reconciliation decisions

    Reescrever Prompt 080 como refactor specialist moderno e evidence-aware.

    Retirar imediatamente qualquer interpretação de Prompt 081 como master ativo.

    Decidir se Prompt 081 sobreviverá como synthesis router ou apenas historical reference.

    Criar uma relação explícita entre full e short prompts.

    Evitar manter full e short como duas fontes sem version binding.

    Reduzir Master Protocol Full para não repetir Independent, Web e Literature stages.

    Substituir “independent AI” por um modelo explícito:

        EXTERNAL_INDEPENDENT_REVIEW;

        SEPARATE_MODEL_REVIEW;

        BLIND_CONTEXT_REVIEW;

        SAME_MODEL_ADVERSARIAL_PASS.

    Remover quotas artificiais de weaknesses.

    Criar operation identity compartilhada entre os quatro estágios:

        project ID;

        task ID;

        plan hash;

        source snapshot;

        generation time;

        invalidation conditions.

    Criar stage handoff schema compartilhado.

    Adicionar provenance bibliográfica ao Literature Audit.

    Remover delivery, install, Error Memory e freeze dos literature prompts.

    Tornar routing intents específicos por stage.

    Manter o grupo full apenas para trabalho realmente alto risco.

    Criar validadores semânticos, não apenas asset/UI validators.

Current feature validator assessment

O arquivo:

tools/validate_anti_hallucination_prompt_groups_show_project_buttons_v1.py

existe e protege:

    presença dos dez prompt assets;

    prompt codes;

    metadata status;

    referências no folder card;

    referências no routing;

    labels e botões de UI;

    cores e bold;

    conexão dos botões;

    wrapper markers;

    cinco arquivos por grupo;

    ordem determinística;

    limite de 500 linhas dos dois módulos Python tocados;

    py_compile dos módulos de UI/helper.

Ele não foi executado durante esta auditoria.

Ele não protege:

    semântica dos prompts;

    compatibilidade full-short;

    version binding;

    admission rules;

    operation identity;

    stage handoff;

    forced weakness quota;

    literature provenance;

    não ownership de delivery/freeze;

    overlap entre Master Protocol e stages;

    source freshness.

Relevant Error Memory

O compact Error Memory foi suficiente.

O full Error Memory ZIP não foi aberto.

As lições mais relevantes para uma futura correção são:

    validator forward-contract rigidity;

    exact-phrase-count assumption;

    package import context.

Aplicação:

    o validador atual usa vários fragmentos literais;

    alguns são contratos legítimos de UI;

    não se deve expandir esse padrão para exigir prose exata nos prompts;

    futuras versões devem validar comportamento, identidade mínima e compatibilidade;

    o helper é carregado via spec_from_file_location; hoje não possui relative imports, mas uma futura alteração pode reproduzir a falha de package context.

A lição de validator rigidity reforça que validadores devem proteger contratos duráveis, não versões ou frases incidentais.
Audit integrity

    Cada prompt foi aberto como alvo primário somente após o encerramento formal do anterior.

    Related prompts foram usados apenas como comparação.

    Os Prompts 082–086 foram avaliados dentro da família, sem transformar 087–091 em alvos primários.

    Prompt Library ZIP foi usado como fonte canônica on-demand.

    Source archive foi usado para confirmar identidade byte a byte.

    Metadata, folder cards, routing, helper de clipboard e validador foram inspecionados.

    Nenhum source, metadata, routing, GUI, helper, validator, Project state, Error Memory ou freeze memory foi modificado.

    Nenhum validador foi executado.

    Nenhum validation pass foi reivindicado.

Context reliability

Context remains reliable for another adaptive cycle:

YES

O próximo conjunto permanece dentro da família anti-hallucination.

Um ciclo seguro seguinte seria 087–091:

    Anti-Hallucination Master Protocol Full

    Anti-Hallucination Protocol Short

    Anti-Hallucination Short Group

    Anti-Hallucination Web Evidence Audit Full

    Anti-Hallucination Web Evidence Audit Short

Exact next unopened prompt

087 — anti_hallucination_master_protocol_full.md

O ciclo 080–086 está formalmente encerrado.

087-95

Apliquei o protocolo de auditoria sequencial, mantendo relatório, fingerprints, disposição e encerramento separados para cada alvo. A ordem canônica confirma os Prompts 087–095 e estabelece python_testing_pytest.md como o próximo alvo.
ADAPTIVE CYCLE RESULT — PROMPTS 087–095

Os nove prompts foram auditados sequencialmente. Cada alvo primário foi formalmente encerrado antes da abertura do seguinte.

Total de fonte canônica auditada:

    Prompt 087: 820 linhas

    Prompt 088: 170 linhas

    Prompt 089: 23 linhas

    Prompt 090: 199 linhas

    Prompt 091: 37 linhas

    Prompt 092: 375 linhas

    Prompt 093: 236 linhas

    Prompt 094: 305 linhas

    Prompt 095: 262 linhas

    Total: 2.427 linhas

As fontes presentes no Prompt Library ZIP e no source archive são byte a byte idênticas para todos os nove prompts.

Nenhum arquivo foi modificado.

Nenhum validador foi executado.

Nenhum validation pass foi reivindicado.
PROMPT AUDIT REPORT 087
Identity

AUDIT_ID:

A087-20260715-REVIEW

PROMPT:

anti_hallucination_master_protocol_full.md

PROMPT CODE:

KPR-09-006

CANONICAL ID:

anti_hallucination_master_protocol_full

DISPLAY NAME:

Anti-Hallucination Master Protocol Full

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_master_protocol_full.md

SOURCE SHA-256:

a2ec72389ca8ecd150f4f1a864e4a05c6d0fdf3545c82a27d2fc0384a08c39d8

METADATA SHA-256:

b9d3aa33077ed75e513b3b258d3598a84a19410a2760690961e286640393458b

SOURCE SIZE:

24.238 bytes

SOURCE LENGTH:

820 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

SOURCE STAGE:

anti-hallucination-prompt-groups-show-project-copy-buttons-v1

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

FIRST-PROMPTS STARTUP COPY:

ausente, corretamente on request

DIRECT REFERENCE SURFACES:

5 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 12

FEATURE-SPECIFIC VALIDATOR:

presente

VALIDATOR PATH:

tools/validate_anti_hallucination_prompt_groups_show_project_buttons_v1.py

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

Manter KPR-09-006 somente como protocolo final de síntese de evidência, truthful reporting e estado de verificação.

O prompt contém princípios fortes e úteis, mas seu corpo atual de 820 linhas é um mega-canon que reproduz responsabilidades de praticamente toda a arquitetura de governança:

    Brick Wall;

    Prompt 085, revisão adversarial;

    Prompt 090, verificação web;

    Prompt 082, literatura;

    Box Architecture;

    Tool/Project Boundary;

    Error Handling;

    Security;

    Testing;

    Validation;

    module-size governance;

    dependency governance;

    human authorization;

    response formatting.

No train full, ele é carregado depois de Independent Audit, Web Audit e Literature Audit. Entretanto, repete novamente esses três estágios. Isso aumenta drasticamente o contexto sem criar uma nova camada claramente distinta.

Sua função final deve ser:

    receber resultados dos estágios;

    reconciliar conflitos;

    registrar evidence state;

    identificar blockers e pontos ainda não verificados;

    produzir o plano final condicionado;

    impedir alegações falsas de execução ou validação;

    devolver a decisão à governança.

Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim, após redução radical

KPR-09-006 deve possuir:

    síntese final do train full;

    normalização dos estados de evidência;

    conflito entre repository, runtime, docs e inferência;

    validação de que claims materiais possuem provenance;

    separação entre candidate, verified, approved e canonicalized;

    final evidence ledger;

    registro de pontos não verificados;

    truthful final reporting;

    handoff para Brick Wall ou para o owner de validação.

Não deve possuir:

    auditoria adversarial completa;

    pesquisa web;

    auditoria de livros;

    module-size canon;

    arquitetura de caixas;

    Error Handling geral;

    Security geral;

    política de testes;

    política de dependências;

    implementação;

    entrega;

    freeze.

Positive findings
P087-001 — O prompt reconhece que nenhum prompt elimina hallucination

A distinção entre geração de candidato e verificação é correta.
P087-002 — Alegações de execução falsa são explicitamente proibidas

O texto proíbe inventar:

    testes;

    comandos;

    resultados;

    benchmarks;

    APIs;

    versões;

    runtime behavior.

P087-003 — Há um modelo explícito de evidência

As categorias REPO_VERIFIED, DOC_VERIFIED, EXEC_VERIFIED, INFERRED, ASSUMED e UNVERIFIED ajudam a comunicar incerteza.
P087-004 — Source truth precede memória do modelo

O prompt rejeita tratar nomes plausíveis como prova de símbolos ou contratos.
P087-005 — Generated artifact não se torna automaticamente canonical source

Esse é um princípio essencial para KANDA.
P087-006 — Scope discipline é forte

Mudanças não relacionadas devem permanecer fora do patch principal.
P087-007 — Dependências não podem ser inventadas

O prompt exige verificação de identidade, documentação, compatibilidade e política do projeto.
P087-008 — A Validation Ladder é útil

Ela diferencia:

    revisão estática;

    compilação;

    qualidade estática;

    targeted tests;

    regressão;

    system validation;

    real user-environment validation.

P087-009 — Human authorization permanece separada de validação

Generated, validated, approved e canonicalized são estados diferentes.
P087-010 — A correção de erro deve ser explícita

O prompt proíbe esconder falhas anteriores.
Critical and high-severity findings
F087-001 — O prompt é um mega-canon de 820 linhas

Ele tenta possuir quase toda a engenharia governada.

Isso contradiz o princípio do próprio projeto de um owner canônico por responsabilidade.
F087-002 — “Master Protocol” sugere autoridade superior indevida

O prompt não pode substituir:

    Brick Wall;

    source owners;

    Box Architecture;

    Security;

    Testing;

    Delivery;

    Freeze.

O nome histórico pode permanecer por compatibilidade, mas o corpo deve declarar que é um synthesis protocol, não master authority.
F087-003 — A Authority Order coloca o pedido humano acima da governança

A ordem começa com:

    current explicit human request;

    active project governance and frozen behavior.

Em trabalho governado, o usuário não deve poder sobrepor:

    safety;

    governance;

    protected frozen behavior;

    write boundaries;

    system contracts.

A ordem precisa colocar governança aplicável e segurança antes de instruções de implementação conflitantes.
F087-004 — Frozen behavior não é identity-bound

“Active project governance and frozen behavior” não é suficiente.

É necessário provar:

    projeto;

    feature;

    owner;

    source identity;

    applicability;

    freshness;

    supersession state.

F087-005 — TEST_VERIFIED é ambíguo

A definição diz que a claim é suportada por um teste inspecionado.

Isso não prova que o teste passou.

Estados separados são necessários:

    TEST_CONTRACT_INSPECTED;

    TEST_EXECUTED_PASS;

    TEST_EXECUTED_FAIL;

    TEST_NOT_EXECUTED.

F087-006 — DOC_VERIFIED não exige version binding completo

A documentação precisa ser vinculada a:

    package;

    versão instalada ou alvo;

    data de recuperação;

    source identity;

    platform profile.

F087-007 — Os evidence labels não possuem operation identity

Uma claim pode estar verificada para:

    outro projeto;

    outra versão;

    outro source snapshot;

    outro ambiente.

Cada evidence record deve ser vinculado ao trabalho atual.
F087-008 — A revisão adversarial exige pelo menos três weaknesses

Isso reproduz o problema do Prompt 085.

Buscar criticamente é correto.

Exigir uma quantidade mínima incentiva fabricação de findings.
F087-009 — “Separate reviewer” não define independência

Pode ser:

    o mesmo modelo;

    a mesma conversa;

    o mesmo plano visível;

    o mesmo contexto.

O prompt deve registrar o tipo real de review.
F087-010 — Web verification duplica integralmente Prompt 090

KPR-09-006 deve consumir o output do Web Audit, não repetir sua metodologia.
F087-011 — Book audit duplica integralmente Prompt 082

A síntese final precisa apenas avaliar o resultado da literatura.
F087-012 — Plan-first gate duplica Brick Wall

O prompt cria um segundo sistema para decidir quando um plano pode prosseguir.

Brick Wall deve permanecer a autoridade de implementação.
F087-013 — Claim Ledger duplica Independent, Web e Literature stages

Cada estágio cria um ledger próprio sem um schema compartilhado.

O resultado pode conter claims duplicadas, divergentes ou com IDs incompatíveis.
F087-014 — O prompt não define um stage-handoff schema

Faltam campos comuns como:

    operation_id;

    plan_hash;

    source_snapshot;

    claim_id;

    evidence_id;

    stage;

    reviewed_at;

    invalidation_conditions.

F087-015 — A module-size law está duplicada

O limite de módulos pertence ao owner ativo de arquitetura e refatoração.
F087-016 — Error Handling, Concurrency e Security estão duplicados

As seções 16–18 resumem especialistas inteiros.

A síntese deveria apenas verificar se os owners relevantes foram consultados.
F087-017 — Test Design duplica Pytest e Brick Wall

Não deve se tornar a política geral de testes.
F087-018 — No-Leak e ownership são reproduzidos

Esses contratos pertencem a Box Architecture, Tool Boundary e Governed Architecture Companion.
F087-019 — Error Memory preflight não é formalmente consumido

O prompt inclui correção após falha, mas não exige revisão das lições relevantes antes de implementar.
F087-020 — Não há comportamento quando os estágios anteriores estão incompletos

O grupo pode chegar ao Master com:

    Web Audit não executado;

    literatura não aplicável;

    reviewer não independente;

    source snapshot alterado.

O synthesis protocol precisa lidar explicitamente com esses estados.
F087-021 — A saída normal é orientada a implementação

KPR-09-006 deve também suportar:

    NO_CHANGE;

    BLOCKED;

    SOURCE_INSPECTION_REQUIRED;

    RUNTIME_VALIDATION_REQUIRED;

    PLAN_REJECTED;

    GOVERNANCE_DECISION_REQUIRED.

F087-022 — Os routing intents são genéricos

“anti hallucination” e “verify AI code claims” não diferenciam Master Protocol dos outros nove assets.
F087-023 — A fonte não possui versão semântica

O contrato de 820 linhas precisa de versionamento e compatibilidade com o train.
F087-024 — O validador atual não prova a semântica do Master Protocol

Ele prova:

    arquivo;

    code;

    metadata;

    folder registration;

    wrapper;

    ordem;

    UI;

    line counts dos módulos de interface.

Não prova owner boundaries ou evidence semantics.
Current owner model

KPR-09-006 deve possuir:

    synthesis;

    evidence-state reconciliation;

    conflict resolution;

    final uncertainty report;

    truthful completion status.

KPR-09-003 deve possuir:

    adversarial review.

KPR-09-004 deve possuir:

    web evidence.

KPR-09-005 deve possuir:

    literature evidence.

KPR-09-001 deve possuir:

    train orchestration.

Brick Wall deve possuir:

    implementation authorization.

Os specialist prompts devem possuir:

    Security;

    Testing;

    Resilience;

    Observability;

    ownership;

    delivery.

Recommended final structure

    Identity and protocol version

    Purpose as synthesis, not master authority

    Required train inputs

    Operation and source identity

    Stage completion states

    Shared claim/evidence schema

    Conflict-resolution rules

    Final claim disposition

    Remaining uncertainty

    Validation status

    Governance handoff

    Non-authorization statement

    Historical compatibility

    Version history

Final disposition

CLASSIFICATION:

Full-train evidence synthesis and truthful completion protocol

ACTION:

KEEP KPR-09-006, RADICALLY REDUCE, REMOVE DUPLICATED SPECIALIST CANONS, AND REDEFINE MASTER AS SYNTHESIS RATHER THAN AUTHORITY

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_mega_canon_scope_authority_conflict_stage_duplication_and_unbound_evidence_states

EXPECTED FINAL STATUS:

active reduced synthesis protocol

FINAL LOAD TYPE:

on_request only as the final stage of the full verification train

PROMPT CODE:

retain KPR-09-006

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 087 was fully audited and formally closed.

No source, metadata, routing, group wrapper, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 088
Identity

AUDIT_ID:

A088-20260715-REVIEW

PROMPT:

anti_hallucination_protocol_short.md

PROMPT CODE:

KPR-09-010

CANONICAL ID:

anti_hallucination_protocol_short

DISPLAY NAME:

Anti-Hallucination Protocol Short

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_protocol_short.md

SOURCE SHA-256:

5c5b95b72dd2fe3f3ac716e6e29d249237a3a9c2caddd5a3e5e3ddedccfada26

METADATA SHA-256:

dc61a5cc3552e687715d0f8c9aa70ca3e7d55f8c3e8bc1ea5b687c7f355dff07

SOURCE SIZE:

4.033 bytes

SOURCE LENGTH:

170 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

09_python_quality_security_observability

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

4 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 11

FEATURE-SPECIFIC VALIDATOR:

presente

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter KPR-09-010 somente como perfil compacto derivado do synthesis protocol full.

A fonte atual é uma cópia resumida manualmente. Ela não possui vínculo verificável com KPR-09-006 e já apresenta diferenças semânticas no modelo de evidência.

Não deve evoluir como segundo canon independente.
Positive findings
P088-001 — A versão curta preserva truthful reporting
P088-002 — Não permite inventar execução
P088-003 — Preserva source hierarchy
P088-004 — Preserva Claim Ledger
P088-005 — Preserva scope e no-leak
P088-006 — Preserva Validation Ladder
P088-007 — O tamanho é compatível com uso compacto
Critical and high-severity findings
F088-001 — É uma segunda fonte manual

Não há:

    derived_from;

    full_prompt_version;

    source hash;

    generation rule;

    compatibility matrix.

F088-002 — O modelo de evidência diverge do full

A versão curta omite estados presentes no full, incluindo:

    TEST_VERIFIED;

    CONFLICTING_EVIDENCE.

Isso comprova drift.
F088-003 — A source truth order repete o problema de autoridade

Human request aparece antes de governance.
F088-004 — Mantém a quota de três weaknesses
F088-005 — Mantém “independent critic” sem classificação de independência
F088-006 — Web Audit é resumido dentro do synthesis prompt
F088-007 — Book Audit também é resumido
F088-008 — A module-size law é duplicada
F088-009 — Não há operation identity
F088-010 — Não há stage input contract
F088-011 — Não há vínculo com Short Group version
F088-012 — Não há escalation behavior para o full protocol
F088-013 — Não há invalidation conditions
F088-014 — Não há Error Memory preflight
F088-015 — Os routing intents são iguais aos demais prompts da família
F088-016 — O validador não compara semântica full-short
F088-017 — Não há versão semântica
F088-018 — Não há non-authorization statement suficientemente explícito
Final disposition

CLASSIFICATION:

Derived compact synthesis and truthful-reporting profile

ACTION:

KEEP KPR-09-010 AS A DERIVED OR GENERATED PROFILE; DO NOT MAINTAIN IT AS AN INDEPENDENT CANON

EXPECTED FINAL STATUS:

active derived profile

PROMPT CODE:

retain KPR-09-010

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 088 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.
PROMPT AUDIT REPORT 089
Identity

AUDIT_ID:

A089-20260715-REVIEW

PROMPT:

anti_hallucination_short_group.md

PROMPT CODE:

KPR-09-002

CANONICAL ID:

anti_hallucination_short_group

DISPLAY NAME:

Anti-Hallucination Short Group

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_short_group.md

SOURCE SHA-256:

fd71abbb0ab266070efe957cf12265fa2982d19c50e9c147e6782a5b8f00377e

METADATA SHA-256:

6fdf06f7d01317bf409451c1cdccf8547494b364c39c2604035269f80e83144e

SOURCE SIZE:

1.186 bytes

SOURCE LENGTH:

23 linhas

METADATA STATUS:

active

LOAD TYPE:

routed

DIRECT REFERENCE SURFACES:

5 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 13
Overall verdict

Manter KPR-09-002 como roteador compacto, mas reduzir sua ativação padrão e permitir seleção condicional de estágios.

Hoje o grupo sempre aplica:

    Independent Short;

    Web Short;

    Literature Short quando aplicável;

    Protocol Short.

Isso significa que até um problema totalmente resolvível por source inspection recebe Web Audit automaticamente.
Positive findings

    É curto.

    Possui ordem explícita.

    Literature é condicional.

    Define escalonamento para o full.

    Preserva truthful reporting.

Critical findings
F089-001 — “Default compact companion” é amplo demais

Praticamente todo trabalho de software contém alguma incerteza.
F089-002 — Web Audit é obrigatório mesmo sem claim externa

O estágio deveria poder ser:

    REQUIRED;

    OPTIONAL;

    NOT_APPLICABLE;

    BLOCKED.

F089-003 — Independent Audit também é sempre obrigatório

Uma mudança pequena, determinística e source-grounded pode não justificar outro reviewer.
F089-004 — Não há risk admission record
F089-005 — Não há operation ID ou plan hash
F089-006 — Não há handoff schema
F089-007 — Não há stage stop conditions
F089-008 — Não há comportamento para web indisponível
F089-009 — Não há comportamento para source alterado durante o train
F089-010 — O escalation rule é amplo

“Unfamiliar”, “material risk” e “uncertainty” precisam de critérios operacionais.
F089-011 — O short group não possui versão compatível dos cinco componentes
F089-012 — Error Memory não aparece no admission
F089-013 — Os routing intents não distinguem group de stage
F089-014 — O validador prova apenas integração
Final disposition

CLASSIFICATION:

Compact evidence-verification train router

ACTION:

KEEP KPR-09-002, ADD RISK ADMISSION, CONDITIONAL STAGE SELECTION, HANDOFF IDENTITY, STOP CONDITIONS, AND VERSION COMPATIBILITY

EXPECTED FINAL STATUS:

active routed group

PROMPT CODE:

retain KPR-09-002
Closure record

Prompt 089 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.
PROMPT AUDIT REPORT 090
Identity

AUDIT_ID:

A090-20260715-REVIEW

PROMPT:

anti_hallucination_web_evidence_audit_full.md

PROMPT CODE:

KPR-09-004

CANONICAL ID:

anti_hallucination_web_evidence_audit_full

DISPLAY NAME:

Anti-Hallucination Web Evidence Audit Full

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_web_evidence_audit_full.md

SOURCE SHA-256:

3e8a27a8fca598793bcbce8dc8b1686b3c795f71475525ccaab4a8597c888750

METADATA SHA-256:

e43f96cbab1095ebd65902121496efc1e51f0410016fcbab5cfecada39d317b0

SOURCE SIZE:

5.696 bytes

SOURCE LENGTH:

199 linhas

METADATA STATUS:

active

LOAD TYPE:

on_request

DIRECT REFERENCE SURFACES:

5 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 12
Overall verdict

Manter KPR-09-004 como especialista de verificação externa atual e disconfirmation search.

A capacidade é distinta e importante.

O prompt deve, porém:

    receber uma operação selada;

    proteger dados privados durante pesquisa;

    registrar data, versão e provenance de cada fonte;

    diferenciar fatos atuais de recomendações;

    definir comportamento sem acesso web;

    evitar output excessivo;

    tornar-se compatível com a versão curta.

Positive findings
P090-001 — Pesquisa de disconfirmation é obrigatória
P090-002 — Source count não é usado como votação
P090-003 — Primary sources possuem prioridade
P090-004 — Generic web advice não supera project source
P090-005 — Unresolved claims permanecem UNVERIFIED
P090-006 — Performance claims exigem benchmark evidence
P090-007 — Web evidence não se torna implementation authorization
P090-008 — O prompt distingue ADOPT, ADAPT, REJECT e DEFER
Critical and high-severity findings
F090-001 — O prompt presume estágios anteriores completos

Ele exige:

    initial plan;

    independent audit;

    claim list.

Não define comportamento standalone ou com input incompleto.
F090-002 — Não há operation identity

Faltam:

    task ID;

    plan hash;

    source snapshot;

    project ID;

    dependency environment;

    reviewed-at;

    invalidation conditions.

F090-003 — Não há proteção de confidencialidade para pesquisas

A IA não deve enviar para mecanismos externos:

    source privado;

    credenciais;

    logs sensíveis;

    nomes de pacientes;

    dados de usuários;

    internal URLs;

    proprietary architecture.

F090-004 — Não há data-minimization rule

Consultas devem usar apenas o mínimo necessário para verificar a claim.
F090-005 — Não há comportamento quando web não está disponível

O correto seria:

WEB_EVIDENCE_NOT_RETRIEVED

e não uma resposta baseada em memória.
F090-006 — Source provenance é incompleta

Cada finding deveria registrar:

    URL ou source identity;

    publisher/owner;

    retrieved_at;

    relevant version;

    relevant date;

    source type;

    exact claim supported;

    applicability.

F090-007 — “Current confidence” é subjetivo

O campo deve ser evidence status, não apenas sensação de confiança.
F090-008 — A hierarquia A/B/C/D é simplista

Um issue oficial pode ser evidência primária de um bug.

Uma documentação oficial pode estar desatualizada.

A classificação precisa considerar:

    authority;

    recency;

    version fit;

    directness;

    reproducibility.

F090-009 — “Current best practices” é uma categoria vaga

Best practice depende do contexto e não deve ser tratada como contrato universal.
F090-010 — Não há controle de copyright

A auditoria deve resumir fontes e evitar reprodução extensa de conteúdo protegido.
F090-011 — Não há política para conflitos entre fontes oficiais

Exemplos:

    docs versus changelog;

    docs versus package source;

    current docs versus installed older version.

F090-012 — Não há environment binding

Uma API documentada pode não existir na versão instalada.
F090-013 — O prompt não exige links entre claim e evidence IDs
F090-014 — O required output de dez seções pode ser excessivo

Uma única claim de API pode ser resolvida com um relatório curto.
F090-015 — Não há evidence expiry

Claims sobre APIs, segurança e packages podem ficar stale rapidamente.
F090-016 — Routing intents são genéricos

O trigger deve incluir:

    verify current API;

    check current package documentation;

    web evidence;

    external disconfirmation;

    version compatibility research.

F090-017 — Não há versão semântica
F090-018 — Full e short não possuem binding
F090-019 — O validador não verifica provenance ou privacy
F090-020 — Não há explicit source-redaction record
Current owner model

KPR-09-004 deve possuir:

    current external evidence;

    official documentation verification;

    disconfirmation;

    source conflict analysis;

    evidence provenance.

KPR-09-003 deve possuir:

    plan criticism.

KPR-09-005 deve possuir:

    books and literature.

KPR-09-006 deve possuir:

    synthesis.

Final disposition

CLASSIFICATION:

Current external evidence and disconfirmation specialist

ACTION:

KEEP KPR-09-004, ADD OPERATION IDENTITY, PRIVACY-SAFE SEARCH, SOURCE PROVENANCE, WEB-UNAVAILABLE BEHAVIOR, AND FULL-SHORT VERSION BINDING

EXPECTED FINAL STATUS:

active

PROMPT CODE:

retain KPR-09-004
Closure record

Prompt 090 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.
PROMPT AUDIT REPORT 091
Identity

AUDIT_ID:

A091-20260715-REVIEW

PROMPT:

anti_hallucination_web_evidence_audit_short.md

PROMPT CODE:

KPR-09-008

CANONICAL ID:

anti_hallucination_web_evidence_audit_short

DISPLAY NAME:

Anti-Hallucination Web Evidence Audit Short

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/anti_hallucination_web_evidence_audit_short.md

SOURCE SHA-256:

b412baea5f6881f0e81f30ce538d3f79f87e976862d61deff73f662287b49efa

METADATA SHA-256:

a36d91dc4eca05cd35dd5ff2171a3234b3da4bd03bc885d25772a7a81443b8db

SOURCE SIZE:

1.464 bytes

SOURCE LENGTH:

37 linhas

METADATA STATUS:

active

LOAD TYPE:

on_request

DIRECT REFERENCE SURFACES:

4 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 11
Overall verdict

Manter KPR-09-008 somente como perfil compacto derivado de KPR-09-004.

Ele preserva o núcleo correto de pesquisa e disconfirmation, mas não possui provenance, privacy, escalation ou binding com o full prompt.
Positive findings

    Source hierarchy é preservada.

    Search support e counterexamples são exigidos.

    Source count não é votação.

    Claims não resolvidas permanecem explicitamente abertas.

    ADOPT/ADAPT precisam alterar o plano concretamente.

Critical findings
F091-001 — Cópia manual paralela do full
F091-002 — Não há full source hash ou minimum version
F091-003 — Não há escalonamento para o full
F091-004 — Presume initial plan e independent audit
F091-005 — Não há operation identity
F091-006 — Não há privacy-safe search
F091-007 — Não há data minimization
F091-008 — Não há retrieved-at ou version relevance record
F091-009 — Não há web-unavailable state
F091-010 — Não há evidence expiry
F091-011 — Não há source conflict policy detalhada
F091-012 — Routing intents são genéricos
F091-013 — Não há versão semântica
F091-014 — O validador não compara full-short
F091-015 — Não há non-authorization statement separado
Final disposition

CLASSIFICATION:

Derived compact web evidence and disconfirmation profile

ACTION:

KEEP KPR-09-008 AS A DERIVED SHORT PROFILE, ADD ESCALATION, PRIVACY, PROVENANCE, AND VERSION BINDING

EXPECTED FINAL STATUS:

active derived profile

PROMPT CODE:

retain KPR-09-008
Closure record

Prompt 091 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.
PROMPT AUDIT REPORT 092
Identity

AUDIT_ID:

A092-20260715-REVIEW

PROMPT:

python_documentation_developer_experience.md

METADATA CANONICAL ID:

python_documentation_developer_experience

SOURCE-DECLARED CANONICAL ID:

documented_python_docs_developer_experience_onboarding

SOURCE AUDIT ID:

A016

DISPLAY NAME:

Python Documentation and Developer Experience

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability/python_documentation_developer_experience.md

SOURCE SHA-256:

69e3faaf6eb7583ae6d2b456bb84ff01f0cb44bd89b7f1938abe8d474763f397

METADATA SHA-256:

69aa9a08638d51e75cf588e545cf54d2c231b9cda93cb7f38a37b787e98fc2bc

SOURCE SIZE:

12.238 bytes

SOURCE LENGTH:

375 linhas

SOURCE VERSION:

1.1-audited

SOURCE STATUS:

audited_candidate

METADATA STATUS:

active

LOAD TYPE:

on_request

PRIORITY:

45

PROMPT CODE:

ausente

SOURCE STAGE:

mechanically_reconciled_from_prompt_library

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e idêntica

DIRECT REFERENCE SURFACES:

13 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 35

GENERATED MANIFEST CANONICAL PATH:

em branco

ACTIVE DUPLICATE SOURCE:

não encontrado

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado
Overall verdict

Manter Prompt 092 como especialista em documentação técnica e developer experience, mas atualizar identidade, lifecycle, plataforma, audience model e ownership.

A fonte atual contém boa base conceitual:

    docs as code;

    tutorials;

    how-to guides;

    explanations;

    references;

    README;

    docstrings;

    ADRs;

    onboarding;

    contributing guides.

Entretanto, ela transforma um toolkit opcional em workflow obrigatório e contém exemplos Unix-centric incompatíveis com o ambiente Windows do projeto.
Positive findings
P092-001 — Documentação possui ownership claro
P092-002 — O modelo Tutorial/How-to/Explanation/Reference é útil
P092-003 — README é tratado como entrada do projeto
P092-004 — ADRs são usados para decisões significativas
P092-005 — Docs devem acompanhar mudanças de código
P092-006 — Exemplos, links e geração podem ser testados
P092-007 — Segredos não devem aparecer em exemplos
P092-008 — Contributing guide e onboarding são reconhecidos como produtos importantes
Critical and high-severity findings
F092-001 — Canonical identity é inconsistente

Source:

documented_python_docs_developer_experience_onboarding

Metadata:

python_documentation_developer_experience
F092-002 — Lifecycle é inconsistente

Source:

audited_candidate

Metadata:

active
F092-003 — Audit ID permanece na fonte operacional

A016 deve permanecer apenas no histórico.
F092-004 — A persona de 15+ anos deve ser removida
F092-005 — Os blocos Markdown estão estruturalmente malformados

A fonte abre um bloco:


e tenta abrir blocos internos com a mesma sequência de backticks.

Isso encerra prematuramente o bloco externo.

O mesmo problema aparece no exemplo de CONTRIBUTING.

### F092-006 — “Healthy project needs all four” é absoluto

Um pequeno pacote interno pode não precisar de tutorial, explanation e reference separados.

### F092-007 — Google docstring style não deve ser default universal

A convenção do projeto deve prevalecer.

### F092-008 — Doctest não é apropriado para todo exemplo

Pode ser frágil para:

- timestamps;
- nondeterminism;
- formatting;
- network;
- platform differences;
- long outputs.

### F092-009 — ADR para toda dependência ou refatoração significativa pode gerar ruído

É necessário um admission threshold.

### F092-010 — One-command onboarding é uma meta, não um contrato universal

Projetos regulados ou com hardware podem exigir passos humanos.

### F092-011 — O Makefile é Unix-specific

Inclui:

- `. venv/bin/activate`;
- shell chaining;
- comandos não nativos de Windows.

### F092-012 — `pre-commit install` é uma ação de estado

Não deve ser executada sem autorização.

### F092-013 — Devcontainers e Docker não são obrigatórios

A fonte privilegia um stack específico.

### F092-014 — “Do not hand-write API docs” é excessivo

Referência pode ser gerada, mas narrative documentation precisa ser escrita e revisada.

### F092-015 — “Interactive and always up to date” é uma promessa não garantida

### F092-016 — Ferramentas e hosting são estáticos

O prompt precisa verificar o toolchain atual.

### F092-017 — A workflow sempre tenta criar dez tipos de artefato

Isso causa scope sprawl.

### F092-018 — Não há audience matrix

Faltam:

- internal maintainer;
- contributor;
- end user;
- operator;
- API consumer;
- administrator.

### F092-019 — Não há documentação de ownership e freshness

Cada artefato deveria registrar:

- owner;
- canonical source;
- update trigger;
- last verified version;
- stale conditions.

### F092-020 — Não há distinção entre canonical docs e generated docs

### F092-021 — Durable Document Artifact Routing não é consumido

Documentos duráveis devem ir ao Project Support correto, não a daily-work.

### F092-022 — Accessibility e localization estão ausentes

### F092-023 — Privacy review é insuficiente

Documentação pode vazar:

- internal hosts;
- account IDs;
- patient data;
- proprietary screenshots;
- secrets;
- local paths.

### F092-024 — Output obrigatório é excessivo

Nem toda correção de docstring precisa de:

- MkDocs;
- CI;
- devcontainer;
- ADR;
- onboarding verification.

### F092-025 — A abertura obrigatória gera ruído

### F092-026 — Box Logic é carregada incondicionalmente

### F092-027 — Required companions são excessivos

### F092-028 — Routing aliases incluem termos de quality, security e observability

Isso pode gerar seleção incorreta.

### F092-029 — O manifest deixa canonical path em branco

### F092-030 — Não há whole-prompt validator

## Current owner model

Prompt 092 deve possuir:

- documentação;
- information architecture;
- audience;
- README;
- tutorials/how-to/reference/explanation;
- ADR records;
- onboarding documentation;
- docs quality.

Durable Document Routing deve possuir:

- destino persistente.

API Design deve possuir:

- contrato de API.

Lifecycle deve possuir:

- changelog/versioning/deprecation.

Testing deve possuir:

- test mechanics.

Brick Wall deve possuir:

- source-write authorization.

## Final disposition

CLASSIFICATION:

Python documentation architecture and developer-experience specialist

ACTION:

KEEP, RECONCILE IDENTITY/LIFECYCLE, REPAIR MARKDOWN, MAKE TOOLING CONDITIONAL, ADD AUDIENCE/FRESHNESS/DURABLE-ROUTING CONTROLS, AND REMOVE UNIX-ONLY DEFAULTS

EXPECTED FINAL STATUS:

active

PROMPT CODE:

assign only after Class 09 identity review

## Closure record

Prompt 092 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.

---

# PROMPT AUDIT REPORT 093

## Identity

AUDIT_ID:

A093-20260715-REVIEW

PROMPT:

python_observability_logging_metrics_tracing.md

CANONICAL ID:

python_observability_logging_metrics_tracing

DISPLAY NAME:

Python Observability Logging Metrics and Tracing

SOURCE SHA-256:

0decf56d5de96852fe9f8a4355e11b336febed39db758711eccb9101a9e420d0

METADATA SHA-256:

bf4395098ed1a13da43674bb12d0252c0a47416ba8863861ec30eb46240d3a03

SOURCE SIZE:

9.886 bytes

SOURCE LENGTH:

236 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

PRIORITY:

45

PROMPT CODE:

ausente

DIRECT REFERENCE SURFACES:

12 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 32

GENERATED MANIFEST CANONICAL PATH:

em branco

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

## Overall verdict

Manter Prompt 093 como especialista em logging, metrics, tracing e operational visibility.

O prompt atual contém princípios importantes, mas aplica um stack de microservices e Kubernetes a qualquer software Python.

Também contém contradições críticas envolvendo PII e metric cardinality.

## Positive findings

- Diferencia logs, métricas e traces.
- Promove structured logging.
- Evita secrets.
- Reconhece high-cardinality labels.
- Distingue liveness e readiness.
- Inclui custos de sampling.
- Recomenda alertas baseados em sintomas.
- Integra observability com operação.

## Critical and high-severity findings

### F093-001 — “Use all three” é uma regra universal incorreta

Um CLI local pode precisar apenas de logs.

Um serviço simples pode precisar de métricas sem tracing distribuído.

### F093-002 — “JSON everywhere in production” é excessivo

O formato deve seguir o collector e o deployment profile.

### F093-003 — Há contradição sobre PII

A fonte manda incluir `user_id` em todo log, mas depois proíbe PII.

User ID pode ser dado pessoal ou identificador sensível.

### F093-004 — Request ID nunca deve ser metric label

A fonte sugere correlation ID em metric labels “in moderation”.

Isso gera cardinalidade praticamente ilimitada.

### F093-005 — O middleware aceita X-Request-ID não confiável

Faltam:

- validação;
- limite de tamanho;
- character policy;
- geração de novo ID para valores inválidos.

### F093-006 — O contextvar não é resetado

O exemplo deveria usar token e `finally`.

### F093-007 — contextvars não propagam automaticamente para qualquer thread

### F093-008 — O middleware não protege cleanup em exceção

### F093-009 — O label endpoint pode ter cardinalidade alta

Deve usar route template, não raw path.

### F093-010 — A explicação de Prometheus Summary é inadequada

A implementação Python do client não deve ser presumida como quantile calculator sem verificação atual.

### F093-011 — O stack OpenTelemetry pode estar desatualizado

Exporters, packages e APIs devem ser verificados contra a versão instalada.

### F093-012 — Readiness não deve automaticamente depender de todo serviço externo

Isso pode causar cascading unavailability.

### F093-013 — Health probes podem sobrecarregar dependências

### F093-014 — Alertar somente sintomas é absoluto demais

Infraestrutura crítica como filesystem exhaustion também pode exigir alertas diretos.

### F093-015 — SLOs de exemplo são apresentados como números prontos

Devem vir de objetivos do serviço.

### F093-016 — `<100 values per label` é threshold arbitrário

O problema depende do produto cartesiano de labels e do volume temporal.

### F093-017 — Sampling de 1% é arbitrário

### F093-018 — Log rotation pode pertencer à plataforma

Aplicações containerizadas normalmente escrevem em stdout e delegam rotação.

### F093-019 — O prompt sempre adiciona logs, metrics, traces, health, alerts e dashboard

Isso causa overinstrumentation.

### F093-020 — Não há telemetry budget

Faltam limites de:

- custo;
- volume;
- storage;
- latency overhead;
- retention.

### F093-021 — Data retention e compliance estão ausentes

### F093-022 — Não há event schema/versioning

### F093-023 — Não há tracing trust-boundary rule

Incoming trace context pode ser controlado externamente.

### F093-024 — Não distingue library, CLI, GUI desktop e service

### F093-025 — Não há validation strategy para instrumentation

### F093-026 — A persona de 15+ anos deve ser removida

### F093-027 — Box Logic e companions são incondicionais

### F093-028 — Routing aliases são amplos

### F093-029 — Não há version, prompt code ou canonical path no manifest

### F093-030 — Não há semantic validator

## Final disposition

CLASSIFICATION:

Proportional Python observability and operational-diagnostics specialist

ACTION:

KEEP, UPDATE FOR PROPORTIONAL INSTRUMENTATION, FIX PII/CARDINALITY/CONTEXT CLEANUP, ADD PLATFORM AND COST PROFILES, AND VERIFY ALL CURRENT TOOL APIs

EXPECTED FINAL STATUS:

active

## Closure record

Prompt 093 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.

---

# PROMPT AUDIT REPORT 094

## Identity

AUDIT_ID:

A094-20260715-REVIEW

PROMPT:

python_resilience_error_handling.md

CANONICAL ID:

python_resilience_error_handling

DISPLAY NAME:

Python Resilience and Error Handling

SOURCE SHA-256:

49aabd1ceb767b5da3a79074e593e0a549f6f9acd68ab006ab703e5f1fe76a24

METADATA SHA-256:

71635cf62f03486e81e3f9921ac352bdd9117deaad8ce66c03a55f41695de608

SOURCE SIZE:

13.593 bytes

SOURCE LENGTH:

305 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

PRIORITY:

45

PROMPT CODE:

ausente

DIRECT REFERENCE SURFACES:

12 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 32

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

## Overall verdict

Manter Prompt 094 como especialista em failure semantics, timeout, retry, idempotency, degradation, circuit breaker e recovery.

O prompt atual tem falhas técnicas importantes. A mais grave é uma contradição entre a política de retries e o próprio exemplo com Tenacity: o texto diz para não retry 4xx, mas o decorator retries qualquer `httpx.HTTPStatusError`, incluindo 4xx.

O exemplo de idempotency para pagamentos também é inseguro por usar check-then-act não atômico.

## Positive findings

- Timeouts são tratados como parte do contrato.
- Jitter é reconhecido.
- Retry infinito é proibido.
- Idempotency é vinculada a duplicate side effects.
- Circuit breaker possui estados explícitos.
- Bulkheading é reconhecido.
- Fallback e degradation são considerados.
- Observability para retries e circuit state é mencionada.

## Critical and high-severity findings

### F094-001 — “Always have a fallback” é incorreto

Em pagamentos, autorização ou dados críticos, o comportamento correto pode ser fail closed.

### F094-002 — “Timeouts everywhere, no exceptions” é amplo demais

Timeout é central para operações bloqueantes ou remotas, não para toda função local.

### F094-003 — Os valores de timeout são arbitrários

Devem vir de:

- latency budget;
- downstream SLO;
- user deadline;
- retry budget;
- operation criticality.

### F094-004 — `requests timeout=3` não é total deadline

### F094-005 — O exemplo Tenacity retries 4xx

`retry_if_exception_type(httpx.HTTPStatusError)` inclui qualquer status transformado por `raise_for_status()`.

### F094-006 — A própria anti-pattern table diz não retry 4xx

Há contradição interna direta.

### F094-007 — Nem todo 5xx é retryable

E alguns 4xx podem ser, dependendo do contrato:

- 408;
- 409;
- 425;
- 429.

### F094-008 — Deadlock retry deve envolver a transação inteira

Retry de uma única statement pode deixar estado inconsistente.

### F094-009 — O cliente HTTP é recriado a cada tentativa

Isso perde pooling e pode aumentar carga.

### F094-010 — Circuit breaker para toda API externa é excessivo

### F094-011 — `ThreadPoolExecutor(max_workers=10)` não possui fila limitada

O executor padrão pode acumular tarefas.

### F094-012 — Empty/default fallback pode ocultar falhas

O caller precisa saber que recebeu degraded data.

### F094-013 — Stale cache precisa de freshness metadata

### F094-014 — O exemplo de idempotency possui race check-then-act

Dois requests podem passar por `exists()` simultaneamente.

### F094-015 — O charge e o armazenamento da key não são atômicos

Crash após a cobrança e antes do Redis write permite duplicate charge.

### F094-016 — A key não é namespaced

Pode haver colisão entre:

- usuários;
- endpoints;
- tenants;
- operation types.

### F094-017 — TTL de 24 horas é arbitrário

### F094-018 — DELETE e PUT não são sempre idempotentes na prática

Side effects, event emission e audit records podem alterar o resultado.

### F094-019 — Readiness vinculada a todas as dependências pode causar cascading outage

### F094-020 — Publicar heartbeat em broker pode ter side effects

### F094-021 — Circuit state não equivale a dependency health

### F094-022 — Graceful shutdown está subespecificado e possui suposições de plataforma

### F094-023 — Falta deadline propagation

### F094-024 — Falta backpressure e load shedding

### F094-025 — Falta outbox/inbox para efeitos distribuídos

### F094-026 — Falta cancellation policy

### F094-027 — Falta partial-completion state model

### F094-028 — APIs das bibliotecas são estáticas e exigem verificação atual

### F094-029 — O workflow sempre adiciona todos os patterns

### F094-030 — Não há failure-criticality classification

### F094-031 — Não há task mode ou source freshness

### F094-032 — Não há non-authorization statement

### F094-033 — Box Logic e companions são incondicionais

### F094-034 — Não há semantic validator

## Final disposition

CLASSIFICATION:

Failure-semantics, retry, timeout, idempotency and degradation specialist

ACTION:

KEEP, URGENTLY CORRECT RETRY AND IDEMPOTENCY EXAMPLES, REPLACE ABSOLUTE FALLBACK/TIMEOUT RULES WITH FAILURE-CRITICALITY POLICIES, AND ADD DEADLINES/BACKPRESSURE/PARTIAL-COMPLETION MODELS

EXPECTED FINAL STATUS:

active

## Closure record

Prompt 094 was fully audited and formally closed.

Nenhum arquivo foi modificado e nenhum validador foi executado.

---

# PROMPT AUDIT REPORT 095

## Identity

AUDIT_ID:

A095-20260715-REVIEW

PROMPT:

python_security_threat_prevention.md

CANONICAL ID:

python_security_threat_prevention

DISPLAY NAME:

Python Security and Threat Prevention

SOURCE SHA-256:

1ed55f6b73fc232c4f566e03758e493053fd0dbb41e7942bed133a3a1b3d4f3c

METADATA SHA-256:

ab1701f6acd7165880cd23103b485ba4741b12c8aa3692ade49a3f6db74341b5

SOURCE SIZE:

10.600 bytes

SOURCE LENGTH:

262 linhas

SOURCE VERSION:

ausente

METADATA STATUS:

active

LOAD TYPE:

on_request

PRIORITY:

45

PROMPT CODE:

ausente

DIRECT REFERENCE SURFACES:

14 arquivos atuais

DIRECT ID OCCURRENCES:

aproximadamente 34

GENERATED MANIFEST CANONICAL PATH:

em branco

WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

## Overall verdict

Manter Prompt 095 como especialista de threat modeling, trust boundaries, secure defaults, authorization e defensive coding.

Ele necessita correção prioritária porque contém pelo menos uma API Python inexistente:

`zipfile max_volume`

A biblioteca padrão `zipfile` não fornece esse mecanismo para limitar o volume total de extração.

Também há orientações inadequadas para Windows, Pydantic, JWT, supply chain, output encoding e log injection.

## Positive findings

### P095-001 — Threat model precede controles

### P095-002 — Parameterized SQL é recomendado

### P095-003 — `eval`, `exec` e unsafe deserialization são rejeitados

### P095-004 — Least privilege é central

### P095-005 — Security-sensitive randomness usa `secrets`

### P095-006 — Password hashing não usa algoritmos rápidos

### P095-007 — File type não deve depender apenas de extensão

### P095-008 — Secrets não devem aparecer em logs

### P095-009 — Security controls precisam de testes negativos

### P095-010 — Residual risk deve ser informado

## Critical and high-severity findings

### F095-001 — A fonte não possui versão ou operational identity completa

### F095-002 — “OWASP Top 10 2021/2025” é uma referência temporal ambígua

O prompt precisa recuperar a versão atual aplicável, não combinar edições.

### F095-003 — A quota de pelo menos três threats pode fabricar riscos

Threats devem ser derivados do attack surface.

### F095-004 — O exemplo Pydantic usa API que depende da versão

`@validator` é associado ao modelo v1 e precisa ser verificado contra a versão instalada.

### F095-005 — Blacklist de caracteres em nome é incorreta

Ela:

- rejeita nomes legítimos;
- não impede ataques contextuais;
- mistura validation com output encoding.

### F095-006 — `shlex.quote()` não é solução geral para Windows

Ele segue semântica de shell POSIX e não protege automaticamente `cmd.exe` ou PowerShell.

### F095-007 — Se `shell=False`, quoting manual normalmente não deve ser aplicado

Use lista de argumentos e o contrato do subprocess.

### F095-008 — JWT guidance é simplificada demais

Faltam:

- explicit algorithm allowlist;
- issuer;
- audience;
- key rotation;
- revocation;
- replay;
- refresh-token storage;
- clock skew;
- logout semantics.

### F095-009 — HS256 e RS256 não são intercambiáveis

A escolha depende de key ownership e trust boundaries.

### F095-010 — Expiry de 15–30 minutos é arbitrária

### F095-011 — Rate-limiting libraries e package identities precisam de verificação atual

### F095-012 — O exemplo de authorization é simplista

Checar apenas owner ou admin não cobre:

- tenant;
- delegated permissions;
- object state;
- policy;
- existence disclosure;
- audit.

### F095-013 — Fernet não é solução universal de criptografia

Falta:

- key storage;
- rotation;
- backup;
- scope;
- data classification;
- envelope encryption quando aplicável.

### F095-014 — Password hashing e password-derived keys são misturados

### F095-015 — Pin exato não é universal

Aplicações e bibliotecas possuem políticas diferentes.

### F095-016 — `pip-audit --fix` é mutação automática

Não deve ser recomendada como ação normal sem revisão e autorização.

### F095-017 — `pyproject.toml` não elimina execução de build code

Build backends PEP 517 ainda podem executar código durante build.

### F095-018 — `json.dumps()` não é defesa suficiente contra XSS

Ao inserir JSON em HTML, é necessário encoding apropriado para o contexto.

### F095-019 — Structured JSON logging não elimina log injection

Untrusted control characters e viewers inseguros ainda podem criar problemas.

### F095-020 — Hashing ou truncating PII não torna automaticamente o dado seguro

### F095-021 — `zipfile max_volume` não existe

Essa é uma hallucination de API dentro do prompt de segurança.

Proteção contra ZIP bomb precisa de verificação explícita de:

- quantidade de membros;
- compressed size;
- uncompressed size;
- expansion ratio;
- cumulative extraction size;
- path containment;
- symlinks;
- disk budget.

### F095-022 — `sqlalchemy.text()` não é inerentemente vulnerável

O risco depende de concatenar input não confiável.

Bound parameters continuam seguros.

### F095-023 — Environment variables não são sempre um secrets manager

Podem vazar em:

- diagnostics;
- process inspection;
- crash dumps;
- child processes.

### F095-024 — Ferramentas e packages são estáticos

Identidade e manutenção de cada ferramenta precisam ser verificadas atualmente.

### F095-025 — Output sanitization depende do contexto

HTML, JavaScript, URL, CSS e shell possuem encodings diferentes.

### F095-026 — SSRF, path traversal e archive traversal estão incompletos

### F095-027 — Não há data-classification model

### F095-028 — Não há likelihood/impact/severity model

### F095-029 — Não há security evidence freshness

### F095-030 — Não há current-source e dependency-version binding

### F095-031 — Não há responsible-disclosure boundary

### F095-032 — O prompt mistura defensive guidance com literatura ofensiva sem explicar o limite

### F095-033 — A linha final é contaminação conversacional

A fonte termina perguntando:

“Shall I continue with the next missing prompt...?”

Isso não pertence a um prompt canônico ativo.

### F095-034 — A frase “AI-generated, for reference only” é resíduo de chat

### F095-035 — A opening statement é ruído

### F095-036 — Box Logic e companions são incondicionais

### F095-037 — Output sempre exige code e tooling

Uma security review pode ser read-only.

### F095-038 — Não há statement de que threat findings não autorizam mudança

### F095-039 — Não há prompt code ou canonical path no manifest

### F095-040 — Não há whole-prompt semantic validator

## Current owner model

Prompt 095 deve possuir:

- threat model;
- trust boundaries;
- input/output handling;
- authentication and authorization review;
- crypto applicability;
- secrets;
- supply-chain risk;
- file/archive safety;
- defensive security review.

Validation/Serialization deve possuir:

- data-model validation mechanics.

Lifecycle/Dependency owners devem possuir:

- dependency update and release policy.

Observability deve possuir:

- logging infrastructure.

Brick Wall deve possuir:

- implementation authorization.

## Recommended final structure

1. Identity and version
2. Purpose and defensive-use boundary
3. Task mode
4. Current source/dependency identity
5. Assets and trust boundaries
6. Threat scenarios
7. Severity and likelihood
8. Input and output contexts
9. Authentication/session policy
10. Authorization policy
11. Cryptography and key management
12. Secrets
13. Files, paths and archives
14. Supply-chain policy
15. Logging/privacy
16. Security validation
17. Residual risk
18. Current-doc verification
19. Non-authorization statement
20. Version history

## Final disposition

CLASSIFICATION:

Python defensive security, threat-modeling and trust-boundary specialist

ACTION:

KEEP, URGENTLY REMOVE THE NONEXISTENT ZIP API AND CHAT RESIDUE, UPDATE VERSION-SENSITIVE GUIDANCE, FIX WINDOWS COMMAND SAFETY, AND ADD SEVERITY/PROVENANCE/KEY-MANAGEMENT CONTRACTS

EXPECTED FINAL STATUS:

active

PROMPT CODE:

assign only after Class 09 identity review

FOCUSED VERIFICATION BEFORE CORRECTION:

required

## Closure record

Prompt 095 was fully audited and formally closed.

No source, metadata, security implementation, dependency, routing, validator, Project state, Error Memory, or freeze memory was modified.

No validator was executed.

No validation pass was claimed.

---

# CONSOLIDATED CHECKPOINT — PROMPTS 087–095

## Audited and closed

### 087 — anti_hallucination_master_protocol_full.md

Disposition:

Manter KPR-09-006 apenas como synthesis protocol. Remover o mega-canon e todas as responsabilidades duplicadas.

### 088 — anti_hallucination_protocol_short.md

Disposition:

Manter KPR-09-010 como perfil compacto derivado e version-bound.

### 089 — anti_hallucination_short_group.md

Disposition:

Manter KPR-09-002 como roteador compacto, com stages condicionais, admission e handoff schema.

### 090 — anti_hallucination_web_evidence_audit_full.md

Disposition:

Manter KPR-09-004 como owner de verificação externa e disconfirmation, com provenance e privacy-safe search.

### 091 — anti_hallucination_web_evidence_audit_short.md

Disposition:

Manter KPR-09-008 como perfil compacto derivado do full.

### 092 — python_documentation_developer_experience.md

Disposition:

Manter, reconciliar identidade e lifecycle, reparar Markdown e tornar ferramentas e onboarding platform-aware.

### 093 — python_observability_logging_metrics_tracing.md

Disposition:

Manter, corrigir PII/cardinality/context cleanup e tornar instrumentação proporcional ao sistema.

### 094 — python_resilience_error_handling.md

Disposition:

Manter, mas corrigir urgentemente retry, idempotency, fallback e readiness.

### 095 — python_security_threat_prevention.md

Disposition:

Manter, com correção prioritária da API inexistente de ZIP, segurança de subprocess no Windows, supply chain e resíduos de chat.

## Highest-priority corrections

1. Reduzir KPR-09-006 de 820 linhas para synthesis protocol.

2. Criar um único schema de operação para o train anti-hallucination:

   - operation_id;
   - project_id;
   - plan_hash;
   - source_snapshot;
   - stage;
   - claim_id;
   - evidence_id;
   - reviewed_at;
   - invalidation_conditions.

3. Tornar short prompts derivados ou gerados a partir dos full prompts.

4. Remover a quota de três weaknesses de full e short.

5. Definir independência real versus same-model adversarial review.

6. Tornar Web Audit privacy-safe.

7. Vincular documentação externa à versão e ao environment atual.

8. Reconciliar a identidade e lifecycle do Prompt 092.

9. Corrigir a estrutura Markdown do Prompt 092.

10. Remover request ID de metric labels no Prompt 093.

11. Corrigir contextvar cleanup no Prompt 093.

12. Corrigir o retry de HTTPStatusError no Prompt 094.

13. Substituir o exemplo de idempotency não atômico do Prompt 094.

14. Remover `zipfile max_volume` do Prompt 095.

15. Remover resíduos conversacionais do final do Prompt 095.

16. Tornar Pydantic, OpenTelemetry, security tools e resilience libraries version-verified.

17. Remover personas de experiência inventada.

18. Tornar Box Logic e delivery companions condicionais.

19. Preencher canonical paths vazios no manifest dos especialistas 092–095.

20. Criar semantic validators, não apenas asset/UI validators.

## Current anti-hallucination validator assessment

O validador:

tools/validate_anti_hallucination_prompt_groups_show_project_buttons_v1.py

protege:

- dez prompt files;
- dez prompt codes;
- status active;
- folder-card references;
- full/short routing references;
- UI labels e botões;
- cores;
- bold;
- clipboard connections;
- wrapper markers;
- cinco arquivos por grupo;
- ordem determinística;
- limite de 500 linhas nos módulos Python de UI/helper;
- py_compile dos módulos tocados.

Ele não protege:

- conteúdo semântico;
- full-short compatibility;
- evidence schema;
- operation identity;
- privacy;
- stage admission;
- stop conditions;
- forced weakness quotas;
- synthesis-versus-stage ownership;
- current API correctness;
- literature provenance;
- web provenance;
- source freshness.

O validador também utiliza vários fragmentos textuais exatos. Futuras correções devem evitar transformar explanatory prose em contrato rígido.

## Relevant Error Memory

O compact Error Memory foi suficiente.

O full Error Memory ZIP não foi aberto.

As lições diretamente relevantes para uma futura correção incluem:

- forward-contract rigidity;
- exact-phrase-count assumptions;
- package import context.

O validador atual usa `spec_from_file_location` para carregar o helper. Atualmente o helper não possui imports relativos, mas uma futura alteração pode reproduzir o erro de package context.

A validação futura deve proteger:

- identities;
- compatible minimum schema versions;
- required behaviors;
- stage ordering;
- negative cases;
- source binding;

e não frases incidentais ou uma versão exata imutável.

## Audit integrity

- Cada prompt foi aberto como alvo primário somente após o fechamento formal do anterior.
- Related prompts foram usados apenas como comparação.
- A família anti-hallucination foi avaliada como train, sem combinar os relatórios individuais.
- Prompt Library ZIP forneceu a fonte canônica on-demand.
- Source archive confirmou identidade byte a byte.
- Metadata, folder card, routing, helper de clipboard e validador focado foram inspecionados.
- Nenhum source, metadata, routing, GUI, helper, validator, dependency, Project state, Error Memory ou freeze memory foi modificado.
- Nenhum validador foi executado.
- Nenhum validation pass foi reivindicado.

## Context reliability

Context remains reliable for another adaptive cycle:

YES

## Exact next unopened prompt

096 — python_testing_pytest.md

O ciclo 087–095 está formalmente encerrado.

096- 101

next

continue

continue

Os dois prompts restantes da Classe 11 foram encerrados. As fontes canônicas e metadados usados na auditoria estão disponíveis aqui:

·

·
ADAPTIVE CYCLE RESULT — PROMPTS 107–108

Os dois prompts foram auditados sequencialmente. O Prompt 107 foi formalmente encerrado antes da abertura do Prompt 108.

Total de fonte canônica auditada:

    Prompt 107: 350 linhas

    Prompt 108: 186 linhas

    Total: 536 linhas

As cópias do Prompt Library ZIP e do source archive são byte a byte idênticas.

Nenhum arquivo foi modificado.

Nenhum validador foi executado.

Nenhum validation pass foi reivindicado.
PROMPT AUDIT REPORT 107
Identity

AUDIT_ID:

A107-20260715-REVIEW

PROMPT:

python_lifecycle_versioning_deprecation.md

METADATA CANONICAL ID:

python_lifecycle_versioning_deprecation

SOURCE-DECLARED PROMPT ID:

sustaining_python_lifecycle_versioning_deprecation_legacy_code

SOURCE AUDIT ID:

A019

DISPLAY NAME:

Python Lifecycle, Versioning, and Deprecation

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/11_productization_and_release_readiness/python_lifecycle_versioning_deprecation.md

SOURCE SHA-256:

e9ec56a99c400efe195a20ceeba868702a3aa48de0f85b83c220fad3cd0d89f4

METADATA SHA-256:

027bc4630c8bd503d3ff0ab352e40f571c5caae861f5c045e6097130ba404999

SOURCE SIZE:

13.046 bytes

SOURCE LENGTH:

350 linhas

SOURCE VERSION:

1.1

SOURCE STATUS:

audited_candidate

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

11_productization_and_release_readiness

PRIORITY:

55

PROMPT CODE:

ausente

SOURCE STAGE:

mechanically_reconciled_from_prompt_library

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

FIRST-PROMPTS STARTUP COPY:

ausente, corretamente on request

DIRECT REFERENCE SURFACES:

14 arquivos atuais

DIRECT CANONICAL-ID OCCURRENCES:

aproximadamente 32

GENERATED MANIFEST CANONICAL PATH:

em branco

ACTIVE DUPLICATE SOURCE:

não encontrado

FOCUSED WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

Manter Prompt 107 como especialista em:

    definição de superfícies públicas;

    versionamento de releases;

    compatibilidade;

    depreciação;

    períodos de suporte;

    manutenção de branches;

    comunicação de migração;

    end-of-life e sunset.

A capacidade é distinta e necessária.

O prompt atual, porém, mistura essa responsabilidade com:

    legacy-code rescue;

    dependency health;

    segurança;

    refatoração;

    feature flags;

    data migrations;

    API design;

    testing;

    documentation.

Também trata Semantic Versioning como política universal para todo software Python, embora o ecossistema de distribuição Python use as regras de versão do PEP 440. SemVer exige que a public API seja declarada; sem esse inventário, decidir MAJOR, MINOR ou PATCH torna-se subjetivo.

Deve permanecer ativo, mas substancialmente modernizado e com ownership reduzido.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

Prompt 107 deve possuir:

    seleção da política de versionamento;

    inventário da public compatibility surface;

    classificação da mudança;

    deprecation contract;

    migration path;

    support window;

    LTS e maintenance branches;

    release notes e changelog policy;

    sunset e end-of-life;

    communication plan;

    compatibility evidence;

    emergency-breaking-change exception;

    remoção programada de compatibility layers.

Não deve possuir:

    refatoração de legacy code;

    dependency implementation;

    database migration mechanics;

    feature-flag implementation;

    API endpoint design;

    security remediation;

    source-write authorization;

    release packaging e instalação.

Positive findings
P107-001 — Compatibilidade é tratada como contrato com usuários
P107-002 — Depreciação deve fornecer alternativa
P107-003 — Removal version é explicitamente comunicada
P107-004 — Adapter layers são reconhecidas como mecanismo de transição
P107-005 — Changelog e migration guide são considerados parte da mudança
P107-006 — Maintenance branches são reconhecidas
P107-007 — Dependency abandonment é considerado risco de longo prazo
P107-008 — Data migrations são reconhecidas como mais difíceis de reverter do que código
P107-009 — Uso de features depreciadas deve ser monitorado quando possível
P107-010 — O prompt tenta diferenciar depreciação, remoção e version bump
Critical and high-severity findings
F107-001 — Canonical identity é inconsistente

Source:

sustaining_python_lifecycle_versioning_deprecation_legacy_code

Metadata e routing:

python_lifecycle_versioning_deprecation

O ID A019 também permanece dentro da fonte operacional.
F107-002 — Lifecycle é inconsistente

Source:

audited_candidate

Metadata:

active
F107-003 — A versão 1.1 não está ligada a um schema ou compatibility contract
F107-004 — A persona de 15+ anos deve ser removida

A capacidade deve ser definida por método e evidência, não experiência pessoal inventada.
F107-005 — Os code blocks estão malformados

Linhas isoladas como:

    python

    toml

não abrem fenced code blocks válidos.
F107-006 — SemVer é tratado como regra obrigatória

SemVer é apropriado quando o projeto decide adotá-lo e define precisamente sua public API. Projetos Python também precisam produzir versões válidas segundo o padrão de distribuição do ecossistema, PEP 440.

O prompt deve primeiro selecionar entre:

    SemVer;

    CalVer;

    release train;

    internal build version;

    application release;

    package distribution version;

    protocol/schema version.

F107-007 — A public API não é inventariada

Compatibilidade pode incluir:

    Python imports;

    function signatures;

    subclass behavior;

    exceptions;

    CLI options;

    configuration keys;

    environment variables;

    HTTP contracts;

    file formats;

    database schemas;

    plugin interfaces;

    emitted events;

    command output;

    operational behavior.

Sem esse inventário, MAJOR/MINOR/PATCH não é verificável.
F107-008 — “Start at 0.1.0” não é uma obrigação do SemVer

Major version zero representa desenvolvimento inicial e API não estável, mas a versão inicial específica é uma escolha do projeto.
F107-009 — “0.x = anything can break” pode ser interpretado de forma abusiva

SemVer permite mudanças durante 0.y.z, mas isso não elimina:

    documentação;

    release notes;

    dependency constraints;

    comunicação;

    project-specific compatibility promises.

F107-010 — Há risco de duas fontes de versão

O exemplo mostra simultaneamente:

    __version__ = "1.2.0"

    importlib.metadata.version(...).

A orientação atual de packaging favorece single-sourcing e, quando ambos existem, recomenda verificar que permaneçam alinhados.
F107-011 — importlib.metadata.version() usa distribution identity

O nome da distribution pode não ser igual ao nome do import package, e a metadata pode não existir quando o source é executado sem instalação.
F107-012 — O período mínimo de depreciação é universalizado

“At least one MINOR release” e “often 6–12 months” não servem para todos os projetos.

A política depende de:

    release cadence;

    user population;

    criticality;

    contractual support;

    security risk;

    replacement availability;

    cost of migration.

A política do próprio CPython, por exemplo, usa um período diferente e mais longo, demonstrando que não há uma única janela universal.
F107-013 — DeprecationWarning pode não chegar ao público pretendido

DeprecationWarning é ignorada por padrão na maioria dos módulos. Para depreciações direcionadas aos usuários finais de aplicações, FutureWarning pode ser mais apropriada.
F107-014 — Depreciação está limitada a runtime warnings

O prompt não considera:

    static deprecation metadata;

    documentation warnings;

    type-checker deprecation;

    release notes;

    telemetry;

    package metadata;

    IDE surfacing.

PEP 702 criou uma forma de expressar depreciações ao type system, que deve ser considerada quando compatível com o runtime e toolchain do projeto.
F107-015 — A biblioteca deprecation é recomendada sem current verification

O projeto pode preferir:

    standard warnings;

    typing deprecation;

    framework-native facilities;

    custom compatibility wrapper.

F107-016 — Adicionar parâmetro opcional não é sempre backward-compatible

Pode quebrar:

    subclasses com overrides incompatíveis;

    wrappers;

    reflection;

    positional-call assumptions;

    generated clients;

    callables constrained por Protocol.

F107-017 — int → float não é automaticamente compatível

Mudanças de type contract podem alterar:

    precision;

    serialization;

    generated schemas;

    comparison;

    consumer validation;

    overload selection.

F107-018 — Loosening validation também pode ser breaking

Pode permitir estados antes impossíveis e quebrar consumidores que assumem invariantes mais fortes.
F107-019 — Mudança de exception type não é universalmente incompatível

Depende de:

    inheritance;

    documented exception contract;

    consumer behavior;

    catch hierarchy;

    observability requirements.

F107-020 — O prompt não distingue source compatibility de behavioral compatibility

Uma assinatura pode continuar igual enquanto o comportamento observável muda.
F107-021 — Não há policy para security-driven breaking changes

Pode ser necessário remover ou desativar imediatamente uma API insegura.

O prompt precisa permitir:

    emergency removal;

    compensating communication;

    security advisory;

    temporary compatibility shim quando seguro;

    explicitly accepted break.

F107-022 — “Last release <1 year” é um indicador fraco de manutenção

Bibliotecas estáveis podem não precisar de releases frequentes.

Projetos com releases recentes podem estar abandonados ou comprometidos.
F107-023 — Dependabot e Renovate não são detectores completos de abandono

Eles ajudam a identificar novas versões e atualizações, mas não substituem uma avaliação de:

    maintainer activity;

    security advisories;

    repository status;

    governance;

    release provenance;

    ecosystem adoption;

    bus factor.

F107-024 — “Fork and maintain” como primeira preferência é inadequado

Forking transfere ao projeto:

    manutenção;

    security response;

    release engineering;

    licença;

    vulnerability tracking;

    long-term compatibility.

Replace ou remove podem ser alternativas superiores.
F107-025 — Vendoring é classificado como low effort

Vendoring pode ser simples inicialmente, mas transfere manutenção e obrigações de licença.
F107-026 — Legacy-code rescue invade Prompt 078

Prompt 107 deve possuir lifecycle de suporte e remoção.

Prompt 078 deve possuir:

    characterization;

    seams;

    legacy stabilization;

    safe incremental rescue.

F107-027 — “Legacy code is code without tests” é usado como definição operacional total

A frase de Feathers é útil como lente, mas código pode ser legacy-risk mesmo com testes inadequados, incompletos ou sem documentação dos contratos reais.
F107-028 — “Big bang rewrite always fails” é absoluto

Rewrites podem ser justificadas quando:

    o sistema é pequeno;

    o comportamento pode ser reespecificado;

    não há migração incremental possível;

    o custo de manter a base excede o de substituí-la;

    há parallel-run e rollback adequados.

F107-029 — Arquivo com mais de 2.000 linhas não é automaticamente legacy
F107-030 — Ausência de type hints não prova dívida crítica
F107-031 — TYPE_CHECKING não é solução geral para circular imports

Pode ocultar parte do ciclo de typing, mas não corrige necessariamente runtime ownership ou dependency direction.
F107-032 — Data-migration mechanics invadem Prompt 102

O lifecycle prompt deve definir:

    compatibility window;

    old/new version coexistence;

    support and removal timing.

Prompt 102 deve definir:

    DDL;

    backfill;

    locking;

    consistency;

    rollback/forward-repair mechanics.

F107-033 — O migration table simplifica rollback indevidamente

Exemplos:

    drop da nova coluna pode perder dados já escritos;

    reverter backfill para NULL pode não restaurar o estado anterior;

    dual write pode divergir;

    backup restore pode ser operacionalmente inviável.

F107-034 — “Never rename a column in one step” é absoluto

A segurança depende do engine, consumidores, lock behavior, deployment order e compatibility requirements.
F107-035 — “Every feature and API should have an expected lifetime” é excessivo

Core features podem ser intencionalmente permanentes, embora continuem sujeitas a revisão.
F107-036 — O exemplo de endpoint é contraditório

O comentário diz “Redirect to new endpoint”, mas o código retorna HTTP 410 Gone.

Um 410 informa remoção; não é redirecionamento.
F107-037 — A política de duas MINOR versions é arbitrária

Support windows devem ser publicadas por branch ou release line.
F107-038 — O upper bound <3.13 é um exemplo perigoso

Bloquear futuras versões de Python sem incompatibilidade comprovada pode impedir instalações válidas.

O intervalo deve refletir suporte testado e política explícita.
F107-039 — Runtime version detection não deve substituir capability detection

Comportamento condicional baseado apenas na versão instalada pode ser frágil quando:

    forks existem;

    backports são usados;

    feature detection é possível;

    distributions e import packages não coincidem.

F107-040 — Remover feature flags após duas releases é arbitrário

O owner de configuração deve registrar:

    flag type;

    expiry;

    owner;

    removal condition;

    permanent/temporary status.

F107-041 — A saída obrigatória sempre exige código

Uma tarefa de lifecycle pode ser apenas:

    policy design;

    compatibility review;

    release classification;

    deprecation communication;

    EOL plan.

F107-042 — A opening statement é ruído

Também contém “I follow SemVer religiously”, linguagem incompatível com avaliação contextual.
F107-043 — Box Logic é carregada incondicionalmente

Uma pergunta sobre política de versão não exige owner-path audit antes de qualquer resposta.
F107-044 — Os companions são inadequados

A metadata exige sempre:

    professional_ai_assisted_engineering_framework;

    evidence_freshness_gate.

O Prompt 105 acabou de ser classificado como mega-framework a deprecar.

Evidence Freshness só é necessária quando a decisão depende de source ou artifacts atuais.
F107-045 — Routing aliases são excessivamente amplos

Aliases como:

    operations;

    product;

    release;

podem carregar o prompt quando lifecycle não é o problema central.
F107-046 — O generated manifest possui canonical path vazio
F107-047 — Não existe whole-prompt semantic validator
Current owner model

Prompt 107 deve possuir:

    public compatibility surface;

    versioning policy;

    release classification;

    deprecation;

    migration communication;

    support windows;

    EOL;

    maintenance branches.

Prompt 078 deve possuir:

    legacy rescue.

Prompt 101 deve possuir:

    feature-flag lifecycle.

Prompt 102 deve possuir:

    data migration execution.

Prompt 099 deve possuir:

    API contract.

Prompt 095 deve possuir:

    security-driven deprecation risk.

Prompt 092 deve possuir:

    documentation mechanics.

Release Delivery deve possuir:

    packaging and publication.

Recommended final structure

    Identity and semantic version

    Purpose

    Product and distribution profile

    Version-policy selection

    Public compatibility-surface inventory

    Change classification

    Deprecation channels

    Deprecation duration policy

    Migration path

    Support branches and LTS

    Security and emergency exceptions

    Data/API/config compatibility handoffs

    EOL and sunset

    Release communication

    Compatibility evidence

    Non-authorization statement

    Version history

Final disposition

CLASSIFICATION:

Python release lifecycle, compatibility, deprecation and end-of-life specialist

ACTION:

KEEP, RECONCILE IDENTITY/LIFECYCLE, DISTINGUISH SEMVER FROM PYTHON PACKAGING VERSION RULES, REMOVE LEGACY/DATABASE OWNERSHIP, AND ADD PUBLIC-SURFACE AND EMERGENCY-BREAK CONTRACTS

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_legacy_identity_semver_universalism_compatibility_misclassifications_and_cross_specialist_scope_sprawl

EXPECTED FINAL STATUS:

active

FINAL LOAD TYPE:

on_request when compatibility, version policy, deprecation, support or EOL is central

PROMPT CODE:

assign only after Class 11 reconciliation

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 107 was fully audited and formally closed.

No prompt source, metadata, package version, API, migration, dependency, routing, validator, Project state, Error Memory or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
PROMPT AUDIT REPORT 108
Identity

AUDIT_ID:

A108-20260715-REVIEW

PROMPT:

python_site_reliability_engineering.md

METADATA CANONICAL ID:

python_site_reliability_engineering

SOURCE-DECLARED PROMPT ID:

A025

SOURCE PROMPT NAME:

Site Reliability Engineering (SRE) for Python

DISPLAY NAME:

Python Site Reliability Engineering

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/11_productization_and_release_readiness/python_site_reliability_engineering.md

SOURCE SHA-256:

cc2390f9a9959d214168e0205a40894b0f712c6378c0dd603f729b4d09e53dee

METADATA SHA-256:

616dd878707b0a266a8b41fa2789219f427d33cf96341702bb7512f5d2fb1da3

SOURCE SIZE:

13.252 bytes

SOURCE LENGTH:

186 linhas

SOURCE VERSION:

audited-v1.0

SOURCE STATUS:

audited_candidate_after_update

METADATA STATUS:

active

LOAD TYPE:

on_request

CATEGORY:

11_productization_and_release_readiness

PRIORITY:

55

PROMPT CODE:

ausente

SOURCE STAGE:

mechanically_reconciled_from_prompt_library

CURRENT PROMPT-LIBRARY COPY:

presente

SOURCE-ARCHIVE COPY:

presente e byte a byte idêntica

FIRST-PROMPTS STARTUP COPY:

ausente, corretamente on request

DIRECT REFERENCE SURFACES:

14 arquivos atuais

DIRECT CANONICAL-ID OCCURRENCES:

aproximadamente 26

GENERATED MANIFEST CANONICAL PATH:

em branco

ACTIVE DUPLICATE SOURCE:

não encontrado

FOCUSED WHOLE-PROMPT SEMANTIC VALIDATOR:

não encontrado

ENCODING:

UTF-8, LF, sem BOM
Overall verdict

Manter Prompt 108 como especialista em governança de confiabilidade para serviços operacionais.

Sua capacidade central é válida:

    seleção de SLIs;

    definição de SLOs;

    error-budget policy;

    incident management;

    toil assessment;

    capacity planning;

    operational readiness;

    progressive rollout;

    on-call and runbook requirements.

O prompt atual, entretanto, transforma práticas do modelo Google SRE em regras universais para qualquer sistema Python.

Também contém erros técnicos concretos:

    trata k6 como ferramenta Python;

    apresenta Bottleneck como profiler;

    usa uma fórmula de error budget incorreta;

    confunde status page com health endpoints;

    transforma concurrency limit, observability e deployment tooling em obrigações universais.

k6 usa scripts em JavaScript ou TypeScript, não Python. O pacote Bottleneck é uma biblioteca de funções NumPy aceleradas, não um profiler de aplicação.

Deve permanecer, mas com foco em governança SRE e delegação rigorosa aos especialistas adjacentes.
Unique capability assessment

UNIQUE ACTIVE CAPABILITY:

sim

Prompt 108 deve possuir:

    service criticality profile;

    user journey and SLI selection;

    SLO and error-budget policy;

    reliability decision gates;

    incident severity and response model;

    post-incident learning;

    toil measurement;

    capacity and overload readiness;

    launch-readiness assessment;

    operational ownership;

    on-call sustainability requirements;

    reliability evidence.

Não deve possuir:

    instrumentation implementation detalhada;

    retry/circuit-breaker code;

    Kubernetes manifests;

    profiling implementation;

    feature-flag middleware;

    CI/CD pipeline;

    alerting vendor configuration universal;

    production mutation authorization.

Positive findings
P108-001 — SLI, SLO e error budget são diferenciados
P108-002 — Reliability é tratada como objetivo mensurável
P108-003 — O prompt rejeita 100% como objetivo padrão
P108-004 — Error budget conecta confiabilidade e velocidade de mudança
P108-005 — Toil é reconhecido como custo operacional
P108-006 — Pages devem exigir ação humana
P108-007 — Alert fatigue é tratada como risco
P108-008 — Postmortems devem gerar action items com owner
P108-009 — Capacity planning e load testing fazem parte da readiness
P108-010 — Chaos engineering exige observability e rollback
P108-011 — Progressive rollout é reconhecido
P108-012 — O prompt possui ownership boundary explícito com Observability, Resilience, Deployment, Performance e Peopleware
Critical and high-severity findings
F108-001 — Canonical identity é inválida na fonte

Source:

A025

Metadata e routing:

python_site_reliability_engineering
F108-002 — Lifecycle é inconsistente

Source:

audited_candidate_after_update

Metadata:

active
F108-003 — audited-v1.0 não é uma semantic version operacional clara
F108-004 — A persona de 15+ anos deve ser removida
F108-005 — O escopo “Python systems” é amplo demais

SRE é mais diretamente aplicável a:

    long-running services;

    production platforms;

    distributed systems;

    operationally owned pipelines.

Um pacote Python, script local ou aplicativo desktop pode não exigir:

    SLO;

    error budget;

    on-call;

    canary;

    chaos engineering.

F108-006 — “Reliability is the most important feature” é absoluto

Reliability precisa ser balanceada com:

    safety;

    security;

    correctness;

    privacy;

    legal obligations;

    product value;

    cost.

F108-007 — SLI selection não começa pelo user journey

O Google SRE recomenda escolher medidas que representem o nível de serviço relevante ao usuário; métricas de servidor podem ser apenas proxies.

O prompt deveria iniciar por:

    user journey;

    valid event;

    good event;

    total event;

    measurement point;

    window;

    exclusions.

F108-008 — error budget = 1 – SLO é válido apenas em modelos simples

A expressão pode representar a fração permitida de bad events para um availability SLO binário.

Não define de forma geral budgets para:

    latency distributions;

    durability;

    freshness;

    composite SLIs;

    multi-window objectives.

F108-009 — Error budget não é crédito para realizar mudanças arriscadas

É uma medida de unreliability tolerada e uma entrada para uma política previamente acordada.
F108-010 — Freeze automático ao esgotar budget não é universal

Uma error-budget policy deve ser acordada entre os owners e pode conter exceções, prioridades e medidas diferentes. A própria orientação do Google descreve feature freezes como uma política negociada, não uma consequência automática de qualquer SLO breach.
F108-011 — “Healthy = well below 0.1% errors” confunde conceitos

Um serviço com SLO 99% possui budget diferente de um serviço com SLO 99.99%.

Saúde deve ser medida por consumption e burn rate relativos ao objetivo.
F108-012 — A meta de 30% de toil não possui base no texto citado

O modelo Google usa 50% como limite máximo de trabalho operacional para suas equipes SRE, garantindo pelo menos 50% para engineering. Isso é uma prática organizacional específica, não um threshold universal para qualquer equipe.
F108-013 — “Automate after doing a manual task twice” é perigoso

Automação deve considerar:

    frequency;

    cost;

    failure impact;

    permissions;

    observability;

    rollback;

    maintenance burden;

    security.

F108-014 — Auto-remediation é apresentada sem guardrails

Reiniciar, escalar ou alterar recursos automaticamente pode:

    ocultar root symptoms;

    gerar loops;

    amplificar incidentes;

    consumir budget;

    causar data loss.

F108-015 — A seção Observability invade Prompt 093

SRE deve definir quais sinais são necessários para decisões.

Prompt 093 deve implementar:

    metrics;

    logs;

    traces;

    correlation;

    cardinality;

    retention.

F108-016 — “Three pillars” é usado como definição completa de observability

Events, profiles, continuous diagnostics e domain-specific evidence também podem ser relevantes.
F108-017 — “Every production service” precisa de RED, resources e business SLIs é absoluto

A seleção depende do workload:

    queue worker;

    batch pipeline;

    storage service;

    scheduled job;

    stream processor;

    user-facing API.

F108-018 — “No dashboards without alerts” é incorreto

Dashboards podem ser úteis para:

    exploration;

    capacity;

    incident analysis;

    trends;

    release comparison;

    business monitoring;

sem exigir alert para cada visualização.
F108-019 — “Alert only on symptoms, never causes” é absoluto

User-visible symptoms devem orientar paging, mas infraestrutura crítica como:

    certificate expiry;

    disk exhaustion;

    quorum loss;

    replication lag;

    backup failure

pode justificar ação direta antes de impacto visível.
F108-020 — Todo incidente não precisa de postmortem formal

A exigência deve depender de:

    severity;

    impact;

    novelty;

    repeated failure;

    learning value;

    regulatory requirement.

F108-021 — “Root cause” singular é simplista

Incidentes complexos frequentemente possuem múltiplos contributing factors e condições sistêmicas.
F108-022 — Armazenar todo postmortem em version control pode vazar dados

Postmortems podem conter:

    customer information;

    security details;

    credentials;

    employee information;

    legal analysis;

    incident evidence.

Precisam de classification, access control e retention.
F108-023 — Headroom de 20–30% é arbitrário

Capacity reserve depende de:

    traffic volatility;

    scaling latency;

    failure domains;

    recovery target;

    cost;

    dependency limits;

    seasonality.

F108-024 — k6 está classificado como ferramenta Python

k6 executa scripts em JavaScript ou TypeScript.
F108-025 — bottleneck está classificado como profiler

O projeto Bottleneck fornece funções NumPy aceleradas em C. Não substitui py-spy, sampling profiler ou application profiler.
F108-026 — Load testing em todo CI/CD é uma regra excessiva

Large load tests podem ser:

    caros;

    noisy;

    environment-dependent;

    disruptive;

    inadequados para cada commit.

A estratégia deve combinar:

    lightweight performance checks;

    scheduled tests;

    pre-release runs;

    isolated capacity tests.

F108-027 — Chaos engineering é apresentado como random failure injection

Uma prática madura começa com:

    hipótese;

    steady-state definition;

    controlled variable;

    blast-radius limit;

    abort condition;

    observability;

    explicit authorization.

Os princípios publicados de Chaos Engineering destacam a necessidade de minimizar e conter o blast radius.
F108-028 — “Start with Chaos Monkey style” é inadequado como default

Desabilitar aleatoriamente um serviço não crítico pode não testar uma hipótese relevante.
F108-029 — Custom scripts que chamam cloud APIs são apresentados sem security boundary

Faltam:

    least privilege;

    target allowlist;

    environment protection;

    audit log;

    rate limit;

    dry run;

    two-person approval;

    abort mechanism.

F108-030 — Toda mudança pequena não precisa de canary

Canary é apropriado quando:

    deployment infrastructure suporta;

    métricas discriminam cohorts;

    rollback é possível;

    blast radius pode ser reduzido.

F108-031 — Rollback drill trimestral é arbitrário

A frequência depende de:

    release cadence;

    criticality;

    operator turnover;

    recovery objectives;

    regulation.

F108-032 — A fórmula de error budget tracking está matematicamente incorreta

A tabela mostra:

(100 - (success_rate / target_success)) * 100

Essa expressão não representa corretamente burn rate nem percent budget consumed.

A abordagem deve derivar:

    allowed bad-event ratio;

    observed bad-event ratio;

    burn rate;

    measurement window.

A orientação do SRE Workbook usa burn rates e múltiplas janelas; os valores sugeridos são pontos iniciais dependentes do serviço, não uma fórmula universal.
F108-033 — A regra fixa “5% em uma hora → page” diverge da própria referência

O SRE Workbook fornece exemplos de 2% em uma hora e 5% em seis horas como pontos iniciais, com multiwindow/multi-burn-rate alerting. Os valores precisam ser ajustados ao serviço.
F108-034 — Status page é confundida com health endpoints

Endpoints /health, /ready e /live atendem máquinas e orquestradores.

Uma status page comunica estado e incidentes a usuários externos ou internos.
F108-035 — O toolkit mistura products, standards e implementation choices

Exemplos:

    PagerDuty;

    Opsgenie;

    Slack;

    Jaeger;

    Flagger;

    Argo Rollouts;

    Chaos Toolkit.

A disponibilidade, manutenção e adequação atual precisam ser verificadas antes de recomendação.
F108-036 — Auto-remediation é exigida para processos repetidos

Alguns processos devem permanecer manuais por:

    security;

    safety;

    approval;

    low frequency;

    ambiguous diagnosis;

    high blast radius.

F108-037 — Runbooks manuais são tratados como anti-pattern

Um runbook manual bem definido pode ser o primeiro controle seguro antes de uma automação confiável.
F108-038 — O prompt não possui incident-severity model

Faltam:

    severity;

    commander;

    communications lead;

    operations lead;

    escalation;

    stakeholder notification;

    resolution criteria.

F108-039 — Não há service ownership record

Antes de definir SLOs, faltam:

    service owner;

    user population;

    critical journeys;

    dependency map;

    business hours;

    on-call model;

    regulatory constraints.

F108-040 — Não há low-traffic SLO treatment

Percentuais e burn rates podem comportar-se mal em serviços de baixo volume.
F108-041 — Não há dependency SLO model

Uma equipe pode não controlar integralmente a confiabilidade de seus downstreams.
F108-042 — Não há capacity failure-domain model

CPU e memória não são suficientes.

Também importam:

    database connections;

    queues;

    storage;

    quotas;

    zones;

    regions;

    third-party limits;

    operator capacity.

F108-043 — A saída obrigatória é excessiva

Toda resposta exige:

    SLO;

    instrumentation code;

    PromQL;

    automation;

    runbook;

    load/chaos test;

    rollback.

Uma tarefa pode ser apenas:

    incident review;

    SLO critique;

    toil assessment;

    capacity-plan review;

    on-call policy.

F108-044 — Não há task modes

Deveria distinguir:

    SRE_EDUCATION;

    SERVICE_READINESS_REVIEW;

    SLO_DESIGN;

    INCIDENT_REVIEW;

    TOIL_AUDIT;

    CAPACITY_PLAN;

    ROLLOUT_POLICY;

    AUTHORIZED_IMPLEMENTATION.

F108-045 — Não há truthful evidence states

O prompt não diferencia:

    metric proposed;

    metric instrumented;

    data observed;

    SLO approved;

    alert configured;

    alert tested;

    rollback rehearsed;

    chaos experiment executed.

F108-046 — A opening statement é ruído

Ela promete comportamentos e implementações antes de analisar o serviço.
F108-047 — Box Logic é carregada incondicionalmente

Uma explicação sobre SLOs não exige source owner paths.
F108-048 — Required companions são inadequados

A metadata exige:

    professional_ai_assisted_engineering_framework;

    evidence_freshness_gate.

Prompt 105 foi classificado como mega-framework a deprecar.

Evidence Freshness só é necessária quando a review depende de artifacts atuais.
F108-049 — Routing aliases são excessivamente amplos

Aliases como:

    engineering;

    operations;

    product;

    release;

    site;

podem selecionar o prompt para tarefas que não envolvem SRE.
F108-050 — O generated manifest possui canonical path vazio
F108-051 — Não há whole-prompt semantic validator
Current owner model

Prompt 108 deve possuir:

    reliability objectives;

    error-budget policy;

    incident governance;

    toil;

    capacity;

    operational readiness;

    service ownership;

    launch reliability decisions.

Prompt 093 deve possuir:

    telemetry implementation.

Prompt 094 deve possuir:

    timeout, retry, idempotency and degradation.

Prompt 103 deve possuir:

    Kubernetes deployment and rollout mechanics.

Prompt 077 deve possuir:

    profiling and benchmark methods.

Prompt 096 deve possuir:

    reliability test mechanics.

Peopleware deve possuir:

    burnout and team-health policies.

Security must own:

    privileged automation and incident confidentiality.

Recommended final structure

    Identity and semantic version

    Purpose and supported service profiles

    Task mode

    Service and owner identity

    Critical user journeys

    SLI definitions

    SLO approval

    Error-budget calculation

    Error-budget policy

    Alert and page policy

    Incident severity and response

    Post-incident learning

    Toil inventory and automation admission

    Capacity and overload planning

    Progressive rollout readiness

    Chaos experiment admission

    Reliability evidence states

    Specialist handoffs

    Non-authorization statement

    Version history

Final disposition

CLASSIFICATION:

Production-service reliability governance, SLO, incident and operational-readiness specialist

ACTION:

KEEP, RECONCILE IDENTITY/LIFECYCLE, CORRECT THE ERROR-BUDGET FORMULA AND TOOLKIT, MAKE GOOGLE SRE PRACTICES CONTEXTUAL, AND DELEGATE IMPLEMENTATION TO OBSERVABILITY/RESILIENCE/DEPLOYMENT OWNERS

DELETE:

no

DEPRECATE:

no

CURRENT AUDIT STATUS:

active_with_legacy_identity_incorrect_error_budget_formula_tool_misclassification_and_universalized_google_sre_practices

EXPECTED FINAL STATUS:

active

FINAL LOAD TYPE:

on_request only for operationally owned production services or reliability governance

PROMPT CODE:

assign only after Class 11 reconciliation

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure record

Prompt 108 was fully audited and formally closed.

No prompt source, metadata, service, SLO, alert, incident record, infrastructure, routing, validator, Project state, Error Memory or freeze memory was modified.

No validator was executed.

No validation pass was claimed.
CONSOLIDATED CHECKPOINT — PROMPTS 107–108
Audited and closed
107 — python_lifecycle_versioning_deprecation.md

Disposition:

Manter como owner de compatibility lifecycle, deprecation, support e EOL.

Remover:

    legacy-code rescue;

    database-migration mechanics;

    universal SemVer;

    arbitrary deprecation windows;

    compatibility generalizations.

108 — python_site_reliability_engineering.md

Disposition:

Manter como owner de SLOs, error budgets, incident governance, toil e operational readiness.

Corrigir:

    error-budget formula;

    k6 classification;

    Bottleneck classification;

    universal toil/headroom/rollout rules;

    forced instrumentation output.

Class 11 final reconciliation
Keep as active specialists after correction

    Kubernetes Deployment and Operations

    Python Lifecycle, Versioning, and Deprecation

    Python Site Reliability Engineering

Remove from global active routing or reduce radically

    Productization Readiness Roadmap

    Professional AI-Assisted Engineering Framework

    Professional Infrastructure Roadmap

Current recommended Class 11 model
Kubernetes

Owns deployment/runtime mechanics.
Lifecycle

Owns release compatibility and deprecation.
SRE

Owns reliability targets and operational governance.
Project-specific readiness

Must reside in Project Support or a project overlay.
AI-human operating model

May survive only as a thin non-authoritative overview.
Historical infrastructure roadmap

Must remain historical provenance, not implementation instruction.
Highest-priority corrections

    Reconcile source IDs with metadata IDs.

    Reconcile candidate versus active lifecycle.

    Remove audit IDs from operational identity.

    Repair malformed code fences.

    Separate PEP 440 package versions from optional SemVer policy.

    Add public compatibility-surface inventory.

    Correct deprecation-warning visibility.

    Add emergency security-break policy.

    Remove legacy-code ownership from Prompt 107.

    Correct the Prompt 108 error-budget formula.

    Correct k6 and Bottleneck classifications.

    Replace fixed SRE thresholds with service-specific policies.

    Add service profile and ownership record.

    Add incident severity and confidentiality controls.

    Make Box Logic conditional.

    Remove the deprecated Professional Framework as required companion.

    Make Evidence Freshness conditional.

    Narrow routing aliases.

    Fill canonical paths in the generated manifest.

    Add semantic validators focused on durable ownership and safety.

Relevant Error Memory

O compact Error Memory foi suficiente.

O full Error Memory ZIP não foi aberto.

As lições mais relevantes continuam sendo:

    validator forward-contract rigidity;

    exact-version rigidity;

    exact-phrase-count assumptions;

    canonical package import context.

Future validators should protect:

    canonical prompt identity;

    supported minimum schema version;

    owner boundaries;

    negative routing;

    absence of unsafe universal claims;

    truthful evidence states;

    compatibility with later stronger contracts.

They should not freeze:

    explanatory wording;

    one exact release version;

    one exact deprecation period;

    one exact SLO threshold;

    one tool vendor.

Audit integrity

    Prompt 107 was fully closed before Prompt 108 was opened.

    Prompt Library ZIP provided the canonical sources.

    Source archive confirmed byte-for-byte identity.

    Metadata, folder card, navigation, group registration and generated manifest were inspected.

    Current official documentation was used only to verify version-sensitive technical claims.

    No prompt, metadata, routing, application source, validator, Project state, Error Memory or freeze memory was modified.

    No validator was executed.

    No validation pass was claimed.

Context reliability

Context remains reliable for another adaptive cycle:

YES

A Classe 11 está encerrada.

O próximo ciclo inicia a Classe 12, Generalized Project Canons.

Um lote inicial seguro provavelmente será 109–111, porque são canons curtos e conceitualmente próximos:

    data transformation invariants;

    desktop help-document layout;

    domain decision tables.

Exact next unopened prompt

109 — data_transform_pipeline_invariants.md

O ciclo 107–108 e a Classe 11 estão formalmente encerrados.

continue

next

do you need the chats with all  prompts audited?

Yes. For a reliable audit-ledger reconciliation, I need the chats containing the completed prompt audits—or one consolidated file containing the same information.

The essential data is:

    Exact prompt filename for every completed primary audit

    Audit range or sequence used

    Final disposition and closure statement

    Any prompts only referenced, but not formally audited

    The exact next unopened prompt recorded at each checkpoint

I do not need the startup packs or canonical prompt sources again unless a source changed. The best upload would be one .md, .txt, or ZIP containing all audit chats from Prompt 001 onward. I can then build a definitive table marking every canonical prompt as AUDITED, NOT AUDITED, REFERENCED ONLY, HISTORICAL/DUPLICATE, or IDENTITY UNRESOLVED.

000 HOW TO(2).md
File
chat 001-011(1).md
File
chat 041-055(1).md
File
chat 012-040(2).md
File
chat 056-075(1).md
File
data_transform_pipeline_invariants(1).md
File
data_transform_pipeline_invariants.meta(1).json
File
desktop_help_document_layout_canon(1).md
File
desktop_help_document_layout_canon.meta(1).json
File
domain_decision_table_template(1).md
File
domain_decision_table_template.meta(1).json
File

Recebi os arquivos. A reconciliação do ledger está concluída segundo o protocolo sequencial fornecido.
AUDIT LEDGER RECONCILIATION — 118 PROMPTS CANÔNICOS
Resultado
Estado	Quantidade
Prompts canônicos formalmente auditados	113
Prompts canônicos ainda não auditados	5
Prompt adicional auditado fora do inventário de 118	1
Total de relatórios primários identificados	114

O inventário canônico contém 118 prompts distribuídos em 12 classes.
Cobertura confirmada
Classes 01–11

Todos os 107 prompts canônicos das Classes 01–11 possuem fechamento primário registrado.

Os históricos enviados confirmam diretamente:

    Prompts 001–011;

    continuidade e checkpoints de 012–040;

    Prompts 041–055;

    Prompts 056–075.

Os fechamentos 076–108 permanecem registrados nesta conversa atual.
Classe 12 já auditada

Os seguintes seis prompts canônicos da Classe 12 já receberam relatório e encerramento primário:

    data_transform_pipeline_invariants.md

    desktop_help_document_layout_canon.md

    domain_decision_table_template.md

    plugin_package_import_canon.md

    shared_visual_render_engine_canon.md

    transform_resolver_architecture_contract.md

As três primeiras fontes também foram reenviadas individualmente nesta etapa.
Cinco prompts canônicos ainda não auditados

Na ordem do inventário canônico:

    architecture_review_project_card_machine_canon.md — KPR-12-005

    error_memory_active_ready_correction_blueprint.md — KPR-12-002

    error_memory_active_ready_json_template.md — KPR-12-003

    error_memory_model_template.md — KPR-12-004

    project_tool_boundary_canon.md — KPR-12-001

Esses são os únicos cinco itens do inventário de 118 que não possuem fechamento primário identificado.
Causa da divergência numérica

O número sequencial da auditoria deixou de coincidir com a posição no inventário canônico porque:
Prompt adicional inserido

O relatório A039 auditou:

governed_architecture_companion_handoff.md

Esse arquivo não aparece no inventário canônico de 118 prompts.

Por isso, a partir desse ponto, a numeração de auditoria ficou uma posição à frente do inventário.
Primeiro prompt canônico posteriormente ignorado

Após o encerramento do Prompt 108, a sequência abriu diretamente:

data_transform_pipeline_invariants.md

O item anterior na Classe 12:

architecture_review_project_card_machine_canon.md

não foi auditado como alvo primário.
Outros saltos na Classe 12

Depois de domain_decision_table_template.md, a auditoria saltou diretamente para:

plugin_package_import_canon.md

Isso deixou sem auditoria os três prompts de Error Memory.

Depois de plugin_package_import_canon.md, a auditoria abriu:

shared_visual_render_engine_canon.md

Isso deixou sem auditoria:

project_tool_boundary_canon.md
Prompt adicional fora do inventário
governed_architecture_companion_handoff.md

Estado do ledger:

AUDITED_OUTSIDE_CANONICAL_118_INVENTORY

Esse relatório deve ser preservado, mas não contado como um dos 118 prompts canônicos até que a identidade do arquivo seja reconciliada com:

    startup bridges;

    generated handoff artifacts;

    Prompt Library;

    possível status de companion não canônico;

    possível inclusão futura no inventário.

Ele não substitui nenhum dos cinco prompts canônicos pendentes.
Qualidade do arquivo histórico 012–040

O arquivo atualmente enviado como chat 012-040 não contém, de forma integral, todos os relatórios detalhados 012–034.

Ele contém:

    referências de continuidade;

    fechamento do Prompt 022;

    checkpoint 031–033;

    checkpoint e relatórios 034–040.

Portanto:

    o status de cobertura pode ser reconciliado;

    a sequência canônica pode ser reconstruída;

    mas o arquivo enviado não constitui um arquivo textual completo de todos os relatórios detalhados 012–030.

Isso não muda a lista dos cinco prompts ainda não auditados, mas deve ser registrado caso se deseje construir posteriormente um arquivo mestre contendo integralmente todos os 118 relatórios.
Estado das fontes pendentes

Há evidência histórica e de freeze para KPR-12-005 e KPR-12-001, incluindo:

    propósito;

    lifecycle;

    routing;

    lessons de Error Memory;

    validator names;

    freeze records.

Entretanto, os uploads desta etapa não contêm os arquivos byte-exact atuais de:

    todos os cinco prompts pendentes;

    seus cinco metadados atuais;

    suas cópias atuais no source archive.

Sem isso, não é seguro produzir fingerprints atuais ou afirmar que o conteúdo histórico corresponde exatamente ao source snapshot que deve ser auditado.
Próximo lote seguro

O próximo lote recomendado é de três prompts:

    architecture_review_project_card_machine_canon.md

    error_memory_active_ready_correction_blueprint.md

    error_memory_active_ready_json_template.md

Justificativa:

    KPR-12-005 é governance-heavy e fortemente ligado a Tool/Project, MCard, Workbench, transações, stale-state protection e freeze;

    KPR-12-002 e KPR-12-003 formam um par de blueprint/schema;

    incluir KPR-12-004 e KPR-12-001 no mesmo ciclo provavelmente reduziria a independência, especialmente porque KPR-12-001 é always-startup e boundary-critical.

Exact next unopened prompt

architecture_review_project_card_machine_canon.md

KPR-12-005

Canonical inventory position:

108 de 118
Audit state

Context reliability:

YES

Canonical coverage:

113 / 118

Remaining:

5

Source changes:

NONE

Validators executed:

NONE

Validation pass claimed:

NO

Para continuar com fingerprints atuais e uma auditoria completa, envie o prompt_library.zip e o source archive atuais, ou somente os cinco arquivos .md pendentes com seus cinco .meta.json.

first audit the last 5 

As cinco auditorias pendentes foram concluídas em ordem canônica, com fechamento individual antes da abertura do alvo seguinte. O inventário confirma suas identidades, códigos e posições na Classe 12.

Fontes exatas inspecionadas:

·

·

·

·

·
FINAL CANONICAL AUDIT CYCLE — FIVE REMAINING PROMPTS
Audit integrity

The supplied protocol was followed:

    one primary target at a time;

    separate fingerprints, findings, disposition and closure;

    related sources inspected only as comparison evidence;

    no source or metadata modification;

    no validator execution;

    no validation-pass claim.

The Prompt Library and source-archive copies were byte-for-byte identical for all five targets.

Total canonical source inspected:

    KPR-12-005: 513 lines

    KPR-12-002: 194 lines

    KPR-12-003: 95 lines

    KPR-12-004: 102 lines

    KPR-12-001: 349 lines

    Total: 1,253 lines

All five files use:

    UTF-8;

    no BOM;

    LF line endings;

    no prohibited control bytes.

AUDIT REPORT — KPR-12-005
Identity

PROMPT:

architecture_review_project_card_machine_canon.md

PROMPT ID:

architecture_review_project_card_machine_canon

PROMPT CODE:

KPR-12-005

DISPLAY NAME:

Architecture Review Project Card Machine Canon

CANONICAL INVENTORY POSITION:

107 of 118

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md

SOURCE SHA-256:

2df3cedc7ec7e0510a80a762eb07c22b7a286faf1be16ba0b4e9e77dacd34f66

METADATA SHA-256:

0b0f7657b2a36edabf115ebe3fc2335888f15b7ebbe82b78da950c45aee07c7d

SOURCE SIZE:

15,145 bytes

SOURCE LENGTH:

513 lines

VERSION:

1.0

STATUS:

active

LOAD TYPE:

routed

PRIORITY:

36

SOURCE STAGE:

architecture-review-project-card-machine-canon-router-bridge-v1

DIRECT REFERENCE SURFACES:

23 current files

DIRECT ID/CODE OCCURRENCES:

approximately 80

ACTIVE DUPLICATE SOURCE:

not found

STARTUP COPY:

absent, correctly routed rather than always-startup

CURRENT FOCUSED VALIDATORS FOUND:

    tools/validate_architecture_review_project_card_machine_canon_router_v1.py

    tools/validate_architecture_review_project_card_lifecycle_v1.py

    tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py

VALIDATORS EXECUTED DURING THIS AUDIT:

no

The frozen routing feature states that KPR-12-005 specializes Architecture Review lifecycle while KPR-12-001 remains the general Tool/Project boundary owner.
Overall verdict

KEEP AND MODERNIZE.

This prompt has a genuine and important responsibility:

Define the lifecycle of one project-owned source target while it is temporarily loaded into reusable Architecture Review tooling.

Its central model is valid:

Tool = reusable card machine
Project = card owner
Selected module = inserted card

The prompt correctly protects:

    target containment;

    root and target invalidation;

    stale asynchronous-result rejection;

    transaction locks;

    project-owned durable results;

    non-destructive eject;

    logical separation during self-hosting.

It should remain active.

However, it currently overlaps too heavily with:

    KPR-12-001 Tool/Project Boundary;

    Brick Wall Q06, Q11 and later authorization gates;

    Large Module Refactor Protocol;

    Workbench implementation contracts;

    transaction and mutation-lane implementation;

    storage-path ownership;

    delivery and validation rules.

The final version should be a lifecycle specialist, not another implementation authority.
Positive findings

    The selected target must remain inside active_project_root.

    Root and target changes invalidate downstream state.

    Late asynchronous results must prove current lifecycle identity.

    Open transactions block switching and ejection.

    Self-hosting does not collapse logical Tool and Project ownership.

    Ejection clears Tool memory without deleting Project-owned source or evidence.

    Preview and Shadow are distinguished.

    The prompt explicitly says it does not replace KPR-12-001.

    Metadata, folder registration, routing and prompt code are synchronized.

    Both registration-oriented and runtime-oriented validators currently exist.

Critical and high-severity findings
F005-001 — Local May implement duplicates Brick Wall authority

The Router Bridge section ends with:

May implement: YES / NO

Resolving MCard ownership and lifecycle does not establish:

    verified problem;

    complete Error Memory preflight;

    final scope;

    source freshness immediately before write;

    validation plan;

    delivery authorization;

    human authorization.

Correction:

Rename the local decision to:

MCard lifecycle gate: COMPLETE / BLOCKED
May proceed to the next Brick Wall gate: YES / NO

The prompt must never independently authorize implementation.
F005-002 — Card identity is incomplete

Current identity contains:

    active project root;

    target relative path;

    target hash or freshness basis;

    lifecycle generation.

Missing:

    operation ID;

    plan ID and version;

    Preview ID;

    transaction ID;

    apply-attempt ID;

    rollback ID;

    source snapshot time;

    current authorization identity.

A target can remain the same while its operation or transaction changes.

Correction:

Bind every asynchronous result and mutation action to a complete operation identity.
F005-003 — target_content_hash or freshness basis is ambiguous

A card identity must not permit an unspecified alternative to a source fingerprint.

Correction:

Require one declared freshness mode:

    exact content hash;

    immutable source revision;

    validated repository commit plus dirty-state record;

    another explicit canonical identity.

F005-004 — APPLIED_NOT_VERIFIED is unreachable

The rollback path permits:

APPLIED_NOT_VERIFIED -> ROLLBACK_REQUESTED

But the main state machine contains no transition into APPLIED_NOT_VERIFIED.

The Q11 validator also accepts the state as a rollback origin without defining the transition that creates it.

Correction:

Add and define:

APPLYING
-> APPLIED_NOT_VERIFIED
-> VERIFIED_TERMINAL

or remove the unused state and model the post-write verification state differently.
F005-005 — Running analysis and Planner ownership are incompletely represented

The state machine does not explicitly model:

    AST audit running;

    Planner worker running;

    Preview generation running;

    cancellation requested;

    cancellation complete;

    stale worker abandoned.

The runtime validator demonstrates that a running audit blocks root switching, but the prompt’s state model does not fully express that behavior.

Correction:

Add worker and cancellation states or define them as orthogonal operation locks.
F005-006 — Cancellation semantics are absent

Invalidating a generation is not the same as:

    cancelling a worker;

    joining it;

    terminating subprocesses;

    releasing resources;

    ensuring callbacks cannot mutate UI state.

Correction:

Require bounded cancellation and terminal cleanup for all card-owned asynchronous operations.
F005-007 — Filesystem containment is underspecified

“Inside active_project_root” needs a physical path contract covering:

    symlinks;

    junctions;

    case normalization;

    alternate separators;

    ..;

    UNC paths;

    drive-letter normalization;

    path replacement after validation.

The inspected validators rely primarily on normalized/common-path checks and do not establish a complete Windows filesystem-identity security boundary.
F005-008 — The prompt is narrower and broader at the same time

Its card is defined as a “selected large module,” but routing triggers include Architecture Review lifecycle generally.

Correction:

Choose one scope:

    any Architecture Review source target; or

    only Large File Refactor targets.

The title and routing currently suggest the broader lifecycle.
F005-009 — Workbench path ownership is copied from KPR-12-001

KPR-12-005 repeats exact Preview, Shadow and transaction destinations.

This increases drift risk.

Correction:

KPR-12-005 should consume resolved owners from KPR-12-001 and only state lifecycle consequences.
F005-010 — “Ownership-free transient garbage root” is misleading

The root is non-authoritative and disposable, but its:

    path;

    lifecycle;

    access;

    cleanup;

    containment;

    disk budget

still require an owner.

Correction:

Use:

non-authoritative project-linked transient workspace

F005-011 — Mutation-lane retention is not fully defined

The prompt says ejection retains mutation-lane state.

It does not distinguish:

    active lock state;

    terminal transaction history;

    archived receipt;

    reusable lane infrastructure;

    stale lock that must be released.

Correction:

Retain historical transaction evidence, but explicitly release terminal locks.
F005-012 — Crash and restart recovery are absent

An application may restart while the card is:

    APPLYING;

    APPLIED_NOT_VERIFIED;

    ROLLBACK_REQUESTED;

    open in a transaction.

Correction:

Define recovery from durable transaction identity before a card can be restored or replaced.
F005-013 — Multi-session concurrency is absent

Two Tool instances can potentially operate on the same target and Project Support records.

Correction:

Require a session/transaction lease or conflict-detection rule.
F005-014 — Eject semantics need finer classification

Tool memory may include:

    target-specific working state;

    safe project-level caches;

    recent-history metadata;

    audit evidence references;

    user preferences.

The prompt currently says to clear a broad list without defining which state is target-, project-, session- or Tool-scoped.
F005-015 — Evidence privacy and retention are absent

Preview, receipts and transaction records can contain:

    source excerpts;

    local paths;

    proprietary code;

    customer data;

    secrets exposed by errors.

Project ownership does not alone establish safe retention.
F005-016 — Module-size validation is outside this owner

The validation section requires touched Python modules to remain within governed size limits.

That belongs to module-size and refactor owners.

KPR-12-005 should only require that applicable external validators are identified.
F005-017 — The registration validator is prose-rigid

validate_architecture_review_project_card_machine_canon_router_v1.py checks many exact sentences and headings.

It can fail after a semantically correct rewrite.

Correction:

Protect:

    ID and code;

    lifecycle-state schema;

    required owner relationships;

    negative routing;

    unique registration;

    current machine-readable result structure.

Do not protect exact explanatory prose.
F005-018 — Runtime validation is coupled to private GUI attributes

The lifecycle validator manipulates a large set of private attributes.

This can detect current regressions but can also block legitimate internal refactors without a public lifecycle contract.

Correction:

Create a small public lifecycle facade or test adapter.
Current owner model

KPR-12-005 should own:

    MCard applicability;

    card identity;

    lifecycle state;

    root/target switching;

    operation locks;

    stale-generation rejection;

    terminal eject;

    retained-versus-cleared state classification.

KPR-12-001 should own:

    Tool, Project, Support and transient-root identity;

    path ownership;

    self-hosting boundary.

Brick Wall should own:

    coding and source-write authorization.

Large Module Refactor should own:

    refactor architecture and module-size rules.

Workbench and transaction owners should own:

    storage and transaction implementation.

Final disposition

CLASSIFICATION:

Architecture Review target-card lifecycle and stale-state protection specialist

ACTION:

KEEP AND MODERNIZE

CURRENT AUDIT STATUS:

active_with_authority_overlap_incomplete_operation_identity_unreachable_state_and_storage_owner_duplication

EXPECTED FINAL STATUS:

active

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure

KPR-12-005 was formally closed.

No source, metadata, router, validator, Workbench state, transaction, Project source or freeze state was modified.
AUDIT REPORT — KPR-12-002
Identity

PROMPT:

error_memory_active_ready_correction_blueprint.md

PROMPT ID:

error_memory_active_ready_correction_blueprint

PROMPT CODE:

KPR-12-002

DISPLAY NAME:

Error Memory Active-Ready Correction Blueprint

CANONICAL INVENTORY POSITION:

111 of 118

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_correction_blueprint.md

SOURCE SHA-256:

1e5cec1793a6fd143b97a9b45546457f61638e0d308fe49b60021ba7d162b150

METADATA SHA-256:

5847e90d86a77cd878c9ef0c1b9fea663cf85199208b202acba3e9543a9c464b

SOURCE SIZE:

6,572 bytes

SOURCE LENGTH:

194 lines

SOURCE VERSION:

not declared

METADATA STATUS:

active

LOAD TYPE:

routed

PRIORITY:

32

SOURCE STAGE:

created_from_error_memory_active_ready_correction_blueprint_v32

DIRECT REFERENCE SURFACES:

20 current files

DIRECT ID/CODE OCCURRENCES:

approximately 40

ACTIVE DUPLICATE SOURCE:

not found

CURRENT WHOLE-PROMPT VALIDATOR:

not found

HISTORICAL FREEZE VALIDATOR:

The freeze record names tools/validate_error_memory_templates_router_bridge_v1.py, but that validator was not present in the inspected current source archive. The frozen feature protected routing and template discoverability rather than proving the semantic correctness of all three template bodies.
Overall verdict

KEEP, NARROW AND ALIGN WITH THE APPLICATION SCHEMA.

This prompt has a useful workflow responsibility:

Decide whether a draft Error Memory lesson has sufficient evidence to be promoted to active status.

It should remain distinct from:

    the marker/envelope contract;

    the field model;

    the application schema;

    the GUI;

    the memorization action.

The current source, however, copies most of the field schema and imposes a patch-delivery model on every durable lesson.
Positive findings

    Active status is evidence-gated.

    Missing evidence must not be invented.

    Draft normalization is not treated as a verified correction.

    Redaction and export safety are required.

    The prompt distinguishes draft, partial evidence and complete evidence conceptually.

    It directs AI to the two current output templates.

    It does not authorize GUI source changes.

Critical and high-severity findings
F002-001 — The prompt has no source version or source lifecycle header

Metadata is versionless as well.

The body therefore has no machine-readable compatibility contract despite using KPR-12-002.
F002-002 — It delegates schema ownership and then copies the schema

The active-ready key list and regression-check contract duplicate:

    KPR-12-003;

    KPR-12-004;

    error_memory/models.py;

    error_memory/schema.py;

    intake normalization.

Correction:

This prompt should reference the canonical schema owner and contain only promotion logic.
F002-003 — It uses statuses rejected by the application

The decision table proposes:

    needs_ai_review;

    active_ready_pending_validation.

The current application accepts only:

    draft;

    active;

    deprecated;

    superseded.

Correction:

Use application-valid status plus a separate promotion/readiness field when needed.
F002-004 — It assumes every active lesson has a correction ZIP

source_patch_zip is mandatory and non-empty.

That excludes or distorts lessons concerning:

    assistant-output formatting;

    procedural errors;

    configuration corrections;

    manual operational repair;

    external dependency incidents;

    user-detected errors with no source patch;

    lessons where installation was not involved.

The existing system has already used artificial values such as no_patch_text_only... to satisfy this requirement.

Correction:

Replace the patch-specific field with a generalized correction-artifact structure, while preserving backward compatibility.
F002-005 — It assumes every regression check is a command

The application currently enforces validation_command, but that application design is itself overly narrow.

Some durable lessons may require:

    manual UI verification;

    static contract check;

    external system confirmation;

    data reconciliation;

    document review;

    security approval;

    scheduled observation.

Correction:

Define typed regression checks and migrate the application schema rather than forcing fake command strings.
F002-006 — required_before_freeze: true is universalized

Not every Error Memory lesson belongs to a freezeable patch.

Correction:

Make freeze applicability explicit.
F002-007 — Promotion evidence lacks source identity

The prompt requests validation output but not:

    source snapshot;

    patch hash;

    validation environment;

    validation time;

    command exit status;

    relation between evidence and corrected source.

F002-008 — Duplicate and supersession admission is absent

Before producing a new active lesson, the workflow should check:

    existing lesson ID;

    fingerprint overlap;

    prevention-trigger overlap;

    whether an existing draft should be updated;

    whether an active lesson should be superseded;

    whether the event is too transient to memorize.

F002-009 — Root cause certainty is not classified

A lesson can have successful mitigation without a proven root cause.

Correction:

Distinguish:

    proven root cause;

    probable cause;

    contributing factor;

    mitigation only.

Only evidence-backed claims should enter active prevention text.
F002-010 — Raw evidence trust levels are absent

Evidence may be:

    observed directly;

    user-reported;

    copied from logs;

    inferred;

    historical;

    generated;

    stale.

F002-011 — The incomplete-evidence output contract is ambiguous

The prompt says not to output active JSON and instead list missing fields.

It does not clearly distinguish:

    user requested a draft block;

    user requested an audit;

    user requested active output only;

    GUI requires marker-wrapped text.

F002-012 — Human memorization authority is underemphasized

Producing active-ready text is not the same as:

    parsing it;

    saving it;

    memorizing it;

    activating it in the current Project.

The prompt must state this explicitly.
F002-013 — Required companions are excessive

The metadata always requires:

    prompt insertion protocol;

    navigation index;

    prompt router.

Correcting one lesson does not normally require prompt-library registration work.
F002-014 — No current semantic validator protects promotion behavior

Current application tests may protect active-ready fields, but no focused validator proves this prompt:

    uses accepted statuses;

    avoids schema duplication;

    supports no-patch lessons;

    checks duplicates;

    separates output from memorization.

Recommended final structure

    Identity and version

    Purpose

    Draft/readiness/active distinctions

    Existing-lesson search

    Evidence classification

    Correction-artifact classification

    Validation-evidence binding

    Root-cause confidence

    Redaction review

    Promotion decision

    Output mode

    Human memorization boundary

    Schema-owner handoff

    Non-authorization statement

    Version history

Final disposition

CLASSIFICATION:

Evidence-gated Error Memory draft-promotion workflow

ACTION:

KEEP, REMOVE COPIED SCHEMA, ALIGN STATUSES AND GENERALIZE NON-PATCH CORRECTIONS

CURRENT AUDIT STATUS:

active_with_schema_duplication_invalid_statuses_patch_centric_promotion_and_missing_duplicate_admission

EXPECTED FINAL STATUS:

active

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure

KPR-12-002 was formally closed.

No lesson, source, metadata, schema, GUI state, Error Memory or freeze memory was modified.
AUDIT REPORT — KPR-12-003
Identity

PROMPT:

error_memory_active_ready_json_template.md

PROMPT ID:

error_memory_active_ready_json_template

PROMPT CODE:

KPR-12-003

DISPLAY NAME:

Error Memory Active-Ready JSON Template

CANONICAL INVENTORY POSITION:

112 of 118

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_json_template.md

SOURCE SHA-256:

84f8b1ab637cd5cb8ed5b2a94222617141fdd1be8ea4ab4087999eff24b3cd3a

METADATA SHA-256:

849c827cff3c0e0a4c778709e328ae6a2748732cd4c06620349fc15ca7dc278d

SOURCE SIZE:

2,728 bytes

SOURCE LENGTH:

95 lines

SOURCE VERSION:

not declared

METADATA STATUS:

active

LOAD TYPE:

routed

PRIORITY:

33

SOURCE STAGE:

error-memory-intake-blueprint-and-copy-window-v1

DIRECT REFERENCE SURFACES:

21 current files

DIRECT ID/CODE OCCURRENCES:

approximately 49

ACTIVE DUPLICATE SOURCE:

not found

CURRENT WHOLE-PROMPT VALIDATOR:

not found
Overall verdict

KEEP AS THE ENVELOPE AND OUTPUT-SHAPE CONTRACT, NOT AS ANOTHER SCHEMA OWNER.

Its unique role should be small:

    exact begin/end markers;

    one JSON object;

    no prose;

    no Markdown fence;

    output-mode behavior;

    routing to the canonical model/schema.

The exact marker requirement is a real GUI integration contract. The current GUI helper reads the two canonical files and places them into the AI intake payload rather than maintaining an independent editable copy. This is a positive single-source pattern. The active source text of both templates is also present in the current intake blueprint flow.
Critical and high-severity findings
F003-001 — Source identity and version are absent

The source does not declare:

    prompt ID;

    prompt code;

    version;

    status;

    load type.

These exist only in metadata.
F003-002 — It duplicates the complete field list

The template should define the output envelope, but it also contains the active-ready schema.

That duplicates KPR-12-004 and the application model.
F003-003 — Required companion dependencies are circular

KPR-12-003 requires:

    KPR-12-004;

    KPR-12-002.

KPR-12-004 requires:

    KPR-12-003;

    KPR-12-002.

KPR-12-002 requires both templates.

Correction:

Use a directed model:

KPR-12-002 promotion workflow
    -> KPR-12-003 output envelope
    -> KPR-12-004 field model

No reverse dependency is needed from the templates to the promotion workflow.
F003-004 — Missing-evidence behavior conflicts with exact-output behavior

The prompt says:

    return exactly one marker-wrapped block;

    add no prose;

    when evidence is missing, explain missing fields outside the final active request.

Correction:

Define explicit modes:

    ACTIVE_LESSON_OUTPUT;

    DRAFT_LESSON_OUTPUT;

    READINESS_ASSESSMENT.

Only the first two produce marker-wrapped JSON.
F003-005 — It is patch- and freeze-centric

The field list and example require:

    source patch ZIP;

    validation command;

    expected marker;

    freeze relevance.

These are not universal Error Memory concepts.
F003-006 — Forward-slash guidance is too broad

Forward slashes are helpful in portable command strings.

They should not rewrite:

    raw Windows error text;

    user-visible paths;

    source evidence;

    registry paths;

    platform-specific command syntax.

F003-007 — It is stricter than the application in inconsistent ways

For example:

    it requires superseded_by in the minimum field list;

    the current active-ready application field list does not require that key;

    it presents all listed nested values as meaningful;

    the current application requires presence but permits some empty contextual fields.

A stricter contract may be appropriate, but it must be deliberate and synchronized.
F003-008 — Schema compatibility is absent

There is no instruction for:

    later compatible schema versions;

    migration;

    unknown fields;

    deprecation;

    consumer capability.

F003-009 — JSON lexical safety is under-specified

The contract should protect:

    valid JSON encoding;

    unescaped control characters;

    invalid newlines;

    duplicate keys;

    non-finite numbers;

    excessive payload size;

    marker text inside values.

F003-010 — Redaction is declared but not reviewed

redaction.applied: true can be asserted falsely.

Correction:

Require redaction evidence or a human-review state.
F003-011 — It does not distinguish generated JSON from memorized state

The output may be:

    generated;

    parsed;

    accepted by intake;

    saved as draft;

    memorized as active.

These are separate evidence states.
F003-012 — No semantic validator exists

A future validator should test the UI parser and output modes, not exact prose.
Recommended final structure

    Identity and version

    Purpose

    Output modes

    Marker contract

    JSON lexical requirements

    Draft versus active output

    Schema/model reference

    Redaction declaration

    Non-memorization statement

    Compatibility

    Version history

Final disposition

CLASSIFICATION:

Error Memory AI-intake marker and output-envelope contract

ACTION:

KEEP, REDUCE TO ENVELOPE BEHAVIOR, REMOVE SCHEMA DUPLICATION AND BREAK COMPANION CYCLES

CURRENT AUDIT STATUS:

active_with_missing_source_identity_schema_duplication_circular_dependencies_and_ambiguous_incomplete_evidence_output

EXPECTED FINAL STATUS:

active

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure

KPR-12-003 was formally closed.

No template, metadata, parser, clipboard payload, Error Memory item or validator was modified.
AUDIT REPORT — KPR-12-004
Identity

PROMPT:

error_memory_model_template.md

PROMPT ID:

error_memory_model_template

PROMPT CODE:

KPR-12-004

DISPLAY NAME:

Error Memory Model Template

CANONICAL INVENTORY POSITION:

113 of 118

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_model_template.md

SOURCE SHA-256:

1a72abbb34b8fd313a66f0ea8e2226f65fdafdb73dd57c2a7f72bfe731d4621e

METADATA SHA-256:

8fb95f2b5b55b2a3109d4a6a82e289c38c855ca3646ce24f04f70151c203f3e6

SOURCE SIZE:

5,104 bytes

SOURCE LENGTH:

102 lines

SOURCE VERSION:

not declared

METADATA STATUS:

active

LOAD TYPE:

routed

PRIORITY:

34

SOURCE STAGE:

error-memory-intake-blueprint-and-copy-window-v1

DIRECT REFERENCE SURFACES:

21 current files

DIRECT ID/CODE OCCURRENCES:

approximately 44

ACTIVE DUPLICATE SOURCE:

not found

CURRENT WHOLE-PROMPT VALIDATOR:

not found
Overall verdict

KEEP AS THE SINGLE HUMAN-READABLE FIELD MODEL, BUT GENERATE OR VERIFY IT AGAINST THE MACHINE SCHEMA.

Of the three Error Memory prompt assets, this is the best candidate to own the filled example and field guidance.

It must not remain independently hand-maintained against:

    error_memory/models.py;

    error_memory/schema.py;

    intake normalization;

    KPR-12-002;

    KPR-12-003.

Positive findings

    It provides a complete marker-wrapped example.

    It requires concrete values rather than placeholders.

    It preserves real raw error context while requiring scrubbing.

    It distinguishes exception information from structural fingerprinting.

    It forbids invented validation evidence.

    The GUI currently reads this canonical source at click time.

Critical and high-severity findings
F004-001 — Source identity and version are absent

The active source does not declare its own KPR identity or compatibility version.
F004-002 — The operation-phase enum is not the application contract

The template limits phases to:

    patch-delivery;

    validation;

    freeze;

    runtime;

    prompt-sync;

    startup-sync;

    unknown.

The current application treats operation phase as a general string, and real lessons use more specific values.

Correction:

Do not present a closed enum unless the machine schema enforces it.
F004-003 — Lesson-ID guidance conflicts with the builder

The template says lesson IDs:

    start with lesson-;

    include a version suffix.

The current application builder generates random IDs such as:

lesson-<12 hex characters>

without a version suffix.

Correction:

Choose one identity policy and migrate both source and application.
F004-004 — Fingerprint guidance conflicts with implementation

The template says:

fingerprint_hash = stable lowercase slug

The current fingerprint owner generates a SHA-256 hexadecimal digest over structural components.

This is a direct contract mismatch.

Correction:

The template must consume the current fingerprint strategy and representation.
F004-005 — Relative paths conflict with current implementation style

The template encourages forward-slash portability.

The current fingerprint path normalizer often produces Windows-style backslashes.

Raw evidence and canonical relative path need separate representation rules.
F004-006 — It repeats patch/freeze assumptions

The model always includes:

    source patch ZIP;

    validation command;

    required-before-freeze true;

    install summary.

These fields need generalized semantics or optional applicability.
F004-007 — It is not a real schema

The template does not define:

    JSON types;

    maximum lengths;

    allowed statuses;

    required versus optional fields;

    nullable values;

    unknown-field behavior;

    date format validation;

    array constraints.

It should be called a human-readable model, while the application schema remains machine authority.
F004-008 — Schema drift is structurally guaranteed

The same shape exists in:

    this model;

    KPR-12-003 field list;

    KPR-12-002 checklist;

    ACTIVE_REQUIRED_PRESENT_FIELDS;

    ACTIVE_REQUIRED_MEANINGFUL_FIELDS;

    JSON schema;

    intake allowed keys.

Correction:

Generate the human model from a single schema source or add a synchronization validator.
F004-009 — The example hardcodes active status

When evidence is incomplete, the user needs a draft model, not an active model with guessed values.

Correction:

Provide explicit draft and active profiles.
F004-010 — Supersession semantics are absent

superseded_by is shown as an empty string but the model does not explain:

    when it is allowed;

    whether the old lesson becomes superseded;

    whether both lessons remain accessible;

    how cycles are prevented.

F004-011 — Fingerprint collision and duplicate handling are absent
F004-012 — Timestamp provenance is absent

The template does not state whether timestamps represent:

    original error;

    draft creation;

    correction;

    active promotion;

    last edit.

F004-013 — Validation evidence does not identify environment or source
F004-014 — Redaction rules can become generic boilerplate

Copying the same three sentences does not prove the actual lesson was scrubbed.
F004-015 — Required companions are circular

The model should not require the correction workflow for every use.
F004-016 — No focused synchronization validator exists

The previously frozen routing validator is not present in the current source archive, and no current validator was found that compares this model against the application schema.
Recommended authority model

Machine authority:

    application schema and model definitions.

Human-readable field model:

    KPR-12-004, generated or verified from machine authority.

Output envelope:

    KPR-12-003.

Draft-promotion workflow:

    KPR-12-002.

Final disposition

CLASSIFICATION:

Human-readable Error Memory lesson field model

ACTION:

KEEP, MAKE IT THE ONLY HUMAN MODEL, AND SYNCHRONIZE IT WITH THE MACHINE SCHEMA

CURRENT AUDIT STATUS:

active_with_application_contract_drift_identity_mismatch_fingerprint_mismatch_and_schema_duplication

EXPECTED FINAL STATUS:

active

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure

KPR-12-004 was formally closed.

No template, application schema, lesson ID, fingerprint logic, GUI helper or Error Memory data was modified.
AUDIT REPORT — KPR-12-001
Identity

PROMPT:

project_tool_boundary_canon.md

PROMPT ID:

project_tool_boundary_canon

PROMPT CODE:

KPR-12-001

DISPLAY NAME:

Project Tool Boundary Canon

CANONICAL INVENTORY POSITION:

115 of 118

CANONICAL PATH:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md

SOURCE SHA-256:

853c4192e23dadd83c591fac8913fb8ff9d190482e1309041e1b6d19ad600e96

METADATA SHA-256:

7ac20a66813f95d72c75eb901d1fd4cfc7ccedb419c1dd86501b8c0160d2b0a6

SOURCE SIZE:

19,800 bytes

SOURCE LENGTH:

349 lines

VERSION:

1.5

STATUS:

active

LOAD TYPE:

always_startup

PRIORITY:

35

SOURCE STAGE:

brick-wall-q06-tool-project-identity-enforcement-v1

UPDATED FOR:

brick-wall-q06-tool-project-identity-enforcement-v1

DIRECT REFERENCE SURFACES:

46 current files

DIRECT ID/CODE OCCURRENCES:

approximately 158

ACTIVE DUPLICATE SOURCE:

not found

GENERATED STARTUP COPY:

present as 14_project_tool_boundary_canon.md

STARTUP SYNCHRONIZATION:

The generated startup copy contains only a generated-file header in addition to the canonical content. Its header records the exact canonical source SHA-256:

853c4192e23dadd83c591fac8913fb8ff9d190482e1309041e1b6d19ad600e96

No startup source drift was found.

CURRENT FOCUSED VALIDATORS FOUND:

    scripts/validate_project_tool_boundary_canon_v1.py

    tools/validate_project_tool_boundary_nested_support_root_v1.py

    tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py

    tools/validate_brick_wall_q06_tool_project_identity_v1.py

    related Q11, Q17 and transient-root validators

VALIDATORS EXECUTED DURING THIS AUDIT:

no
Overall verdict

KEEP AS A CENTRAL CANON, BUT SPLIT THE FULL SOURCE FROM THE ALWAYS-STARTUP BRIDGE.

This is one of the project’s most important boundary owners.

It correctly prevents the recurrent self-hosting error:

KANDA runs the operation
therefore KANDA owns every target and every result

Its essential laws are sound:

    Tool and Active Project are separate logical identities.

    Project source and Project Support are different roots.

    Project Support must remain external to Project source.

    Transient work must not become durable truth.

    Self-hosting does not collapse ownership.

    Generated artifacts are not automatically source truth.

    Source writes must match the declared operation owner.

    Q06 does not authorize coding.

The prompt should remain canonical.

The current body is nonetheless too large and implementation-specific for an always-loaded startup prompt.
Positive findings

    Canonical ID, code, version, metadata and generated startup source are synchronized.

    Q06 explicitly keeps May begin coding: NO.

    Self-hosting is modeled as logical separation despite physical equality.

    Nested support roots fail closed.

    Preview and Shadow are distinguished.

    Tool source, Project source, Project Support and transient roots are separated.

    Selected-project paths are dynamic rather than hardcoded to KANDA.

    The prompt protects Project-specific freeze and Error Memory state from reusable Tool storage.

    Current validators cover several real runtime and path behaviors.

    No competing KPR-12-001 metadata record was found.

Critical and high-severity findings
F001-001 — The always-startup source is too large

At 349 lines and almost 20 KB, it carries:

    full Q06 record;

    path examples;

    Workbench-specific ownership;

    nested-root migration;

    fixture policy;

    routing rules;

    validation questions;

    many repeated do-not-regress statements.

Correction:

Create a compact always-startup bridge containing only:

    four identities;

    self-hosting law;

    source/support/transient separation;

    wrong-root hard stop;

    route to full KPR-12-001.

Keep the full canon routed on demand.

This is a reduction of startup context, not creation of a competing canon.
F001-002 — “Ownership-free transient garbage root” is semantically wrong

The root has no durable authority, but it still requires:

    a path owner;

    a cleanup owner;

    permission policy;

    storage budget;

    containment;

    lifecycle.

Correction:

Use:

non-authoritative transient workspace

F001-003 — The prompt is KANDA-specific despite residing among generalized canons

It hardcodes:

    KANDA Tool identity;

    support-root naming;

    first_prompt_files;

    second_prompt_files;

    Workbench layout;

    freeze and Error Memory paths;

    drive-root sibling policy.

Correction:

Classify it explicitly as the KANDA Tool/Project boundary profile, or move the generic identity law to a smaller abstract core.

Do not claim these paths are universal software architecture.
F001-004 — Slug-only support-root identity can collide

Two projects with the same directory name on the same drive can resolve to the same support root:

E:/client_a/app
E:/client_b/app
-> E:/app_show_project_to_AI

Correction:

Add a stable Project ID or disambiguating root fingerprint.
F001-005 — Project rename and move behavior are absent

Changing:

    project folder name;

    drive;

    canonical path;

    selected workspace

can orphan or collide with support data.

Correction:

Define migration, discovery and conflict behavior.
F001-006 — Path identity is not a complete physical-identity contract

The Q06 validator compares normalized path strings to determine “same physical root.”

That does not fully account for:

    symlinks;

    junctions;

    substituted drives;

    UNC aliases;

    case-preserving aliases;

    network mappings.

Correction:

Rename the field to same_canonical_resolved_root unless true filesystem identity is proven.
F001-007 — Nested-root checks are partly lexical

Prefix or common-path checks can be insufficient around junctions and link replacement.

Correction:

Use resolved paths, containment recheck immediately before write and safe open/write operations where applicable.
F001-008 — The drive-root model is not universal

The prompt assumes <project_drive>.

Potential environments include:

    POSIX;

    UNC shares;

    containers;

    cloud workspaces;

    read-only mounts;

    projects without writable parent directories.

The current validator creates a POSIX approximation, but the source does not define the profile.
F001-009 — Support-root security is absent

Project Support may contain:

    code excerpts;

    error logs;

    patient or customer data;

    freeze records;

    credentials accidentally captured in diagnostics.

Correction:

Add:

    permissions;

    redaction;

    encryption profile when required;

    retention;

    secure deletion;

    backup policy.

F001-010 — Transient cleanup policy is absent

The canon says transient data may be deleted, but does not define:

    who deletes it;

    when;

    what happens after crashes;

    maximum age;

    disk-quota protection;

    handling of failed diagnostics.

F001-011 — Failed diagnostic evidence needs a durable summary

A transient controlled clone may be deleted after validation, but a failure may require durable:

    logs;

    source fingerprints;

    failure markers;

    reproduction record.

The clone can remain disposable while its scrubbed evidence is routed to Project Support.
F001-012 — Q06 operation identity is incomplete

The identity record lacks:

    operation ID;

    session ID;

    transaction ID;

    Project ID independent of slug;

    selection timestamp;

    source revision;

    identity expiration/invalidation.

F001-013 — Mixed governed operations are underdefined

MIXED_GOVERNED is allowed, but the canon does not define:

    separate Tool and Project write sets;

    atomicity;

    ordering;

    rollback;

    validators per owner;

    public-contract migration;

    partial failure.

F001-014 — Cross-project paths are over-constrained by the validator

The current Q06 validator rejects any non-empty cross_project_paths.

Legitimate operations can read:

    external dependencies;

    comparison repositories;

    controlled fixtures;

    migration sources.

The correct rule is no undeclared or unauthorized cross-project mutation.
F001-015 — Generated-evidence authority validation is prose-based

The Q06 validator accepts authority only when a free-text field contains phrases such as:

    non-authoritative;

    canon assigns.

Correction:

Use a structured enum plus owner reference.
F001-016 — Human-selection evidence is validated by keywords

The validator searches for words such as current or human.

This is not a durable evidence contract.

Correction:

Use a typed selection record:

    selected root;

    selection source;

    timestamp;

    session;

    Project ID;

    freshness.

F001-017 — Required companions are excessive

Metadata requires:

    box_architecture_canon;

    bundle_gated_development_workflow.

The Bundle-Gated prompt was already identified as scope-sprawled and should not be a universal companion for every startup boundary decision.

Correction:

Companions should be conditional.
F001-018 — Workbench detail occupies too much of the general canon

Preview and Shadow ownership are important, but the complete Workbench path profile should live in a specialist overlay consumed by the boundary canon.
F001-019 — The root list mixes classes of identity

Tool and Project are logical/source owners.

Support and transient roots are storage/lifetime classes.

The final contract should explicitly separate:

    logical owner identity;

    source root;

    support root;

    temporary workspace;

    generated artifact authority.

F001-020 — Multi-project workspaces are absent

A selected “project” may be:

    monorepo;

    workspace;

    repository set;

    parent Project with multiple source roots.

One active_project_root may be insufficient.
F001-021 — Concurrent sessions are absent

Two KANDA sessions can use the same Project Support root and transient namespace.

Correction:

Add session and operation namespaces plus conflict detection.
F001-022 — Current validators preserve many exact phrases

Several validators require precise explanatory text and historical marker strings.

Correction:

Retain behavioral path and negative tests, but reduce prose assertions.
F001-023 — One validator still identifies itself as v1.4

The canonical source and metadata are v1.5, while scripts/validate_project_tool_boundary_canon_v1.py describes and emits a v1.4 feature identity.

It accepts later versions, so this is not an active rejection defect, but it is stale validator provenance.
F001-024 — “Absolute prohibition in every circumstance” needs scope

The nested support-root prohibition is a valid KANDA architecture rule.

It should be stated as:

for KANDA-managed Project Support roots

rather than a universal prohibition on every support directory inside every repository.
Current owner model

KPR-12-001 should own:

    Tool and selected-Project logical identity;

    self-hosting separation;

    Project source versus external Project Support;

    transient non-authority;

    source-write owner classification;

    wrong-root hard stop.

Box Architecture should own:

    module and responsibility boundaries.

Durable Documentation Routing should own:

    durable document/evidence destinations.

Class 05 should own:

    staging and installation details.

MCard should own:

    Architecture Review target lifecycle.

Workbench should own:

    its specific Preview, transaction and Shadow implementation.

Brick Wall should own:

    final source-write authorization.

Recommended final structure
Always-startup bridge

Approximately 30–60 lines:

    Tool identity

    selected Project identity

    self-hosting rule

    source/support/transient distinction

    wrong-root stop

    full-canon routing

Full routed canon

    Identity and version

    Project identity record

    logical owners

    root profiles

    stable Project ID

    canonical path resolution

    self-hosting

    mixed governed operations

    support-root security

    transient lifecycle

    generated-artifact authority

    concurrent sessions

    specialist overlays

    validation

    version history

Final disposition

CLASSIFICATION:

Canonical KANDA Tool-versus-selected-Project identity and root-ownership owner

ACTION:

KEEP, SPLIT COMPACT STARTUP BRIDGE FROM FULL CANON, AND MODERNIZE PROJECT/PATH IDENTITY

CURRENT AUDIT STATUS:

active_with_startup_context_bloat_slug_collision_risk_ownership_free_terminology_and_path_identity_gaps

EXPECTED FINAL STATUS:

active

FOCUSED VERIFICATION BEFORE CORRECTION:

required
Closure

KPR-12-001 was formally closed.

No canonical source, generated startup file, metadata, path helper, Project Support folder, validator, routing surface or freeze memory was modified.
FINAL CLASS 12 CHECKPOINT
Dispositions
KPR-12-005

KEEP AND MODERNIZE.

Retain MCard lifecycle ownership.

Remove local implementation authority and duplicate root/storage contracts.
KPR-12-002

KEEP AND NARROW.

Retain evidence-gated draft promotion.

Remove copied schema and patch-only assumptions.
KPR-12-003

KEEP AS OUTPUT ENVELOPE.

Retain exact marker/no-prose contract.

Remove field-schema duplication.
KPR-12-004

KEEP AS THE SINGLE HUMAN-READABLE MODEL.

Synchronize or generate it from the application schema.
KPR-12-001

KEEP AS CENTRAL BOUNDARY OWNER.

Split a compact always-startup bridge from the full routed canon.
Recommended Error Memory owner architecture

Application schema/models
    = machine authority

KPR-12-004
    = human-readable field model generated or verified from machine authority

KPR-12-003
    = marker and output-envelope contract

KPR-12-002
    = draft/readiness/promotion workflow

Error Memory GUI
    = intake, parsing, validation and explicit human Memorize Error action

This removes the current circular companion model and four-way schema duplication.
KPR-12-001 and KPR-12-005 relationship

KPR-12-001
    owns Tool / Project / Support / transient identity

KPR-12-005
    owns the lifecycle of one Architecture Review target

Brick Wall
    owns final implementation authorization

Neither KPR-12-001 nor KPR-12-005 should replace the other.
Validator findings

Current validators provide useful protection, particularly for:

    nested support-root rejection;

    Workbench Preview/Shadow separation;

    self-hosting;

    target containment;

    stale lifecycle state;

    transaction locks;

    unique routing identity.

Future correction should reduce:

    exact prose matching;

    substring-based evidence validation;

    private GUI attribute coupling;

    exact historical marker dependence;

    stale validator version labels.

The Error Memory template trio currently lacks a focused source-to-application schema synchronization validator.
Error Memory relevance

The compact Error Memory lessons directly supported:

    KPR-12-005 lifecycle ownership;

    KPR-12-001 Preview/Shadow routing;

    marker-wrapped Error Memory intake;

    package import context and validator-rigidity precautions.

Historical freeze records were treated as prior evidence only.

They were not treated as proof that the current files still pass, because no validators were rerun in this audit.
Canonical inventory completion

Canonical prompts formally audited:

118 / 118

Additional audited prompt outside the canonical 118 inventory:

1

Exact next unopened canonical prompt:

NONE

Canonical audit phase:

COMPLETE
Final audit integrity statement

    No prompt source was changed.

    No metadata was changed.

    No generated startup artifact was changed.

    No routing record was changed.

    No Error Memory lesson was created or memorized.

    No Project Support path was changed.

    No validator was executed.

    No validation pass was claimed.

    No freeze action was performed.

The canonical 118-prompt audit is now complete.

Fontes exatas inspecionadas:gimme all Fontes exatas inspecionadas: in a zip

Conteúdo:

    5 fontes canônicas .md

    5 metadados .meta.json

    INSPECTED_SOURCES_MANIFEST.json com tamanho e SHA-256 de cada arquivo

Integridade do ZIP verificada: OK.

0073 MAIN BRICK WALL 13.07.2026(6).md
File
we are at q25 of brick wall update , can we start prompts update or is it better finish  brick wall implementation?

É melhor terminar primeiro a implementação e a finalização governada do Brick Wall. O Q25 é um bom ponto de pausa antes de começar a modificar os prompts.

O próprio handoff atual ainda registra:

    instalação local no Windows: pendente;

    validação local: pendente;

    evidência durável: pendente;

    Freeze Preview e Confirm and Write: pendentes;

    revisão da lição de Error Memory: pendente;

    estado final: “SOURCE AND DELIVERY PACKAGE COMPLETE / LOCAL INSTALLATION AND GOVERNED FINALIZATION PENDING”.

Por que não iniciar as alterações dos prompts no Q25

Os próximos quesitos contêm justamente as proteções necessárias para atualizar os 118 prompts com segurança:

    Q26: segurança e contrato final dos ZIPs;

    Q27: encoding e control bytes;

    Q28: provenance estruturada dos erros;

    Q30: confirmação humana e freeze;

    Q31: mapa changed-file → validator;

    Q32: provenance das validações;

    Q36: tamanho e coesão dos módulos;

    Q37: reconciliação dos owners duplicados;

    Q38: freshness dos handoffs;

    Q40: release governado com um primary box.

Começar agora significaria alterar a Prompt Library antes de finalizar o sistema criado justamente para governar essas alterações.

Além disso, as atualizações de prompts provavelmente tocarão:

    fontes canônicas;

    metadados;

    routing humano e machine-readable;

    folder cards;

    grupos;

    startup bridges;

    validators;

    possíveis aliases/deprecations.

Esse é exatamente o tipo de trabalho em que Q26–Q40 devem estar operacionais antes da primeira escrita.
Sequência recomendada
1. Terminar o Brick Wall até Q40

Isso não significa implementar indiscriminadamente todos os pilotos.

Para o trabalho atual:

    Q24 Property-Based Testing pode permanecer N/A ou PILOT_NOT_ADMITTED, com justificativa;

    Q25 Mutation Testing pode permanecer N/A ou limitado a validators críticos;

    Q29 Runtime Trace pode ser N/A se não houver runtime mutation relevante;

    Q33 Local Model Provenance pode ser N/A;

    Q34–Q35 Performance podem ser N/A;

    Q39 New Context System pode ser N/A.

“Terminar Q01–Q40” significa que cada quesito possui:

    estado formal;

    evidência ou justificativa de não aplicabilidade;

    owner;

    blocker;

    próximo passo.

Não significa criar ferramentas desnecessárias para preencher todos os itens.
2. Finalizar a própria feature Brick Wall

Antes de atualizar os prompts:

    instalar a versão atual no projeto Windows;

    executar a validação local;

    confirmar os markers reais;

    gerar evidência durável no Project Support;

    executar o merge de evidência para freeze;

    revisar o Freeze Preview;

    realizar Confirm and Write;

    revisar a lição de Error Memory;

    memorizar ou rejeitar explicitamente a lição;

    atualizar o handoff final com o estado frozen.

3. Só então iniciar as alterações dos prompts

A primeira execução do Brick Wall após o freeze deve ser:

Current task:
Prompt Library consolidation after the 118-prompt audit

Primary box:
kanda_prompt_workspace/prompt_library

Verified problem:
118 prompts audited; corrections, deprecations, owner reconciliation
and schema/routing cleanup are required.

May begin coding:
determined by the completed Q01–Q40 ledger

O que pode ser feito agora sem risco

Enquanto o Brick Wall é finalizado, podemos preparar em modo somente leitura:

    ordem de prioridade dos prompts;

    grupos de correção;

    owner-conflict matrix;

    prompts que serão mantidos, reduzidos, reclassificados ou deprecados;

    dependências entre alterações;

    versões-alvo;

    validators necessários;

    estratégia de batches e releases.

Mas eu não começaria ainda a editar as fontes, metadados ou routing.
Minha recomendação final

Fechar Brick Wall → validar localmente → congelar → revisar Error Memory → iniciar as atualizações dos prompts usando o Brick Wall já operacional.

Isso adiciona uma pequena etapa agora, mas evita que a consolidação dos 118 prompts seja feita sob um sistema de governança ainda incompleto e potencialmente mutável.


