import tkinter as tk
from tkinter import ttk
import psycopg2

class RegistroGUI:
    def __init__(self, parent):

        self.parent = parent
        self.parent.title('Registros de Pets')
        self.parent.geometry('600x400')

        frame = tk.Frame(self.parent)
        frame.pack(expand=True, fill='both')

        tree = ttk.Treeview(frame, columns=("Raça", "Nome", "Peso", "Data da Consulta", "Próxima Consulta", "Valor do Medicamento", "Valor Total"), height=10, show="headings")  
        tree.column("#1", width=90, anchor="center")  
        tree.column("#2", width=90, anchor="center")
        tree.column("#3", width=90, anchor="center")
        tree.column("#4", width=90, anchor="center")
        tree.column("#5", width=90, anchor="center")
        tree.column("#6", width=90, anchor="center")
        tree.column("#7", width=90, anchor="center")
        tree.heading('#1', text='Raça')
        tree.heading('#2', text='Nome')
        tree.heading('#3', text='Peso')
        tree.heading('#4', text='Data da Consulta')
        tree.heading('#5', text='Próxima Consulta')
        tree.heading('#6', text='Valor do Medicamento')
        tree.heading('#7', text='Valor Total')

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)

        
        conn = psycopg2.connect(user="postgres", password="estudante123", host="localhost", port="5432", database="postgres")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM public."pets"')
        records = cursor.fetchall()
        for record in records:
            tree.insert('', 'end', values=record)

        tree.pack(fill='both', expand=True)

        
        for col in ("Raça", "Nome", "Peso", "Data da Consulta", "Próxima Consulta", "Valor do Medicamento", "Valor Total"):
            tree.heading(col, command=lambda _col=col: self.sort_treeview(tree, _col, False))
            tree.column(col, width=30)

        
        tree.tag_configure("disabled", background="light gray")
        for item in tree.get_children():
            tree.item(item, tags=("disabled",))

        
        btn_fechar = tk.Button(self.parent, text="Fechar", command=self.parent.destroy)
        btn_fechar.pack(side='bottom')

    def sort_treeview(self, tree, col, reverse):
        items = [(tree.set(item, col), item) for item in tree.get_children("")]
        items.sort(reverse=reverse)
        for index, (val, item) in enumerate(items):
            tree.move(item, "", index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))
