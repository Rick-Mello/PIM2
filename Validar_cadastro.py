def validar_cadastro (nome, email, senha):
    if not nome or not email or not senha:
        return "Preencha todos os campos!"
    if not nome.replace(" ", "").isalpha():
        return "O nome deve conter apenas letras!"
    if "@" not in email:
        return "E-mail inválido!"
    return f"Usuário {nome} cadastrado com sucesso!"