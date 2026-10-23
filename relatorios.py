import tkinter as tk
from datetime import datetime, date, timedelta
from tarefas import listar_tarefas

AZUL = '#2563eb'
FUNDO = '#f1f5f9'

class TelaRelatorios:
    def __init__(self, janela, voltar):
        self.janela = janela
        janela.configure(bg=FUNDO)
        topo = tk.Frame(janela, bg=AZUL, height=76)
        topo.pack(fill='x')
        topo.pack_propagate(False)
        tk.Label(topo, text='✓ TaskFlow | Relatórios', font=('Arial', 20, 'bold'), bg=AZUL, fg='white').pack(side='left', padx=24, pady=18)
        tk.Button(topo, text='← Voltar', command=voltar, bg='white', fg=AZUL, bd=0, padx=15, pady=8).pack(side='right', padx=24)
        corpo = tk.Frame(janela, bg=FUNDO)
        corpo.pack(fill='both', expand=True, padx=26, pady=20)
        tk.Label(corpo, text='Visão geral da produtividade', font=('Arial', 20, 'bold'), bg=FUNDO, fg='#1e293b').pack(anchor='w')
        tk.Label(corpo, text='Resumo das tarefas cadastradas no TaskFlow', font=('Arial', 11), bg=FUNDO, fg='#64748b').pack(anchor='w', pady=(3, 16))
        cards = tk.Frame(corpo, bg=FUNDO)
        cards.pack(fill='x')
        self.valores = {}
        for i, (nome, cor) in enumerate([('Total de tarefas', AZUL), ('Concluídas', '#16a34a'), ('Pendentes', '#7c3aed'), ('Taxa de conclusão', '#0f766e')]):
            card = tk.Frame(cards, bg='white', padx=16, pady=14)
            card.grid(row=0, column=i, sticky='nsew', padx=(0, 10) if i < 3 else 0)
            cards.columnconfigure(i, weight=1)
            tk.Label(card, text=nome, bg='white', fg='#64748b', font=('Arial', 10)).pack(anchor='w')
            valor = tk.Label(card, text='0', bg='white', fg=cor, font=('Arial', 25, 'bold'))
            valor.pack(anchor='w', pady=(6, 0))
            self.valores[nome] = valor
        painel = tk.Frame(corpo, bg='white', padx=20, pady=16)
        painel.pack(fill='both', expand=True, pady=(18, 0))
        tk.Label(painel, text='Situação das tarefas', bg='white', fg='#1e293b', font=('Arial', 15, 'bold')).pack(anchor='w')
        self.grafico = tk.Canvas(painel, bg='white', highlightthickness=0, height=175)
        self.grafico.pack(fill='x', pady=(12, 16))
        tk.Label(painel, text='Tarefas agendadas para os próximos 7 dias', bg='white', fg='#1e293b', font=('Arial', 15, 'bold')).pack(anchor='w')
        self.agenda = tk.Listbox(painel, font=('Arial', 11), bg='#f8fafc', fg='#334155', bd=0, height=8)
        self.agenda.pack(fill='both', expand=True, pady=(10, 0))
        tk.Button(corpo, text='Atualizar relatórios', command=self.atualizar, bg=AZUL, fg='white', bd=0, pady=10).pack(fill='x', pady=(12, 0))
        self.atualizar()
        self.grafico.bind('<Configure>', lambda evento: self.desenhar())

    def atualizar(self):
        registros = listar_tarefas()
        self.total = len(registros)
        self.concluidas = sum(r[5] == 'Concluída' for r in registros)
        self.pendentes = self.total - self.concluidas
        percentual = round(self.concluidas / self.total * 100) if self.total else 0
        for nome, valor in [('Total de tarefas', self.total), ('Concluídas', self.concluidas), ('Pendentes', self.pendentes), ('Taxa de conclusão', f'{percentual}%')]:
            self.valores[nome].config(text=str(valor))
        self.agenda.delete(0, tk.END)
        hoje = date.today()
        proximas = []
        for r in registros:
            try:
                prazo = datetime.strptime(r[4], '%d/%m/%Y').date()
            except (ValueError, TypeError):
                continue
            if hoje <= prazo <= hoje + timedelta(days=6):
                proximas.append((prazo, r[1], r[5]))
        for prazo, titulo, status in sorted(proximas):
            self.agenda.insert(tk.END, f"{prazo:%d/%m/%Y}  •  {titulo}  ({status})")
        if not proximas:
            self.agenda.insert(tk.END, 'Nenhuma tarefa agendada para os próximos 7 dias.')
        self.desenhar()

    def desenhar(self):
        c = self.grafico
        c.delete('all')
        largura = max(c.winfo_width(), 320)
        x0, x1 = 135, largura - 65
        escala = max(self.total, 1)
        for y, nome, valor, cor in [(45, 'Concluídas', self.concluidas, '#16a34a'), (112, 'Pendentes', self.pendentes, '#7c3aed')]:
            c.create_text(12, y, text=nome, anchor='w', fill='#334155', font=('Arial', 11, 'bold'))
            c.create_rectangle(x0, y - 12, x1, y + 13, fill='#e2e8f0', outline='')
            if valor:
                c.create_rectangle(x0, y - 12, x0 + (x1-x0) * valor/escala, y + 13, fill=cor, outline='')
            c.create_text(x1 + 12, y, text=str(valor), anchor='w', fill='#334155', font=('Arial', 11, 'bold'))
