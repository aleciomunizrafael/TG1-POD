class ErroCadastro(Exception):
    # cria o erro guardando o tipo, o campo e o valor que deu problema e monta a mensagem
    def __init__(self, tipo, campo, valor):
        self.tipo = tipo 
        self.campo = campo
        self.valor = valor

        mensagem = f"[{tipo}] campo '{campo}' inválido: '{valor}'"
        super().__init__(mensagem)
        