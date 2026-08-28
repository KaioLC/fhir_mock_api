FROM python:3.10-slim

# Evita geração de .pyc e força flush imediato do stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala o gerenciador uv a partir da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copia arquivos de dependência primeiro para aproveitar cache de build
COPY pyproject.toml uv.lock* ./

# Instala dependências do projeto no ambiente do sistema do container
RUN uv pip install --system --no-cache -r pyproject.toml

# Copia o código-fonte da aplicação
COPY . .

# Expõe a porta padrão configurada na API
EXPOSE 9123

# Comando padrão de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9123"]
