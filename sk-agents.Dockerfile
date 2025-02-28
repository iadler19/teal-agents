FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl git \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 skagent && \
    useradd -g 1000 -u 1000 -m skagent && \
    mkdir /app && \
    chown -R skagent:skagent /app

USER skagent

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH=$PATH:/home/skagent/.local/bin

WORKDIR /app

COPY --chown=skagent:skagent shared/ska_utils /app/shared/ska_utils
COPY --chown=skagent:skagent src/sk-agents /app/src/sk-agents

WORKDIR /app/src/sk-agents

RUN uv sync --frozen --no-dev

EXPOSE 8000

RUN chmod +x sk_agents.sh

ENTRYPOINT ["./sk_agents.sh"]