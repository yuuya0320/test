import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("電卓")

        self.expression = ""  # 現在の計算式を保持する変数
        self.input_text = tk.StringVar()  # 入力されたテキストを表示する変数

        # 入力フィールドの配置
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        # 入力フィールドの設定(配置よりも下に書く)
        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), bd=10, insertwidth=4, width=30, borderwidth=4)
        input_field.grid(row=0, column=0)

        # キーボード入力のバインド
        self.root.bind('<Key>', self.key_input)  # キーボード入力をバインド
        self.root.bind('<Return>', lambda event: self.on_button_click('='))  # Enterキーで計算を実行
        self.root.bind('<BackSpace>', lambda event: self.on_button_click('⌫'))  # BackSpaceキーで削除

        # ボタンの配置
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        # ボタンの設定(配置よりも下に書く)
        buttons = [
            ['C', '⌫', '.', '*'],
            ['7', '8', '9', '/'],  
            ['4', '5', '6', '+'],  
            ['1', '2', '3', '-'],  
            ['0', '(', ')', '=']
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                button = tk.Button(button_frame, text=char, padx=20, pady=20, font=('arial', 18, 'bold'),
                                   command=lambda t=char: self.on_button_click(t))
                button.grid(row=r, column=c, sticky="nsew")

    # キーボード入力時のイベント
    def key_input(self, event):
        valid_keys = '0123456789+-*/%.()'
        if event.char in valid_keys:
            self.on_button_click(event.char)

    # ボタンクリック時のイベント
    def on_button_click(self, char):
        if char == '=':
            self.calculate_expression()
        elif char == 'C':
            self.expression = ""
            self.input_text.set("")
        elif char == '⌫':
            self.expression = self.expression[:-1]  # 最後の一文字を削除
            self.input_text.set(self.expression)
        else:
            self.expression += str(char)
            self.input_text.set(self.expression)

    # 入力された値を判定・計算する
    def calculate_expression(self):
        try:
            result = self.evaluate_expression(self.expression)
            self.input_text.set(result)
            self.expression = str(result)
        except Exception as e:
            self.input_text.set("エラー")
            self.expression = ""

    # 計算詳細
    def evaluate_expression(self, expression):
        def parse_tokens(expression):
            tokens = []
            current_number = ""
            for char in expression:
                if char.isdigit() or char == '.':
                    current_number += char
                else:
                    if current_number:
                        tokens.append(current_number)
                        current_number = ""
                    if char in '+-*/%()':
                        tokens.append(char)
            if current_number:
                tokens.append(current_number)
            return tokens

        def apply_operator(ops, values):
            right = values.pop()
            left = values.pop()
            op = ops.pop()
            if op == '+':
                values.append(left + right)
            elif op == '-':
                values.append(left - right)
            elif op == '*':
                values.append(left * right)
            elif op == '/':
                values.append(left / right)
            elif op == '%':
                values.append(left % right)

        def evaluate(tokens):
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
            values = []
            ops = []

            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token.isdigit() or '.' in token:
                    values.append(float(token) if '.' in token else int(token))
                elif token == '(':
                    ops.append(token)
                elif token == ')':
                    while ops and ops[-1] != '(':
                        apply_operator(ops, values)
                    ops.pop()
                elif token in precedence:
                    while (ops and ops[-1] in precedence and precedence[ops[-1]] >= precedence[token]):
                        apply_operator(ops, values)
                    ops.append(token)
                i += 1

            while ops:
                apply_operator(ops, values)

            return values[0]

        tokens = parse_tokens(expression)
        return evaluate(tokens)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

'''
def evaluate_expression(self, expression):について

この関数は、与えられた文字列の計算式（expression）を解析して計算する関数です。関数evaluate_expressionは3つの内部関数を使って、計算式をトークンに分解し、それを評価して計算結果を得る手順を実行します。

各内部関数の説明
1. parse_tokens関数
目的: expressionの文字列を構成要素（トークン）に分解します。

処理:

tokensリストにトークン（数値や演算子）を格納します。
current_number変数を使って、数値の文字列を一時的に保持します。
文字列expressionを1文字ずつループで処理し、数字または小数点ならcurrent_numberに追加します。それ以外（演算子や括弧）の場合は、tokensリストに追加します。
最後にtokensリストを返します。
出力:

例: "3+5*(2-8)" → ['3', '+', '5', '*', '(', '2', '-', '8', ')']

2. apply_operator関数
目的: 演算子を使って2つの数値を計算します。

処理:

opsリストから演算子を取得し（pop()）、valuesリストから2つの数値（rightとleft）を取り出します。
取得した演算子に応じて、leftとrightを計算し、その結果をvaluesリストに戻します。
例:

もし ops に '+' があり、values が [3, 5] の場合、apply_operatorはこれを 8 に計算して values に戻します。

3. evaluate関数
目的: トークンリストを評価して最終的な計算結果を得ます。

処理:

precedence辞書を使って、各演算子の優先順位を定義します。
tokensをループで処理し、数値、演算子、括弧に応じて、valuesとopsリストを適切に操作します。
数値ならvaluesリストに追加。
演算子ならopsリストに追加。ただし、優先順位を考慮し、必要に応じてapply_operatorで計算を実行。
'('はそのままopsに追加、')'が現れたら対応する '('までの計算を実行。
すべてのトークンを処理した後、opsに残っている演算子を適用し、最終的な値を返します。
出力:

例: ['3', '+', '5', '*', '(', '2', '-', '8', ')'] → -25

結論
このevaluate_expression関数は、expressionの文字列をまずparse_tokensで分解し、evaluate関数で計算処理を行い、apply_operatorを使って各ステップで演算を適用することで、最終的な計算結果を得ています。
'''
