import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

BANCO = Path(__file__).resolve().parent / 'taskflow.db'

def conectar():
    return sqlite3.connect(BANCO)

def criar_banco():
    with conectar() as con:
        con.execute('''CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            prioridade TEXT DEFAULT 'Média',
            prazo TEXT DEFAULT '',
            status TEXT DEFAULT 'Pendente'
        )''')

def listar_tarefas(filtro='Todas'):
    sql = 'SELECT id, titulo, descricao, prioridade, prazo, status FROM tarefas'
    params = ()
    if filtro == 'Pendentes':
        sql += ' WHERE status = ?'
        params = ('Pendente',)
    elif filtro == 'Concluídas':
        sql += ' WHERE status = ?'
        params = ('Concluída',)
    sql += ' ORDER BY id DESC'
    with conectar() as con:
        return con.execute(sql, params).fetchall()

def adicionar_tarefa(titulo, descricao='', prioridade='Média', prazo=''):
    with conectar() as con:
        con.execute('INSERT INTO tarefas (titulo, descricao, prioridade, prazo, status) VALUES (?, ?, ?, ?, ?)', (titulo, descricao, prioridade, prazo, 'Pendente'))

def atualizar_tarefa(id_tarefa, titulo, descricao, prioridade, prazo):
    with conectar() as con:
        con.execute('UPDATE tarefas SET titulo=?, descricao=?, prioridade=?, prazo=? WHERE id=?', (titulo, descricao, prioridade, prazo, id_tarefa))

def alterar_status(id_tarefa, status):
    with conectar() as con:
        con.execute('UPDATE tarefas SET status=? WHERE id=?', (status, id_tarefa))

def excluir_tarefa(id_tarefa):
    with conectar() as con:
        con.execute('DELETE FROM tarefas WHERE id=?', (id_tarefa,))

class TelaTarefas:
    def __init__(self, janela, voltar):
        self.janela = janela
        self.voltar = voltar
        self.id_selecionado = None
        janela.configure(bg='#f1f5f9')
        cabecalho = tk.Frame(janela, bg='#2563eb', height=75)
        cabecalho.pack(fill='x')
        cabecalho.pack_propagate(False)
        tk.Label(cabecalho, text='✓ TaskFlow | Gerenciar tarefas', font=('Arial', 20, 'bold'), bg='#2563eb', fg='white').pack(side='left', padx=24, pady=18)
        tk.Button(cabecalho, text='← Voltar', command=voltar, bg='white', fg='#2563eb', bd=0, padx=15, pady=8, cursor='hand2').pack(side='right', padx=24)

        formulario = tk.LabelFrame(janela, text=' Dados da tarefa ', bg='white', fg='#1e293b', font=('Arial', 12, 'bold'), padx=16, pady=14)
        formulario.pack(fill='x', padx=25, pady=18)
        tk.Label(formulario, text='Título', bg='white').grid(row=0, column=0, sticky='w')
        self.titulo = ttk.Entry(formulario, width=35)
        self.titulo.grid(row=1, column=0, sticky='ew', padx=(0, 12), pady=5)
        tk.Label(formulario, text='Prioridade', bg='white').grid(row=0, column=1, sticky='w')
        self.prioridade = ttk.Combobox(formulario, values=['Baixa', 'Média', 'Alta'], state='readonly', width=13)
        self.prioridade.set('Média')
        self.prioridade.grid(row=1, column=1, padx=(0, 12))
        tk.Label(formulario, text='Prazo (DD/MM/AAAA)', bg='white').grid(row=0, column=2, sticky='w')
        self.prazo = ttk.Entry(formulario, width=18)
        self.prazo.grid(row=1, column=2, sticky='ew')
        tk.Label(formulario, text='Descrição', bg='white').grid(row=2, column=0, sticky='w', pady=(10, 0))
        self.descricao = ttk.Entry(formulario)
        self.descricao.grid(row=3, column=0, columnspan=3, sticky='ew', pady=5)
        formulario.columnconfigure(0, weight=2)
        formulario.columnconfigure(2, weight=1)

        acoes = tk.Frame(janela, bg='#f1f5f9')
        acoes.pack(fill='x', padx=25)
        for texto, cor, comando in [('+ Adicionar', '#2563eb', self.adicionar), ('Salvar edição', '#7c3aed', self.editar), ('Concluir / Reabrir', '#16a34a', self.concluir), ('Excluir', '#ef4444', self.excluir), ('Limpar', '#64748b', self.limpar)]:
            tk.Button(acoes, text=texto, bg=cor, fg='white', bd=0, padx=13, pady=10, cursor='hand2', command=comando).pack(side='left', padx=(0, 8))

        filtros = tk.Frame(janela, bg='#f1f5f9')
        filtros.pack(fill='x', padx=25, pady=(16, 8))
        tk.Label(filtros, text='Minhas tarefas', bg='#f1f5f9', fg='#1e293b', font=('Arial', 17, 'bold')).pack(side='left')
        self.filtro = ttk.Combobox(filtros, values=['Todas', 'Pendentes', 'Concluídas'], state='readonly', width=17)
        self.filtro.set('Todas')
        self.filtro.pack(side='right')
        self.filtro.bind('<<ComboboxSelected>>', lambda e: self.carregar())

        tabela_frame = tk.Frame(janela, bg='white')
        tabela_frame.pack(fill='both', expand=True, padx=25, pady=(0, 10))
        colunas = ('id', 'titulo', 'descricao', 'prioridade', 'prazo', 'status')
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show='headings', selectmode='browse')
        for coluna, nome, largura in zip(colunas, ['ID', 'Tarefa', 'Descrição', 'Prioridade', 'Prazo', 'Status'], [45, 190, 240, 95, 110, 110]):
            self.tabela.heading(coluna, text=nome)
            self.tabela.column(coluna, width=largura, anchor='center')
        self.tabela.tag_configure('concluida', background='#dcfce7')
        barra = ttk.Scrollbar(tabela_frame, orient='vertical', command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.pack(side='right', fill='y')
        self.tabela.pack(fill='both', expand=True)
        self.tabela.bind('<<TreeviewSelect>>', self.selecionar)
        self.resumo = tk.Label(janela, text='', bg='#f1f5f9', fg='#64748b')
        self.resumo.pack(pady=(0, 12))
        self.carregar()

    def dados(self):
        titulo = self.titulo.get().strip()
        descricao = self.descricao.get().strip()
        prioridade = self.prioridade.get()
        prazo = self.prazo.get().strip()
        if not titulo:
            messagebox.showwarning('Atenção', 'Digite um título.')
            return None
        if prazo:
            try:
                datetime.strptime(prazo, '%d/%m/%Y')
            except ValueError:
                messagebox.showwarning('Atenção', 'Informe uma data válida em DD/MM/AAAA.')
                return None
        return titulo, descricao, prioridade, prazo

    def carregar(self):
        self.id_selecionado = None
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        registros = listar_tarefas(self.filtro.get())
        for registro in registros:
            self.tabela.insert('', 'end', values=registro, tags=('concluida',) if registro[5] == 'Concluída' else ())
        self.resumo.config(text=f'{len(registros)} tarefa(s) exibida(s)')

    def selecionar(self, evento=None):
        selecao = self.tabela.selection()
        if not selecao:
            return
        valores = self.tabela.item(selecao[0], 'values')
        self.id_selecionado = int(valores[0])
        for entrada, valor in [(self.titulo, valores[1]), (self.descricao, valores[2]), (self.prazo, valores[4])]:
            entrada.delete(0, tk.END)
            entrada.insert(0, valor)
        self.prioridade.set(valores[3])

    def limpar(self):
        self.id_selecionado = None
        for entrada in (self.titulo, self.descricao, self.prazo):
            entrada.delete(0, tk.END)
        self.prioridade.set('Média')
        for item in self.tabela.selection():
            self.tabela.selection_remove(item)

    def adicionar(self):
        dados = self.dados()
        if dados is None:
            return
        adicionar_tarefa(*dados)
        self.limpar()
        self.carregar()

    def editar(self):
        if self.id_selecionado is None:
            messagebox.showwarning('Atenção', 'Selecione uma tarefa.')
            return
        dados = self.dados()
        if dados is None:
            return
        atualizar_tarefa(self.id_selecionado, *dados)
        self.limpar()
        self.carregar()

    def concluir(self):
        if self.id_selecionado is None:
            messagebox.showwarning('Atenção', 'Selecione uma tarefa.')
            return
        with conectar() as con:
            linha = con.execute('SELECT status FROM tarefas WHERE id=?', (self.id_selecionado,)).fetchone()
        if linha:
            alterar_status(self.id_selecionado, 'Pendente' if linha[0] == 'Concluída' else 'Concluída')
        self.limpar()
        self.carregar()

    def excluir(self):
        if self.id_selecionado is None:
            messagebox.showwarning('Atenção', 'Selecione uma tarefa.')
            return
        if messagebox.askyesno('Confirmar', 'Excluir esta tarefa?'):
            excluir_tarefa(self.id_selecionado)
            self.limpar()
            self.carregar()
