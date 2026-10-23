import tkinter as tk
from tkinter import messagebox

class TelaLogin:
    def __init__(self, janela, abrir_home):
        self.abrir_home = abrir_home
        janela.configure(bg='#2563eb')
        frame = tk.Frame(janela, bg='white', padx=35, pady=35)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(frame, text='✓ TaskFlow', font=('Arial', 28, 'bold'), fg='#2563eb', bg='white').pack(pady=(0, 10))
        tk.Label(frame, text='Organize suas tarefas com facilidade', font=('Arial', 11), fg='#64748b', bg='white').pack(pady=(0, 30))
        tk.Label(frame, text='E-mail', font=('Arial', 11, 'bold'), bg='white').pack(anchor='w')
        self.email = tk.Entry(frame, font=('Arial', 12), width=30, relief='solid', bd=1)
        self.email.pack(ipady=8, pady=(8, 20))
        tk.Label(frame, text='Senha', font=('Arial', 11, 'bold'), bg='white').pack(anchor='w')
        self.senha = tk.Entry(frame, font=('Arial', 12), width=30, show='*', relief='solid', bd=1)
        self.senha.pack(ipady=8, pady=(8, 25))
        tk.Button(frame, text='Entrar', font=('Arial', 12, 'bold'), bg='#2563eb', fg='white', activebackground='#7c3aed', activeforeground='white', width=25, pady=10, bd=0, cursor='hand2', command=self.fazer_login).pack()
        tk.Label(frame, text='TaskFlow • Versão de demonstração', font=('Arial', 10), fg='#64748b', bg='white').pack(pady=(25, 0))
        self.senha.bind('<Return>', lambda e: self.fazer_login())
        self.email.focus_set()

    def fazer_login(self):
        if not self.email.get().strip() or not self.senha.get():
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return
        self.abrir_home()
