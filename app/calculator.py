from textual.app import App
from textual.widgets import Static, Button, Footer
from textual.containers import Horizontal, Vertical

import math


class Calculator(App):
    CSS_PATH = "style.css"

    def __init__(self):
        super().__init__()
        self.expression = ""  # Armazena a expressão matemática
        self.is_result = False  # Inicia a variavel que diz se o que está sendo mostrado é um resultado.

    def compose(self):
        """Desenha os botões da calculadora.

        Yields:
            Static: Campo onde o resultado é mostrado.
            Button: Botões da calculadora.
        """
        yield Static("0", id="result")

        with Horizontal():
            yield Button("√", name="special", classes="operator")
            yield Button("π", name="special", classes="operator")
            yield Button("^", name="number", classes="operator")
            yield Button("x²", name="special", classes="operator")

        with Horizontal():
            yield Button("C", name="special", classes="cdell")
            yield Button("(", name="number", classes="operator")
            yield Button(")", name="number", classes="operator")
            yield Button("/", name="number", classes="operator")

        with Horizontal():
            yield Button("7", name="number")
            yield Button("8", name="number")
            yield Button("9", name="number")
            yield Button("*", name="number", classes="operator")

        with Horizontal():
            yield Button("4", name="number")
            yield Button("5", name="number")
            yield Button("6", name="number")
            yield Button("-", name="number", classes="operator")

        with Horizontal():
            yield Button("1", name="number")
            yield Button("2", name="number")
            yield Button("3", name="number")
            yield Button("+", name="number", classes="operator")

        with Horizontal():
            yield Button("0", name="number")
            yield Button(".", name="number")
            yield Button("del", name="special", classes="cdell")
            yield Button("=", name="special", classes="equal")
        
        yield Footer()

    def on_button_pressed(self, event):
        """Define o que cada Botão faz quando é pressionado

        Verifica qual o "tipo" do botão, se for um botão do típo número, apenas
        concatena na string self.expression, se for do tipo special executa a lógica apropriada.

        """

        button = event.button.label  # Recebe valor do botão pressionado
        type_button = event.button.name  # Recebe o "name" do botão pressionado
        result_widget = self.query_one(
            "#result", Static
        )  # Recebe o campo onde o resultado é mostrado

        if type_button == "number":
            # Esse blco "if" transforma a variável self.expression em 0 quando um botão for clicado
            # após a calculadora exibir um resultado, após isso o botão 0 deve sumir e ser subistituido
            # pelo botão clicado. Tudo isso deve ocorrer antes que o usuário chegue a ver o O.
            if self.is_result == True:
                self.expression = "0"
                result_widget.update(self.expression)

            # Se o resultado for 0 (o que deve ocorrer quando a calculadora inicia, quando o "C" é clicado,
            # qando "delete" é usado até não sobrar números, ou quando o if acima for acionado) o 0 é subistituido
            # pelo número clicado.
            if self.expression == "0":
                self.expression = button
                result_widget.update(self.expression)
                self.is_result = False

            elif (
                self.expression == "Divisão Por ZERO!!"
                or self.expression == "Sintax inválida"
            ):
                self.expression = button
                result_widget.update(self.expression)
                self.is_result = False

            else:
                self.expression += button
                result_widget.update(self.expression)
                self.is_result = False

        # Bloco que contém as regras caso o botão clicado tenha o "name" special.
        elif type_button == "special":
            if button == "C":
                self.expression = "0"
                result_widget.update(self.expression)
            elif button == "√":
                # Pega self.expression, transforma em str para que float consiga transformar em um número, depois calcula a raiz quadrada, para
                # em seguida transformar denovo em uma string e mandar para self.expression.
                self.expression = str(math.sqrt(float(str(self.expression))))
                result_widget.update(self.expression)
                self.is_result = True

            elif button == "π":
                # Valida se o mostrador está vazio, se sim ele adiciona o PI, se não ele multiplica o valor por PI, caso possua uma operação, ele
                # adiciona Pi a operação
                if self.expression == "" or self.expression == "0":
                    self.expression = str(math.pi)
                    result_widget.update(self.expression)
                    self.is_result = False
                else:
                    try:
                        self.expression = str(float(str(self.expression)) * math.pi)
                        result_widget.update(self.expression)
                        self.is_result = True
                    except:
                        self.expression += str(math.pi)
                        result_widget.update(self.expression)
                        self.is_result = False

            # tenta resolver a expressão usando eval
            elif button == "=":
                try:
                    # "^" não é tratado pelo eval como potenciação, então o  tratamento é necessário.
                    self.expression = str(eval(str(self.expression).replace("^", "**")))
                    result_widget.update(self.expression)
                    self.is_result = True

                except ZeroDivisionError:
                    self.expression = "Divisão Por ZERO!!"
                    result_widget.update(self.expression)
                    self.is_result = True

                except:
                    self.expression = "Sintax inválida"
                    result_widget.update(self.expression)
                    self.is_result = True

            elif button == "x²":
                self.expression = str(math.pow(float(str(self.expression)), 2))
                result_widget.update(self.expression)
                self.is_result = True

            # deleta o último número da expressão até sobrar um, quando isso ocorre ele coloca um 0
            elif button == "del":
                if len(self.expression) == 1:
                    self.expression = "0"
                    result_widget.update(self.expression)

                else:
                    self.expression = str(self.expression)[:-1]
                    result_widget.update(self.expression)


if __name__ == "__main__":
    Calculator().run()
