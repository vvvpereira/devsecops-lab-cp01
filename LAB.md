# Laboratório Prático: Semgrep (SAST) + Checkov (IaC Security)

**Grupo:** Grupo 1  
**Ferramentas:** Semgrep (SAST) + Checkov (IaC Security)  
**Alvo Vulnerável:** OWASP Juice Shop (`bkimminich/juice-shop`) + Arquivos Inseguros em `target/`  
**Duração estimada:** 12 minutos  

---

0. Pré-requisitos (Executar ANTES da aula)
Docker Engine >= 24 e Docker Compose v2 instalados
4 GB de RAM livres e ~3 GB de espaço livre em disco
Comandos de preparação:
git clone https://github.com/SEU_USUARIO/devsecops-lab-grupo1.git
cd devsecops-lab-grupo1
docker pull returntocorp/semgrep:latest
docker pull bridgecrew/checkov:latest
docker pull bkimminich/juice-shop:v15.0.0

Verificação: O comando docker images | grep -E "semgrep|checkov|juice-shop" deve listar as 3 imagens.
1. Subir o Ambiente (Alvo Vulnerável Autorizado)
Comando:
docker compose up -d

Resultado esperado: Criação e execução do contêiner juice-shop-target na porta 3000.
Validação: Acesse http://localhost:3000 no seu navegador ou execute:
curl -I http://localhost:3000

2. Executar a Ferramenta 1: Semgrep (SAST)
Comando:
docker run --rm -v $(pwd):/src returntocorp/semgrep semgrep scan --config=p/owasp-top-ten /src

Resultado esperado: Varredura estática no código Python (target/app.py) apontando a detecção de segredo exposto no código (hardcoded credential/API key).
3. Executar a Ferramenta 2: Checkov (IaC Security)
Comando:
docker run --rm -v $(pwd):/tf bridgecrew/checkov --directory /tf/target

Resultado esperado: Varredura de Infraestrutura como Código nos arquivos target/Dockerfile e target/main.tf, apontando execução como root e bucket S3 com leitura pública.
4. Interpretar os Relatórios Versionados

Os relatórios pré-gerados estão salvos no formato JSON na pasta ./reports/:

Semgrep Report: reports/semgrep-report.json
Checkov Report: reports/checkov-report.json

Para visualizar um trecho no terminal:

cat reports/semgrep-report.json | head -n 30

5. Rodar o Pipeline CI/CD e Observar o Quality Gate
Acesse a aba Actions no repositório GitHub.
Observe o workflow DevSecOps Quality Gate - Build Vermelho e verifique que ele falhou devido aos achados críticos.
Acione manualmente o workflow DevSecOps Quality Gate - Build Verde para visualizar a aprovação.
6. Perguntas de Verificação (Responder e Entregar)
Pergunta 1: Qual é a credencial/chave exposta (hardcoded secret) detectada pelo Semgrep no arquivo target/app.py?
Pergunta 2: Qual a severidade e a falha apontada pelo Checkov quanto ao usuário configurado no target/Dockerfile?
7. Encerrar o Ambiente

Após concluir as análises, destrua o ambiente de testes:

docker compose down -v


