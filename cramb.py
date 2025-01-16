import os
import sys
from pathlib import Path

import tomlkit

LANGUAGE = sys.argv[1]
PROJECT_NAME = sys.argv[2]
PATH_PROJETO = Path()

print(
    f"Criando ambiente para desenvolvimento do projeto: {
        PROJECT_NAME} em {LANGUAGE}!"
)


def configDotenv(project_path):
    """Cria o arquivo .env com as variáveis de ambiente."""
    try:
        project = (
            project_path / ".env"
        )
        with open(project, "w", encoding="utf-8") as file:
            file.write('API_KEY=sua-apikey')

        print(".env criado e configurado com sucesso!")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erro ao criar .env: {e}")


def addConfiguracaoToml(project_path):
    """Modifica o arquivo pyproject.toml."""
    try:
        path_toml = (
            project_path / "pyproject.toml"
        )  # Corrigido: caminho relativo ao projeto
        with open(path_toml, "r", encoding="utf-8") as file:
            content = tomlkit.parse(file.read())

        # Adiciona a configuração do autopep8
        if "tool" not in content:
            content["tool"] = tomlkit.table()
        if "autopep8" not in content["tool"]:
            content["tool"]["autopep8"] = tomlkit.table()
        content["tool"]["autopep8"]["max-line-length"] = 79

        # Adiciona a configuração do isort
        if "isort" not in content["tool"]:
            content["tool"]["isort"] = tomlkit.table()
        content["tool"]["isort"]["profile"] = "black"
        content["tool"]["isort"]["multi_line_output"] = 0
        content["tool"]["isort"]["trailing_comma"] = True
        content["tool"]["isort"]["force_grid_wrap"] = 0
        content["tool"]["isort"]["use_parentheses"] = True
        content["tool"]["isort"]["line_length"] = 79

        # Salva as alterações no arquivo
        with open(path_toml, "w", encoding="utf-8") as file:
            file.write(tomlkit.dumps(content))

        print("Versão do Python atualizada para 3.13.1!")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erro ao modificar pyproject.toml: {e}")


def ajusteVersionPythonToml(project_path):
    """Modifica o arquivo pyproject.toml para definir a versão do Python."""
    try:
        path_toml = (
            project_path / "pyproject.toml"
        )  # Corrigido: caminho relativo ao projeto
        with open(path_toml, "r", encoding="utf-8") as file:
            content = tomlkit.parse(file.read())

        # Atualiza a versão do Python
        if "requires-python" in content["project"]:
            content["project"]["requires-python"] = "<4.0,>=3.13"
        else:
            raise KeyError(
                "O campo 'requires-python' não foi encontrado no arquivo.")

        # Salva as alterações no arquivo
        with open(path_toml, "w", encoding="utf-8") as file:
            file.write(tomlkit.dumps(content))

        print("Versão do Python atualizada para 3.13.1!")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erro ao modificar pyproject.toml: {e}")


# def configSetup(project_path, project_name):
#     """Configura o setup para instalação dos modulos internos."""
#     try:
#         project = (
#             project_path / "setup.py"
#         )  # Corrigido: caminho relativo ao projeto
#         with open(project, "w", encoding="utf-8") as file:
#             file.write(
#                 f"""from setuptools import setup, find_packages

# setup(
#     name='selfe_package_{project_name.replace('-', '_')}',
#     packages=find_packages(),
# )""")

#         print("Setup.py criado e configuradocom sucesso!")

#     except (FileNotFoundError, KeyError) as e:
#         print(f"Erro ao criar setup.py: {e}")

def configPytestCov(project_path, project_name):
    """Configura o pytest para executar os comandos cov automaticamente."""
    try:
        project = (
            project_path / "pytest.ini"
        )
        with open(project, "w", encoding="utf-8") as file:
            file.write(
                f"[pytest]\naddopts = --cov={project_name.replace(
                    '-', '_')} --cov-report=html:tests/htmlcov --cov-report term-missing"
            )

        print("pytest.ini criado e configurado com sucesso!")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erro ao criar pytest.ini: {e}")


def ambientePythonUv():
    try:
        path_absoluto = PATH_PROJETO.absolute() / PROJECT_NAME
        path_relativo = PATH_PROJETO / PROJECT_NAME

        if not path_absoluto.exists():
            print(f"Iniciando script de criação do ambiente python em {
                path_relativo}")
            print("Criando projeto pelo uv...")
            os.system(f"uv init --lib {path_relativo}")

            # modificarPyprojectToml(path_relativo)

            configPytestCov(path_relativo, PROJECT_NAME)

            print("Instalando dev dependencies...")
            os.system(
                f"cd {path_relativo} \
                    && uv add --group dev pytest \
                    && uv add --group dev pytest-cov \
                    && uv add --group dev isort \
                    && uv add --group dev taskipy \
                    && uv add --group dev blue \
                    && uv add --group dev ruff"
            )
            print("dev dependencies instaladas...")
            print("Instalando doc dependencies...")
            os.system(
                f"cd {path_relativo} \
                    && uv add --group doc mkdocs-material \
                    && uv add --group doc mkdocstrings \
                    && uv add --group doc mkdocstrings-python"
            )
            print("doc dependencies instaladas...")
            print("Instalando dependencies...")

            os.system(
                f"cd {path_relativo} \
                    && uv add python-dotenv"
            )

            print("Dependencies instaladas...")

            print("Ambiente criado com sucesso!")

            addConfiguracaoToml(path_relativo)

            configDotenv(path_relativo)

            print("Configurando git...")
            os.system(f"cd {path_relativo} && ignr -p python > .gitignore")
            os.system(f"cd {path_relativo} && git init && git add .")
            os.system(
                f'cd {path_relativo} \
                    && git commit -m "Commit inicial, estrutura do projeto"'
            )
            print("Configurando GitHub...")
            os.system(f"cd {path_relativo} && gh repo create")
            print("Push para GitHub...")
        else:
            print("Projeto já existe!")

    except Exception:
        print("Erro ao criar ambiente!")


def ambientePythonPoetry():
    try:
        path_absoluto = PATH_PROJETO.absolute() / PROJECT_NAME
        path_relativo = PATH_PROJETO / PROJECT_NAME

        if not path_absoluto.exists():
            print(f"Iniciando script de criação do ambiente python \
                em {path_relativo}")
            print("Criando projeto pelo poetry...")
            os.system(f"poetry new {path_relativo}")

            print("Criando ambiente virtual .venv...")
            os.system(f"python -m venv {path_absoluto}" + R"\.venv")
            os.system(f"call {path_absoluto}" + R"\.venv\Scripts\activate")

            os.system(f"cd {path_relativo}\\{PROJECT_NAME.replace(
                '-', '_')} && mkdir src && echo. > src\\__init__.py")
            print("Configurando poetry...")
            os.system(f"cd {path_relativo} && poetry install")

            ajusteVersionPythonToml(path_relativo)

            configPytestCov(path_relativo, PROJECT_NAME)

            print("Instalando dev dependencies...")
            os.system(
                f"cd {path_relativo} \
                    && poetry add --group dev pytest \
                    && poetry add --group dev pytest-cov \
                    && poetry add --group dev isort \
                    && poetry add --group dev taskipy \
                    && poetry add --group dev blue"
            )
            print("dev dependencies instaladas...")
            print("Instalando doc dependencies...")
            os.system(
                f"cd {path_relativo} \
                    && poetry add --group doc mkdocs-material \
                    && poetry add --group doc mkdocstrings \
                    && poetry add --group doc mkdocstrings-python"
            )
            print("doc dependencies instaladas...")
            print("Instalando dependencies...")

            # os.system(
            #     f"cd {path_relativo} \
            #         && poetry add setuptools \
            #         && poetry add . --editable"
            # )

            print("Dependencies instaladas...")

            print("Ambiente criado com sucesso!")

            print("Configurando git...")
            os.system(f"cd {path_relativo} && ignr -p python > .gitignore")
            os.system(f"cd {path_relativo} && git init && git add .")
            os.system(
                f'cd {path_relativo} \
                    && git commit -m "Commit inicial, estrutura do projeto"'
            )
            print("Configurando GitHub...")
            os.system(f"cd {path_relativo} && gh repo create")
            print("Push para GitHub...")

            # os.system(
            #     f"cd {path_relativo} && git push --set-upstream github master")

        else:
            print("Projeto já existe!")

    except Exception:
        print("Erro ao criar ambiente!")


def ambienteFlutter():
    print("Iniciando script de criação do ambiente flutter")


if LANGUAGE == "python":
    ambientePythonUv()

if LANGUAGE == "flutter":
    ambienteFlutter()
