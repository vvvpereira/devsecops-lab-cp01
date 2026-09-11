# Laboratório DevSecOps - Grupo 1 (Semgrep + Checkov)

Este repositório contém o ambiente prático e os pipelines de CI/CD desenvolvidos para o trabalho prático da disciplina de DevSecOps.

## 🚀 Pré-requisitos para a Turma (Executar com 24h de Antecedência)

Para acompanhar a execução ao vivo durante a aula, realize o download prévio do repositório e das imagens Docker:

### 1. Requisitos de Software e Hardware

- **Docker Engine:** >= 24.0
- **Docker Compose:** v2
- **PODMAN TAMBÉM SERVE

### 2. Comandos de Preparação (Download Prévio)

Execute os comandos abaixo no terminal com antecedência:

```bash
# 1. Clone do repositório
git clone https://github.com/vvvpereira/devsecops-lab-grupo1.git
cd devsecops-lab-grupo1

# 2. Download das imagens dos scanners e do alvo vulnerável
docker pull returntocorp/semgrep:latest
docker pull bridgecrew/checkov:latest
docker pull bkimminich/juice-shop:v15.0.0

### 3. Verificação das Imagens Baixadas

Confirme se as imagens estão salvas localmente:

```bash
docker images | grep -E "semgrep|checkov|juice-shop"

