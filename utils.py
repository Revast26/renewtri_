import random
import string
import re


def gerar_codigo_escola():
    """
    Gera um código aleatório para a escola.
    Exemplo: ESC-4F7K2
    """

    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choices(caracteres, k=5))

    return f"ESC-{codigo}"


def validar_cnpj(cnpj):
    """
    Validação simples de formato do CNPJ.
    Aceita:
    00.000.000/0000-00
    ou apenas números.
    """

    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    return True


def formatar_kg(valor):
    """
    Formata valores em kg.
    """

    return f"{valor:.2f} kg"