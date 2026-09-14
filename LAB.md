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

## 1\. Subir o Ambiente (Alvo Vulnerável Autorizado)

* **Comando:**

```
docker compose up -d
podman run -d --name juice-shop-test -p 3000:3000 docker.io/bkimminich/juice-shop:v15.0.0

```

* **Resultado esperado:** Criação e execução do contêiner `juice-shop-target` na porta `3000`.
* **Validação:** Acesse `http://localhost:3000` no seu navegador ou execute `curl -I http://localhost:3000`.

---

## 2\. Executar a Ferramenta 1: Semgrep (SAST)

* **Comando:**

```
podman run --rm -v $(pwd):/src:Z docker.io/returntocorp/semgrep semgrep scan --config=p/owasp-top-ten --config=p/secrets /src

podman run --rm -v $(pwd):/src:Z docker.io/returntocorp/semgrep semgrep scan --config=p/owasp-top-ten --config=p/secrets --json --output=/src/reports/semgrep-report.json /src

```

* **Resultado esperado:** Varredura estática no código Python (`target/app.py`) apontando a detecção de segredo exposto no código (*hardcoded credential/API key*).

---

## 3\. Executar a Ferramenta 2: Checkov (IaC Security)

* **Comando:**

```
docker run --rm -v \$(pwd):/tf bridgecrew/checkov --directory /tf/target
podman run --rm -v $(pwd):/tf:Z docker.io/bridgecrew/checkov --directory /tf/target

podman run --rm -v $(pwd):/tf:Z docker.io/bridgecrew/checkov --directory /tf/target -o json &gt; reports/checkov-report.json

```

* **Resultado esperado:** Varredura de Infraestrutura como Código nos arquivos `target/Dockerfile` e `target/main.tf`, apontando execução como `root` e bucket S3 com leitura pública.

---

## 4\. Interpretar os Relatórios Versionados

Os relatórios pré-gerados estão salvos no formato JSON na pasta `./reports/`:

* **Semgrep Report:** `reports/semgrep-report.json`
* **Checkov Report:** `reports/checkov-report.json`

Para visualizar um trecho no terminal:

```
cat reports/semgrep-report.json | head -n 30

```

---

## 5\. Rodar o Pipeline CI/CD e Observar o Quality Gate

1. Acesse a aba **Actions** no repositório GitHub.
2. Observe o workflow **DevSecOps Quality Gate - Build Vermelho** e verifique que ele **falhou** devido aos achados críticos.
3. Acione manualmente o workflow **DevSecOps Quality Gate - Build Verde** para visualizar a aprovação.

---

## 6\. Perguntas de Verificação (Responder e Entregar)

1. **Pergunta 1:** Qual é a credencial/chave exposta (*hardcoded secret*) detectada pelo Semgrep no arquivo `target/app.py`?
2. **Pergunta 2:** Qual a severidade e a falha apontada pelo Checkov quanto ao usuário configurado no `target/Dockerfile`?

---

## 7\. Encerrar o Ambiente

Após concluir as análises, destrua o ambiente de testes:

```
docker compose down -v

```

---

## Troubleshooting

| Sintoma                           | Causa Provável                                | Solução                                                     |
| --------------------------------- | --------------------------------------------- | ----------------------------------------------------------- |
| Conexão recusada na porta 3000    | Porta 3000 já em uso na máquina               | Altere a porta mapeada no docker-compose.yml para 8080:3000 |
| Permissão negada ao montar volume | SELinux ativo no sistema (RHEL/Oracle/Fedora) | Adicione o sufixo :Z no volume (ex: \-v $(pwd):/src:Z)      |
| Imagem não encontrada             | Download prévio não realizado                 | Execute os comandos de docker pull listados no item 0       |

