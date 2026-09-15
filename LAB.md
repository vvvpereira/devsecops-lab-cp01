# 🛡️ Guia Definitivo e Roteiro de Apresentação do Laboratório Guiado (DevSecOps)

> **Disciplina:** DevSecOps preparatório E|CDE (EC-Council Certified DevSecOps Engineer)  
> **Trabalho:** Check Point 01 - Pipeline DevSecOps  
> **Grupo:** Grupo 1 - Toolchain OWASP / Pipeline Tradicional  
> **Ferramentas:** Semgrep (SAST), Checkov (IaC Security), OWASP Juice Shop (Alvo)  
> **Objetivo:** Conduzir a turma em um laboratório prático de 12 minutos e demonstrar a atuação de Quality Gates em CI/CD (GitHub Actions).

---

## 📖 1. Visão Geral e Contexto Didático para a Apresentação

### 🔑 Conceitos-chave a destacar durante a fala:
* **Shift-Left Security:** Mover a segurança para as fases iniciais do desenvolvimento (Code e Build). Quanto mais cedo uma vulnerabilidade é encontrada, mais barato e rápido é para corrigi-la.
* **SAST (Static Application Security Testing):** Teste de caixa-branca (*white-box*) no código-fonte próprio da aplicação. Não precisa do sistema em execução.
* **IaC Security (Infrastructure as Code Security):** Análise estática de arquivos de configuração de infraestrutura (Dockerfile, Terraform, K8s, Helm) para evitar más configurações antes de subir recursos na nuvem ou em contêineres.
* **Quality Gate (Portão de Qualidade):** Regra automatizada no pipeline de CI/CD que bloqueia a esteira (Build Vermelho) se forem detectadas vulnerabilidades de alta ou crítica severidade.

---

## 🛠️ Passo 0: Pré-requisitos e Preparação Prévia do Ambiente (Explicativo)

### 🎯 O que fazer na prática
Baixar antecipadamente (24h a 48h antes da aula) o repositório e as imagens dos contêineres no Podman/Docker.

### 💻 Comandos a executar no terminal

1. **Clonar o repositório e entrar na pasta do projeto:**
```bash
git clone https://github.com/vvvpereira/devsecops-lab-cp01.git
cd devsecops-lab-cp01
```

2. **Realizar o download prévio das imagens Docker/Podman:**
```bash
podman pull docker.io/bkimminich/juice-shop:v15.0.0
podman pull docker.io/returntocorp/semgrep:latest
podman pull docker.io/bridgecrew/checkov:latest
```

3. **Confirmar a presença das imagens no cache local:**
```bash
podman images | grep -E "semgrep|checkov|juice-shop"
```

### 🗣️ Explicação Detalhada / O que falar para a turma
* "Pessoal, conforme exigido nas diretrizes do trabalho, este passo foi executado previamente para garantir a reprodutibilidade. O download antecipado evita que a apresentação falhe por congestionamento ou bloqueio da rede Wi-Fi da faculdade."
* "Usamos contêineres para que ninguém precise instalar o Semgrep ou o Checkov diretamente no sistema operacional hospedeiro. Tudo roda de forma isolada e descartável."

---

## 🚀 Passo 1: Subir o Ambiente e Validar o Alvo Vulnerável (OWASP Juice Shop)

### 🎯 O que fazer na prática
Iniciar o contêiner da aplicação vulnerável OWASP Juice Shop e testar se ela está respondendo na porta 3000.

### 💻 Comandos a executar no terminal

1. **Iniciar o contêiner em segundo plano:**
```bash
podman run -d --name juice-shop -p 3000:3000 docker.io/bkimminich/juice-shop:v15.0.0
```

2. **Verificar o status do contêiner:**
```bash
podman ps | grep juice-shop
```

3. **Testar a conectividade HTTP via terminal:**
```bash
curl -I http://localhost:3000
```

### 🔍 Detalhamento parâmetro por parâmetro
* `podman run`: Cria e executa um novo contêiner a partir de uma imagem.
* `-d` (detached): Executa em segundo plano, liberando o terminal para novos comandos.
* `--name juice-shop`: Define um nome amigável para o contêiner em vez de uma ID aleatória.
* `-p 3000:3000`: Mapeia a porta 3000 da máquina hospedeira (VM) para a porta 3000 interna do contêiner.
* `curl -I`: Traz apenas o cabeçalho (HTTP Header) da resposta.

### 🗣️ Explicação Detalhada / O que falar para a turma
* "O OWASP Juice Shop é uma aplicação web feita em Node.js intencionalmente insegura, mantida pela OWASP. Ela é um dos alvos autorizados pelo guia do trabalho para testes éticos."
* "Se o comando `curl` retornar 'HTTP/1.1 200 OK', confirmamos que o servidor web está ativo e pronto para responder a requisições locais."

---

## 🕵️‍♂️ Passo 2: Análise Estática de Código (SAST) com Semgrep

### 🎯 O que fazer na prática
Executar a varredura SAST sobre o código-fonte em `target/app.py` buscando falhas do OWASP Top 10 e credenciais expostas (*hardcoded secrets*).

### 💻 Comandos a executar no terminal

1. **Garantir que está na raiz do projeto:**
```bash
cd /home/aluno/devops-lab-cp01
```

2. **Executar o scan e exibir o resultado no terminal:**
```bash
podman run --rm -v $(pwd):/src:Z docker.io/returntocorp/semgrep semgrep scan --config=p/owasp-top-ten --config=p/secrets /src
```

3. **Gerar e salvar o relatório em formato JSON na pasta `./reports/`:**
```bash
podman run --rm -v $(pwd):/src:Z docker.io/returntocorp/semgrep semgrep scan --config=p/owasp-top-ten --config=p/secrets --json --output=/src/reports/semgrep-report.json /src
```

### 🔍 Detalhamento parâmetro por parâmetro
* `--rm`: Remove o contêiner automaticamente após a conclusão do scan (evita lixo no disco).
* `-v $(pwd):/src`: Mapeia o diretório atual do seu projeto na VM para a pasta `/src` dentro do contêiner.
* `:Z`: Flag ESSENCIAL para Podman/SELinux no Linux. Ela rotula o volume para dar permissão de leitura ao contêiner.
* `--config=p/owasp-top-ten`: Aplica o pacote oficial de regras para as 10 maiores vulnerabilidades da OWASP.
* `--config=p/secrets`: Aplica o pacote especializado na identificação de API keys, senhas e tokens gravados no código.
* `/src`: Indica ao Semgrep qual diretório interno ele deve analisar.

### 🗣️ Explicação Detalhada / O que falar para a turma
* "O Semgrep é uma ferramenta moderna de SAST rápida, multilinguagem e baseada em regras em YAML."
* "Diferente de scanners pesados tradicionais, o Semgrep analisa a Árvore de Sintaxe Abstrata (AST) do código sem precisar compilar a aplicação."
* "Reparem na saída do terminal: ele encontrou uma chave de API da Stripe inserida diretamente na linha 5 do arquivo `target/app.py`. Isso é um *Hardcoded Secret* (CWE-798)."

---

## 🏗️ Passo 3: Segurança em Infraestrutura como Código (IaC Security) com Checkov

### 🎯 O que fazer na prática
Analisar os arquivos de infraestrutura `target/Dockerfile` e `target/main.tf` em busca de más configurações de segurança.

### 💻 Comandos a executar no terminal

1. **Garantir que está na raiz do projeto:**
```bash
cd /home/aluno/devops-lab-cp01
```

2. **Executar a varredura de IaC e exibir no terminal:**
```bash
podman run --rm -v $(pwd):/tf:Z docker.io/bridgecrew/checkov --directory /tf/target
```

3. **Exportar o relatório em JSON para a pasta `./reports/`:**
```bash
podman run --rm -v $(pwd):/tf:Z docker.io/bridgecrew/checkov --directory /tf/target -o json > reports/checkov-report.json
```

### 🔍 Detalhamento parâmetro por parâmetro
* `docker.io/bridgecrew/checkov`: Imagem oficial mantida pela Bridgecrew/Prisma Cloud.
* `-v $(pwd):/tf:Z`: Monta a raiz do projeto dentro da pasta `/tf` do contêiner.
* `--directory /tf/target`: Especifica que o Checkov deve verificar exclusivamente a pasta `target/`.

### 🗣️ Explicação Detalhada / O que falar para a turma
* "O Checkov analisa estaticamente arquivos de Infraestrutura como Código (IaC), cobrindo Terraform, Dockerfile, Kubernetes e Helm."
* "Na saída do terminal, o Checkov classifica os resultados em `PASSED` e `FAILED`."
* "Ele identificou no Dockerfile a ausência da instrução `USER`. Isso significa que a aplicação dentro do contêiner roda como usuário 'root', o que viola gravemente o Princípio do Menor Privilégio."
* "No arquivo Terraform (`main.tf`), ele também detectou um Bucket S3 configurado com permissão pública de leitura."

---

## 🚧 Passo 4: Quality Gate e Automação CI/CD no GitHub Actions

### 🎯 O que fazer na prática
Mostrar na aba Actions do GitHub como as ferramentas integradas ao pipeline bloqueiam automaticamente o deploy quando há vulnerabilidades impeditivas.

### ⚙️ Estrutura dos Pipelines de CI/CD
1. **🔴 Build Vermelho (`.github/workflows/ci-red.yml`):**
   * **Execução:** Roda o Semgrep e o Checkov sem tolher os erros.
   * O Semgrep utiliza a flag `--error`, fazendo o processo encerrar com `exit code 1` ao encontrar falhas.
   * O Checkov não utiliza `--soft-fail`, falhando o job imediatamente ao detectar o erro no Dockerfile/Terraform.
   * **Resultado:** Ícone de X Vermelho no GitHub Actions.

2. **🟢 Build Verde (`.github/workflows/ci-green.yml`):**
   * **Execução:** Representa a esteira liberada após correção dos problemas ou aplicando controle de exceção.
   * **Resultado:** Ícone de Check Verde no GitHub Actions.

### 🗣️ Explicação Detalhada / O que falar para a turma
* "O Quality Gate é o 'portão de segurança' no CI/CD. Não adianta apenas gerar relatórios; o pipeline precisa interromper o build para impedir que código vulnerável vá para produção."
* "Mostrem a tela do GitHub Actions: aqui vemos o `sast-semgrep` e o `iac-checkov` falhando com `exit code 1`. Isso comprova o funcionamento do Quality Gate no Build Vermelho."

---

## 🛑 Passo 5: Encerrar o Ambiente Local

### 🎯 O que fazer na prática
Parar e remover o contêiner do Juice Shop ao finalizar o laboratório.

### 💻 Comando a executar
```bash
podman stop juice-shop && podman rm juice-shop
```

### 🗣️ Explicação Detalhada / O que falar para a turma
* "Por boas práticas de gerenciamento de ambiente, encerramos os contêineres no final da apresentação para liberar a porta 3000 e os recursos da máquina hospedeira."

---

## 📝 Perguntas de Verificação para a Turma (Entrega Individual)

### 1️⃣ PERGUNTA 1 (SAST - Semgrep):
**"Quantos achados de segurança foram reportados pelo Semgrep no arquivo `target/app.py` ao aplicar o conjunto de regras `--config=p/secrets`?"**


### 2️⃣ PERGUNTA 2 (IaC Security - Checkov):
**"Qual é a principal falha de segurança (FAILED check) apontada pelo Checkov referente ao usuário no arquivo `target/Dockerfile`?"**

---

## 💡 Dicas para Perguntas do Professor e Respostas de Defesa

<details>
<summary><b>Q1: "Por que vocês usaram SAST e IaC no laboratório em vez de DAST?"</b></summary>
<b>R:</b> "O SAST e o IaC Security atuam nos estágios de Code e Build, que são extremamente rápidos (executam em poucos segundos) e não exigem que a aplicação esteja completamente compilada ou rodando. O DAST é mais lento, precisa da aplicação ativa em ambiente de Test/Release e é complementar. Para um laboratório ao vivo de 12 minutos com a turma, SAST e IaC garantem execuções ágeis e determinísticas."
</details>

<details>
<summary><b>Q2: "O que é um Falso Positivo e como lidamos com ele no Semgrep ou Checkov?"</b></summary>
<b>R:</b> "Falso positivo ocorre quando a ferramenta aponta uma vulnerabilidade que na prática não representa um risco real (por exemplo, um segredo de teste em ambiente de staging). No Semgrep, podemos usar comentários inline como <code># nosemgrep</code> ou criar um arquivo <code>.semgrepignore</code>. No Checkov, podemos usar anotações inline no código ou configurar um arquivo <code>.checkov.yml</code> para suprimir checagens específicas."
</details>

<details>
<summary><b>Q3: "Qual a diferença entre SAST e SCA?"</b></summary>
<b>R:</b> "O SAST (ex.: Semgrep) analisa o código-fonte escrito pelos próprios desenvolvedores da empresa. O SCA (ex.: OWASP Dependency-Check) analisa as bibliotecas e dependências de terceiros importadas no projeto (como pacotes npm, pip, maven) verificando a base de CVEs conhecidas e gerando a SBOM (Software Bill of Materials)."
</details>

<details>
<summary><b>Q4: "Por que o comando do Podman usa a flag :Z no volume (-v $(pwd):/src:Z)?"</b></summary>
<b>R:</b> "A flag <code>:Z</code> ajusta o contexto de segurança do SELinux no ecossistema RedHat/Fedora/Linux. Ela instrui o sistema de segurança a conceder permissões privadas de leitura/escrita para que o contêiner consiga acessar os arquivos da máquina hospedeira sem retornar erro de 'Permission Denied'."
</details>
