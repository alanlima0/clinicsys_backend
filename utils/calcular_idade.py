from datetime import date

def calcular_idade(data_nascimento):
    if not data_nascimento:
        return None

    # Se já for date (Django DateField)
    if isinstance(data_nascimento, date):
        nascimento = data_nascimento
    else:
        nascimento = date.fromisoformat(data_nascimento)

    hoje = date.today()

    idade = hoje.year - nascimento.year
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade
