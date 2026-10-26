# Passo a Passo de Execução e Publicação

Este guia resume os passos para executar as consultas no MongoDB, coletar os prints e publicar o projeto no seu repositório pessoal do GitHub.

---

## 1. Configurar as Credenciais no `.env`

Crie um arquivo `.env` na raiz do projeto (`c:\Users\felip\GitHubAllan\.env`) com base no `.env.example`:

```env
MONGO_URI=mongodb://root:<SENHA_FORNECIDA>@<HOST_FORNECIDO>:27017/?authSource=admin
MONGO_DB=iot
MONGO_COLLECTION=sensores
```

> **Nota:** As credenciais (`<SENHA_FORNECIDA>` e `<HOST_FORNECIDO>`) foram disponibilizadas pelo professor Allan / grupo da disciplina.

---

## 2. Executar a Leitura dos Sensores no MongoDB

Com as dependências já instaladas (`pymongo`, `python-dotenv`), execute no terminal:

```bash
python consulta_mongo.py 10
```

- Este script traz as últimas 10 leituras da coleção `iot.sensores` e fica escutando em tempo real a cada 2 segundos.
- **Tire um print da tela do terminal** mostrando as leituras de temperatura e umidade para anexar ao seu artigo.

---

## 3. Publicar no seu Repositório Pessoal do GitHub

Para enviar o código para o seu próprio GitHub:

1. Crie um novo repositório vazio na sua conta do GitHub (ex: `PI-SEXTO-TERMO-IOT`).
2. No terminal do VS Code, altere a URL do repositório remoto para o seu link pessoal:

```bash
git remote set-url origin https://github.com/<SEU_USUARIO>/<SEU_REPOSITORIO>.git
```

3. Adicione as alterações e faça o commit:

```bash
git add .
git commit -m "feat: configuracao do ambiente, scripts de consulta e modelo de artigo"
```

4. Envie para o seu GitHub pessoal:

```bash
git push -u origin main
```

---

## 4. Publicar o Artigo no LinkedIn

O arquivo [ARTIGO_LINKEDIN.md](file:///c:/Users/felip/GitHubAllan/ARTIGO_LINKEDIN.md) já está redigido no padrão do artigo do Pedro Henrique Ribeiro dos Santos.

1. Abra o [ARTIGO_LINKEDIN.md](file:///c:/Users/felip/GitHubAllan/ARTIGO_LINKEDIN.md).
2. Cole os prints das leituras obtidas no passo 2.
3. No LinkedIn, clique em **"Escrever artigo"** (Pulse) ou publique como um post no feed com as imagens e hashtags sugeridas.
