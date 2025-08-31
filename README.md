# BPJS-QA

BPJS-QA is a system that uses Retrieval-Augmented Generation (RAG) to answer questions about BPJS. It retrieves relevant information from a knowledge base and uses it to generate accurate responses.

![BPJS-QA](./screenshoot-bpjsqa.png)

## Model

You may use some models, free or paid. But, in this case, I use `google/gemma-3-27b-it:free` model from [OpenRouterAI](https://openrouter.ai).

![alt text](./rag-flow.png)

## Installing `uv`

Install uv with our standalone installers:

```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or, from PyPI:

```
# With pip.
pip install uv
```

```
# Or pipx.
pipx install uv
```

## Running the project

- Clone the project using command `git clone <repository>`
- Add `.env`
  ```
  MYSQL_HOST=
  MYSQL_PORT=
  MYSQL_USERNAME=
  MYSQL_PASSWORD=
  MYSQL_DATABASE=
  MYSQL_CERT_PATH=
  OLLAMA_HOST=
  OLLAMA_MODEL=
  OLLAMA_API_URL=
  SENTENCE_TRANSFORMER_MODEL=
  OPENROUTER_API_URL=
  OPENROUTER_API_KEY=
  OPENROUTER_MODEL=
  ```
- Create folder `data` and add `bpjs_kb.csv`
- Install libraries using command `uv sync`
- Run the command `flask --app app.py --debug run`
