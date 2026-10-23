import tkinter as tk
from tkinter import messagebox
from tarefas import listar_tarefas, adicionar_tarefa, alterar_status, excluir_tarefa

class TelaInicial:
    def __init__(self, janela, abrir_tarefas, sair, abrir_calendario, abrir_relatorios):
        self.janela = janela
        self.ids = []
        janela.configure(bg='#f1f5f9')
        cabecalho = tk.Frame(janela, bg='#2563eb', height=100)
        cabecalho.pack(fill='x')
        cabecalho.pack_propagate(False)
        tk.Label(cabecalho, text='✓ TaskFlow', font=('Arial', 26, 'bold'), bg='#2563eb', fg='white').pack(pady=(12, 1))
        tk.Label(cabecalho, text='Organize seu dia de forma simples', font=('Arial', 11), bg='#2563eb', fg='white').pack()
        conteudo = tk.Frame(janela, bg='white', padx=25, pady=25)
        conteudo.pack(fill='both', expand=True, padx=35, pady=25)
        topo = tk.Frame(conteudo, bg='white')
        topo.pack(fill='x')
        tk.Label(topo, text='Minhas tarefas', font=('Arial', 20, 'bold'), bg='white', fg='#1e293b').pack(side='left')
        tk.Button(topo, text='Sair', command=sair, bg='#64748b', fg='white', bd=0, padx=12, pady=7).pack(side='right')
        self.resumo = tk.Label(conteudo, text='', font=('Arial', 11), bg='white', fg='#64748b')
        self.resumo.pack(anchor='w', pady=(5, 20))
        self.entrada = tk.Entry(conteudo, font=('Arial', 12), relief='solid', bd=1)
        self.entrada.pack(fill='x', ipady=9, pady=(0, 10))
        self.entrada.bind('<Return>', lambda e: self.adicionar())
        tk.Button(conteudo, text='+ Adicionar tarefa', command=self.adicionar, font=('Arial', 11, 'bold'), bg='#2563eb', fg='white', bd=0, pady=10).pack(fill='x', pady=(0, 12))
        tk.Button(conteudo, text='Gerenciar tarefas →', command=abrir_tarefas, font=('Arial', 11, 'bold'), bg='#7c3aed', fg='white', bd=0, pady=10).pack(fill='x', pady=(0, 18))
        tk.Button(conteudo, text='📅 Calendário de tarefas →', command=abrir_calendario, font=('Arial', 11, 'bold'), bg='#0f766e', fg='white', bd=0, pady=10).pack(fill='x', pady=(0, 14))
        tk.Button(conteudo, text='📊 Relatórios e produtividade →', command=abrir_relatorios, font=('Arial', 11, 'bold'), bg='#2563eb', fg='white', bd=0, pady=10).pack(fill='x', pady=(0, 14))
        area = tk.Frame(conteudo, bg='white')
        area.pack(fill='both', expand=True)
        barra = tk.Scrollbar(area)
        barra.pack(side='right', fill='y')
        self.lista = tk.Listbox(area, font=('Arial', 12), bg='#f8fafc', fg='#334155', selectbackground='#bfdbfe', selectforeground='#1e293b', relief='flat', bd=0, yscrollcommand=barra.set)
        self.lista.pack(side='left', fill='both', expand=True)
        barra.config(command=self.lista.yview)
        acoes = tk.Frame(conteudo, bg='white')
        acoes.pack(fill='x', pady=(18, 0))
        tk.Button(acoes, text='✓ Concluir / Reabrir', command=self.concluir, bg='#7c3aed', fg='white', bd=0, padx=15, pady=10).pack(side='left')
        tk.Button(acoes, text='Excluir tarefa', command=self.excluir, bg='#ef4444', fg='white', bd=0, padx=15, pady=10).pack(side='right')
        self.atualizar()
        self.entrada.focus_set()

    def atualizar(self):
        self.lista.delete(0, tk.END)
        registros = listar_tarefas()
        self.ids = [registro[0] for registro in registros]
        for registro in registros:
            simbolo = '✓' if registro[5] == 'Concluída' else '○'
            self.lista.insert(tk.END, f'{simbolo}  {registro[1]}')
        pendentes = sum(registro[5] == 'Pendente' for registro in registros)
        self.resumo.config(text=f'Pendentes: {pendentes}  |  Concluídas: {len(registros) - pendentes}')

    def adicionar(self):
        titulo = self.entrada.get().strip()
        if not titulo:
            messagebox.showwarning('Atenção', 'Digite uma tarefa!')
            return
        adicionar_tarefa(titulo)
        self.entrada.delete(0, tk.END)
        self.atualizar()

    def selecionada(self):
        selecao = self.lista.curselection()
        if not selecao:
            messagebox.showwarning('Atenção', 'Selecione uma tarefa!')
            return None
        return self.ids[selecao[0]]

    def concluir(self):
        id_tarefa = self.selecionada()
        if id_tarefa is None:
            return
        from tarefas import conectar
        with conectar() as con:
            linha = con.execute('SELECT status FROM tarefas WHERE id=?', (id_tarefa,)).fetchone()
        if linha:
            alterar_status(id_tarefa, 'Pendente' if linha[0] == 'Concluída' else 'Concluída')
        self.atualizar()

    def excluir(self):
        id_tarefa = self.selecionada()
        if id_tarefa is not None and messagebox.askyesno('Confirmar', 'Excluir esta tarefa?'):
            excluir_tarefa(id_tarefa)
            self.atualizar()
