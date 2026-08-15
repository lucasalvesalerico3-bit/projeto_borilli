# Sistema de Cadastro de Metas

Aplicação desktop desenvolvida em Python para gerenciamento de funcionários, definição de metas e acompanhamento de resultados.

O projeto surgiu com o objetivo de desenvolver uma solução simples para centralizar o controle de metas de uma equipe, permitindo cadastrar funcionários, estabelecer objetivos, registrar resultados e acompanhar o desempenho através de dashboards e relatórios.

Esta é a **primeira versão funcional do projeto (v1.0)**.

---

## Funcionalidades

O sistema atualmente possui:

- Cadastro de funcionários
- Edição e exclusão de funcionários
- Cadastro de metas por funcionário
- Edição e exclusão de metas
- Registro de valores realizados
- Acompanhamento de metas diárias
- Dashboard para visualização de desempenho
- Relatórios de resultados
- Cálculo automático do percentual atingido
- Relatórios diários, mensais e anuais
- Configurações da aplicação
- Tema claro, escuro e acompanhamento do tema do sistema
- Banco de dados local
- Aplicação desktop executável no Linux

---

## Dashboard

O dashboard permite visualizar rapidamente informações relacionadas ao desempenho das metas cadastradas, facilitando o acompanhamento dos resultados sem precisar consultar individualmente cada registro.

---

## Relatórios

A área de relatórios permite consultar o desempenho em diferentes períodos:

- Diário
- Mensal
- Anual

O sistema compara o valor realizado com a meta definida e calcula automaticamente o percentual atingido.

---

## Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

- **Python**
- **CustomTkinter** — interface gráfica
- **SQLite** — banco de dados local
- **Pillow (PIL)** — manipulação e carregamento de imagens
- **PyInstaller** — geração do executável Linux
- **Git / GitHub** — versionamento e gerenciamento do projeto

---

## Estrutura do projeto

```text
projeto_borilli/
│
├── imagens/
│   └── arquivos utilizados pela interface
│
├── telas/
│   ├── tela_dashboard.py
│   ├── tela_funcionarios.py
│   ├── tela_metas.py
│   ├── tela_relatorios.py
│   └── tela_configuracoes.py
│
├── banco_de_dados.py
├── interface.py
├── interface.spec
└── README.md
```

---

## Armazenamento de dados

A aplicação utiliza **SQLite** como banco de dados local.

No Linux, os dados persistentes da aplicação são armazenados separadamente do executável.

Banco de dados:

```text
~/.local/share/SistemaMetas/metas.db
```

Configurações:

```text
~/.config/SistemaMetas/configuracoes.json
```

Dessa forma, os dados permanecem disponíveis mesmo quando uma nova versão do executável é gerada.

---

## Executável Linux

A aplicação pode ser empacotada utilizando o PyInstaller.

Exemplo:

```bash
pyinstaller \
  --onefile \
  --windowed \
  --hidden-import=PIL._tkinter_finder \
  --add-data "imagens:imagens" \
  interface.py
```

Após a compilação, o executável será gerado dentro do diretório:

```text
dist/
```

Os diretórios `build/` e `dist/` não fazem parte do código-fonte versionado no repositório.

---

## Sobre o desenvolvimento

Este projeto também foi utilizado como experiência prática de desenvolvimento de software, envolvendo diferentes partes do ciclo de construção de uma aplicação:

- modelagem e manipulação de banco de dados;
- implementação da lógica da aplicação;
- integração entre interface e banco de dados;
- organização modular do código;
- persistência de dados;
- construção da interface gráfica;
- empacotamento da aplicação;
- versionamento com Git;
- distribuição através do GitHub.

Embora meu foco de estudos seja **Cybersecurity**, desenvolver uma aplicação completa também permite compreender melhor como softwares são estruturados, executados e distribuídos — conhecimento importante para posteriormente estudar sua segurança de forma mais aprofundada.

---

## Próximas versões

Algumas melhorias consideradas para versões futuras:

- Suporte oficial para Windows
- Sistema de login e autenticação
- Melhorias na segurança e proteção dos dados
- Melhorias nos dashboards e relatórios
- Sistema de atualização da aplicação
- Melhor tratamento de erros
- Testes automatizados
- Melhorias gerais de arquitetura

---

## Status do projeto

**Versão:** `1.0.0`

Primeira versão funcional concluída.

O projeto continuará recebendo melhorias conforme novos conceitos forem estudados e implementados.

---

## Autor

Desenvolvido por **Lucas Alérico Alves**.

Projeto desenvolvido para fins de estudo, prática de desenvolvimento de software e construção de portfólio na área de tecnologia e Cybersecurity.
