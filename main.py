import tkinter as tk
import importlib.util
from pathlib import Path
from home import TelaInicial
from tarefas import TelaTarefas, criar_banco
from calendario import TelaCalendario
from relatorios import TelaRelatorios

PASTA = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pagina_login', PASTA / 'pagina.login.py')
modulo_login = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo_login)
TelaLogin = modulo_login.TelaLogin

class TaskFlow:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title('TaskFlow')
        criar_banco()
        self.mostrar_login()
        self.janela.mainloop()

    def limpar_tela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpar_tela()
        self.janela.geometry('450x550')
        self.janela.resizable(False, False)
        TelaLogin(self.janela, self.mostrar_home)

    def mostrar_home(self):
        self.limpar_tela()
        self.janela.resizable(True, True)
        self.janela.geometry('800x650')
        self.janela.minsize(650, 500)
        TelaInicial(self.janela, self.mostrar_tarefas, self.mostrar_login, self.mostrar_calendario, self.mostrar_relatorios)

    def mostrar_tarefas(self):
        self.limpar_tela()
        self.janela.resizable(True, True)
        self.janela.geometry('1050x700')
        self.janela.minsize(850, 550)
        TelaTarefas(self.janela, self.mostrar_home)

    def mostrar_calendario(self):
        self.limpar_tela()
        self.janela.resizable(True, True)
        self.janela.geometry('1050x700')
        self.janela.minsize(850, 600)
        TelaCalendario(self.janela, self.mostrar_home)

    def mostrar_relatorios(self):
        self.limpar_tela()
        self.janela.resizable(True, True)
        self.janela.geometry('1050x700')
        self.janela.minsize(850, 600)
        TelaRelatorios(self.janela, self.mostrar_home)

if __name__ == '__main__':
    TaskFlow()
