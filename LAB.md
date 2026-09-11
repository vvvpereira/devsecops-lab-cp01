# Laboratório Prático: Semgrep (SAST) + Checkov (IaC Security)

**Grupo:** Grupo 1  
**Ferramentas:** Semgrep (SAST) + Checkov (IaC Security)  
**Alvo Vulnerável:** OWASP Juice Shop (`bkimminich/juice-shop`) + Arquivos Inseguros em `target/`  
**Duração estimada:** 12 minutos  

---

## 0. Pré-requisitos (Executar ANTES da aula)

- Docker Engine >= 24 e Docker Compose v2 instalados
- 4 GB de RAM livres e ~3 GB de espaço livre em disco
- **Comandos de preparação:**

  ```bash
  git clone https://github.com/vvvpereira/devsecops-lab-grupo1.git
  cd devsecops-lab-grupo1
  docker pull returntocorp/semgrep:latest
  docker pull bridgecrew/checkov:latest
  docker pull bkimminich/juice-shop:v15.0.0

VERIFICAÇAO: docker images | grep -E "semgrep|checkov|juice-shop"


