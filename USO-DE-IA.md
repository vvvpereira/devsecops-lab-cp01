Declaração de Uso de Inteligência Artificial Generativa

Disciplina: DevSecOps preparatório E|CDE
Trabalho: Check Point 01 — Pipeline DevSecOps (Grupo 1)

1. Contexto e Ferramentas Utilizadas

Em conformidade com as diretrizes do trabalho, declaramos que ferramentas de IA generativa foram utilizadas como suporte ao desenvolvimento, revisão e validação deste projeto [1].

Ferramentas de IA: ChatGPT / Gemini / Claude Code

Escopo de Atuação: Apoio na estruturação de sintaxe de pipelines (GitHub Actions YAML), refinamento de scripts de automação do laboratório e auxílio na formatação da documentação.

2. O que foi gerado pela IA

Estrutura de Workflows de CI/CD:
Auxílio na sintaxe dos arquivos .github/workflows/ci-red.yml e .github/workflows/ci-green.yml para integração dos scanners Semgrep e Checkov.

Modelagem de Relatórios e Troubleshooting:
Sugestão de comandos Docker/Podman e montagem da tabela de troubleshooting do LAB.md.

Revisão de Código Inseguro para Teste:
Ajuste do formato da credencial de teste em target/app.py para detecção adequada pela regra p/secrets.

3. Processo de Validação Humana e Técnica

Toda a informação técnica, código e configuração fornecida ou sugerida por IA foi estritamente verificada e validada na prática pelo grupo [1]:

Validação Local: Todos os comandos do Semgrep e Checkov foram executados e testados em ambiente isolado de máquina virtual com Podman/Docker.

Validação de Pipeline: O funcionamento do Quality Gate foi confirmado com a execução real dos builds vermelho e verde no GitHub Actions.

Auditoria de Achados: Os relatórios em JSON foram inspecionados manualmente para classificar e justificar os achados reais (Verdadeiros Positivos).
