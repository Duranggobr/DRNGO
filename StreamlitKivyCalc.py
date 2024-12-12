from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout

class InvestmentCalculatorApp(App):
    def build(self):
        self.title = "Calculadora de Investimentos"
        self.layout = BoxLayout(orientation='vertical')
        self.layout.padding = [10, 10, 10, 10]  # Ajusta o padding para melhorar a usabilidade no celular

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Fundo branco
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Inputs layout
        self.input_layout = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        self.input_layout.bind(minimum_height=self.input_layout.setter('height'))

        # Inputs
        self.add_input("Investimento Inicial (R$):", "10000")
        self.add_input("Aporte Mensal (R$):", "3000")
        self.add_input("Período (meses):", "12")
        self.add_input("Selic (% a.a.):", "11.15")
        self.add_input("CDI (% a.a.):", "11.15")
        self.add_input("IPCA (% a.a.):", "4.64")
        self.add_input("Taxa de Custódia (%):", "0.20")
        self.add_input("Taxa de Administração (%):", "0.25")

        scroll = ScrollView(size_hint=(1, 0.4))
        scroll.add_widget(self.input_layout)
        self.layout.add_widget(scroll)

        # Calculate button
        self.calculate_button = Button(text="Calcular", size_hint_y=None, height=50, background_color=(0.5, 0.2, 0.8, 1), color=(1, 1, 1, 1))
        self.calculate_button.bind(on_press=self.calcular_investimentos)
        self.layout.add_widget(self.calculate_button)

        # Results layout
        self.results_layout = StackLayout(size_hint=(1, 0.5), padding=10, spacing=10)

        # Headers
        header_layout = GridLayout(cols=3, size_hint_y=None, height=40, spacing=10, padding=10)
        header_layout.add_widget(Label(text="Investimento", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=100))
        header_layout.add_widget(Label(text="Valor Líquido", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=100))
        header_layout.add_widget(Label(text="Rentabilidade Líquida (%)", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=200))

        self.results_layout.add_widget(header_layout)

        scroll_results = ScrollView(size_hint=(1, 1))
        scroll_results.add_widget(self.results_layout)
        self.layout.add_widget(scroll_results)

        return self.layout

    def add_input(self, label_text, default_value):
        self.input_layout.add_widget(Label(text=label_text, color=(0.2, 0.2, 0.6, 1)))
        text_input = TextInput(text=default_value, multiline=False, size_hint_y=None, height=40, background_color=(0.9, 0.9, 1, 1), foreground_color=(0, 0, 0, 1))
        self.input_layout.add_widget(text_input)
        setattr(self, label_text.split(" (")[0].replace(" ", "_"), text_input)

    def calcular_investimentos(self, instance):
        try:
            investimento_inicial = float(self.Investimento_Inicial.text)
            aporte_mensal = float(self.Aporte_Mensal.text)
            periodo = int(self.Período.text)
            selic = float(self.Selic.text) / 100
            cdi = float(self.CDI.text) / 100
            ipca = float(self.IPCA.text) / 100
            taxa_custodia = float(self.Taxa_de_Custódia.text) / 100
            taxa_admin = float(self.Taxa_de_Administração.text) / 100

            resultados = []

            # Cálculo dos investimentos
            total_investido = investimento_inicial + (aporte_mensal * periodo)

            # LCI e LCA
            lci_lca = total_investido * (1 + cdi * 0.85)**(periodo / 12)
            rentabilidade_lci_lca = ((lci_lca - total_investido) / total_investido) * 100
            resultados.append(("LCI e LCA", lci_lca, rentabilidade_lci_lca))

            # CDB
            cdb = total_investido * (1 + cdi)**(periodo / 12)
            rentabilidade_cdb = ((cdb - total_investido) / total_investido) * 100
            resultados.append(("CDB", cdb, rentabilidade_cdb))

            # Tesouro Selic
            selic_total = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
            rentabilidade_selic = ((selic_total - total_investido) / total_investido) * 100
            resultados.append(("Tesouro Selic", selic_total, rentabilidade_selic))

            # Fundo DI
            fundo_di = total_investido * (1 + cdi * 0.9817)**(periodo / 12) - (total_investido * taxa_admin)
            rentabilidade_fundo_di = ((fundo_di - total_investido) / total_investido) * 100
            resultados.append(("Fundo DI", fundo_di, rentabilidade_fundo_di))

            # Tesouro Prefixado
            tesouro_prefixado = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
            rentabilidade_prefixado = ((tesouro_prefixado - total_investido) / total_investido) * 100
            resultados.append(("Tesouro Prefixado", tesouro_prefixado, rentabilidade_prefixado))

            # Tesouro IPCA+
            tesouro_ipca = total_investido * (1 + ipca + 0.055)**(periodo / 12) - (total_investido * taxa_custodia)
            rentabilidade_ipca = ((tesouro_ipca - total_investido) / total_investido) * 100
            resultados.append(("Tesouro IPCA+", tesouro_ipca, rentabilidade_ipca))

            # Poupança
            poupanca = total_investido * (1 + 0.006091)**periodo
            rentabilidade_poupanca = ((poupanca - total_investido) / total_investido) * 100
            resultados.append(("Poupança", poupanca, rentabilidade_poupanca))

            # Atualiza tabela
            self.results_layout.clear_widgets()
            header_layout = GridLayout(cols=3, size_hint_y=None, height=40, spacing=10, padding=10)
            header_layout.add_widget(Label(text="Investimento", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=100))
            header_layout.add_widget(Label(text="Valor Líquido", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=100))
            header_layout.add_widget(Label(text="Rentabilidade Líquida (%)", color=(0.2, 0.2, 0.6, 1), size_hint_x=None, width=200))
            self.results_layout.add_widget(header_layout)
            for nome, valor, rentabilidade in resultados:
                result_row = GridLayout(cols=3, size_hint_y=None, height=40, spacing=10, padding=10)
                result_row.add_widget(Label(text=nome, color=(0, 0, 0, 1), size_hint_x=None, width=100))
                result_row.add_widget(Label(text=f"R$ {valor:.2f}", color=(0, 0, 0, 1), size_hint_x=None, width=100))
                result_row.add_widget(Label(text=f"{rentabilidade:.2f}%", color=(0, 0, 0, 1), size_hint_x=None, width=200))
                self.results_layout.add_widget(result_row)

        except ValueError:
            print("Erro: Verifique os valores inseridos.")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == "__main__":
    InvestmentCalculatorApp().run()
