import sys
from pathlib import Path
import os
import tomlkit


LANGUAGE = sys.argv[1]
PROJECT_NAME = sys.argv[2]
PATH_PROJETO = Path()

print(
    f"Criando ambiente para desenvolvimento do projeto: {PROJECT_NAME} em {LANGUAGE}!"
)


def modificarPyprojectToml(project_path):
    """Modifica o arquivo pyproject.toml para definir a versão do Python."""
    try:
        path_toml = (
            project_path / "pyproject.toml"
        )  # Corrigido: caminho relativo ao projeto
        with open(path_toml, "r", encoding="utf-8") as file:
            content = tomlkit.parse(file.read())

        # Atualiza a versão do Python
        if "requires-python" in content["project"]:
            content["project"]["requires-python"] = "3.13.1"
        else:
            raise KeyError("O campo 'requires-python' não foi encontrado no arquivo.")

        # Salva as alterações no arquivo
        with open(path_toml, "w", encoding="utf-8") as file:
            file.write(tomlkit.dumps(content))

        print("Versão do Python atualizada para 3.13.1!")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erro ao modificar pyproject.toml: {e}")


def ambientePython():
    try:
        path_absoluto = PATH_PROJETO.absolute() / PROJECT_NAME
        path_relativo = PATH_PROJETO / PROJECT_NAME

        if not path_absoluto.exists():
            print(f"Iniciando script de criação do ambiente python em {path_relativo}")
            print("Criando projeto pelo poetry...")
            os.system(f"poetry new {path_relativo}")

            print("Criando ambiente virtual .venv...")
            os.system(f"python -m venv {path_absoluto}" + R"\.venv")
            os.system(f"call {path_absoluto}" + R"\.venv\Scripts\activate")

            print("Configurando poetry...")
            os.system(f"cd {path_relativo} && poetry install")

            modificarPyprojectToml(path_relativo)

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
            # os.system(f"cd {path_relativo} && git push --set-upstream github master")

        else:
            print("Projeto já existe!")

    except Exception:
        print("Erro ao criar ambiente!")


def ambienteFlutter():
    print("Iniciando script de criação do ambiente flutter")


if LANGUAGE == "python":
    ambientePython()

if LANGUAGE == "flutter":
    ambienteFlutter()
