import calendar
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from tarefas import listar_tarefas, adicionar_tarefa, atualizar_tarefa

MESES = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
         'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')

class TelaCalendario:
    def __init__(self, janela, voltar):
        self.janela = janela
        self.voltar = voltar
        self.selecionada = date.today()
        self.ano = self.selecionada.year
        self.mes = self.selecionada.month
        self.opcoes = {}
        janela.configure(bg='#f1f5f9')

        topo = tk.Frame(janela, bg='#2563eb', height=75)
        topo.pack(fill='x')
        topo.pack_propagate(False)
        tk.Label(topo, text='✓ TaskFlow | Calendário', bg='#2563eb', fg='white',
                 font=('Arial', 20, 'bold')).pack(side='left', padx=24, pady=18)
        tk.Button(topo, text='← Voltar', command=voltar, bg='white', fg='#2563eb',
                  bd=0, padx=15, pady=8, cursor='hand2').pack(side='right', padx=24)

        principal = tk.Frame(janela, bg='#f1f5f9')
        principal.pack(fill='both', expand=True, padx=22, pady=18)
        esquerda = tk.Frame(principal, bg='white', padx=18, pady=18)
        esquerda.pack(side='left', fill='both', expand=True, padx=(0, 12))
        direita = tk.Frame(principal, bg='white', padx=18, pady=18, width=340)
        direita.pack(side='right', fill='both')
        direita.pack_propagate(False)

        nav = tk.Frame(esquerda, bg='white')
        nav.pack(fill='x', pady=(0, 18))
        tk.Button(nav, text='◀', command=lambda: self.mudar_mes(-1), bg='#e2e8f0',
                  bd=0, padx=12, pady=8).pack(side='left')
        self.titulo_mes = tk.Label(nav, text='', bg='white', fg='#1e293b',
                                   font=('Arial', 17, 'bold'))
        self.titulo_mes.pack(side='left', expand=True)
        tk.Button(nav, text='▶', command=lambda: self.mudar_mes(1), bg='#e2e8f0',
                  bd=0, padx=12, pady=8).pack(side='right')

        self.grade = tk.Frame(esquerda, bg='white')
        self.grade.pack(fill='both', expand=True)
        for coluna, nome in enumerate(('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom')):
            tk.Label(self.grade, text=nome, bg='white', fg='#64748b',
                     font=('Arial', 10, 'bold')).grid(row=0, column=coluna, sticky='nsew', pady=5)
            self.grade.columnconfigure(coluna, weight=1, uniform='dias')
        for linha in range(1, 7):
            self.grade.rowconfigure(linha, weight=1)

        self.rotulo_dia = tk.Label(direita, text='', bg='white', fg='#1e293b',
                                   font=('Arial', 17, 'bold'))
        self.rotulo_dia.pack(anchor='w', pady=(0, 10))
        tk.Label(direita, text='Tarefas do dia', bg='white', fg='#64748b').pack(anchor='w')
        self.lista = tk.Listbox(direita, font=('Arial', 11), bg='#f8fafc',
                                fg='#334155', relief='flat', height=9)
        self.lista.pack(fill='both', expand=True, pady=(8, 18))
        tk.Label(direita, text='Agendar tarefa existente', bg='white',
                 fg='#1e293b', font=('Arial', 11, 'bold')).pack(anchor='w')
        self.combo = ttk.Combobox(direita, state='readonly', width=35)
        self.combo.pack(fill='x', pady=(7, 8))
        tk.Button(direita, text='Agendar no dia selecionado',
                  command=self.agendar, bg='#7c3aed', fg='white', bd=0,
                  pady=10, cursor='hand2').pack(fill='x', pady=(0, 17))
        tk.Label(direita, text='Ou criar uma nova tarefa', bg='white',
                 fg='#1e293b', font=('Arial', 11, 'bold')).pack(anchor='w')
        self.nova = ttk.Entry(direita)
        self.nova.pack(fill='x', pady=(7, 8))
        tk.Button(direita, text='+ Criar tarefa neste dia',
                  command=self.criar, bg='#2563eb', fg='white', bd=0,
                  pady=10, cursor='hand2').pack(fill='x')
        self.atualizar()

    def mudar_mes(self, deslocamento):
        indice = self.ano * 12 + self.mes - 1 + deslocamento
        self.ano, indice_mes = divmod(indice, 12)
        self.mes = indice_mes + 1
        ultimo = calendar.monthrange(self.ano, self.mes)[1]
        self.selecionada = date(self.ano, self.mes, min(self.selecionada.day, ultimo))
        self.atualizar()

    def escolher(self, dia):
        self.selecionada = date(self.ano, self.mes, dia)
        self.atualizar()

    def atualizar(self):
        registros = listar_tarefas()
        self.titulo_mes.config(text=f'{MESES[self.mes - 1]} {self.ano}')
        datas_com_tarefas = {r[4] for r in registros if r[4]}
        for widget in self.grade.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()
        semanas = calendar.monthcalendar(self.ano, self.mes)
        for linha, semana in enumerate(semanas, start=1):
            for coluna, dia in enumerate(semana):
                if not dia:
                    continue
                data_dia = date(self.ano, self.mes, dia)
                selecionado = data_dia == self.selecionada
                tem_tarefa = data_dia.strftime('%d/%m/%Y') in datas_com_tarefas
                texto = f'{dia}\n●' if tem_tarefa else str(dia)
                cor = '#2563eb' if selecionado else '#dbeafe' if tem_tarefa else '#f8fafc'
                fg = 'white' if selecionado else '#1e293b'
                tk.Button(self.grade, text=texto, bg=cor, fg=fg, bd=0,
                          font=('Arial', 11, 'bold' if selecionado else 'normal'),
                          command=lambda d=dia: self.escolher(d),
                          cursor='hand2').grid(row=linha, column=coluna,
                                               sticky='nsew', padx=3, pady=3)
        self.rotulo_dia.config(text=self.selecionada.strftime('%d/%m/%Y'))
        self.lista.delete(0, tk.END)
        dia_texto = self.selecionada.strftime('%d/%m/%Y')
        do_dia = [r for r in registros if r[4] == dia_texto]
        if not do_dia:
            self.lista.insert(tk.END, 'Nenhuma tarefa agendada.')
        for registro in do_dia:
            simbolo = '✓' if registro[5] == 'Concluída' else '○'
            self.lista.insert(tk.END, f'{simbolo} {registro[1]} ({registro[3]})')
        self.opcoes = {f'#{r[0]} - {r[1]}': r for r in registros}
        self.combo['values'] = list(self.opcoes)
        self.combo.set('')

    def agendar(self):
        registro = self.opcoes.get(self.combo.get())
        if registro is None:
            messagebox.showwarning('Atenção', 'Selecione uma tarefa existente.')
            return
        atualizar_tarefa(registro[0], registro[1], registro[2], registro[3],
                         self.selecionada.strftime('%d/%m/%Y'))
        self.atualizar()
        messagebox.showinfo('TaskFlow', 'Tarefa agendada com sucesso!')

    def criar(self):
        titulo = self.nova.get().strip()
        if not titulo:
            messagebox.showwarning('Atenção', 'Digite o nome da tarefa.')
            return
        adicionar_tarefa(titulo, prazo=self.selecionada.strftime('%d/%m/%Y'))
        self.nova.delete(0, tk.END)
        self.atualizar()
        messagebox.showinfo('TaskFlow', 'Tarefa criada e agendada!')
