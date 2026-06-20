import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import database
from datetime import datetime, timedelta

class Pergamium:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Pergamium - Sistema de Biblioteca")
        self.root.geometry("1300x800")
        self.root.configure(bg='#f5e6d3')
        
        # Cores temáticas
        self.cores = {
            'principal': '#2c1810',
            'destaque': '#8B4513',
            'sucesso': '#2d5016',
            'perigo': '#8b1a1a',
            'atencao': '#c47f17',
            'fundo': '#f5e6d3',
            'card': '#ffffff',
            'texto': '#2c1810',
            'titulo': '#f5e6d3',
            'cinza': '#95a5a6',
            'info': '#2980b9'
        }
        
        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        self.criar_header()
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Criar abas
        self.aba_livros = ttk.Frame(self.notebook)
        self.aba_usuarios = ttk.Frame(self.notebook)
        self.aba_emprestimos = ttk.Frame(self.notebook)
        self.aba_reservas = ttk.Frame(self.notebook)
        self.aba_relatorios = ttk.Frame(self.notebook)
        self.aba_config = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_livros, text="📖 Livros")
        self.notebook.add(self.aba_usuarios, text="👤 Usuários")
        self.notebook.add(self.aba_emprestimos, text="📋 Empréstimos")
        self.notebook.add(self.aba_reservas, text="🔖 Reservas")
        self.notebook.add(self.aba_relatorios, text="📊 Relatórios")
        self.notebook.add(self.aba_config, text="⚙️ Configurações")
        
        # Inicializar abas
        self.init_aba_livros()
        self.init_aba_usuarios()
        self.init_aba_emprestimos()
        self.init_aba_reservas()
        self.init_aba_relatorios()
        self.init_aba_config()
        
        # Carregar dados
        self.atualizar_tudo()
        
        # Botão atualizar global
        btn_atualizar_global = tk.Button(
            self.main_frame,
            text="🔄 Atualizar Todos os Dados",
            command=self.atualizar_tudo,
            bg=self.cores['principal'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2'
        )
        btn_atualizar_global.pack(pady=5)
    
    def criar_header(self):
        """Cria o cabeçalho do sistema"""
        header = tk.Frame(self.main_frame, bg=self.cores['principal'])
        header.pack(fill=tk.X)
        
        titulo = tk.Label(
            header,
            text="📚 PERGAMIUM",
            font=("Georgia", 22, "bold"),
            bg=self.cores['principal'],
            fg=self.cores['titulo'],
            pady=10,
            padx=20
        )
        titulo.pack(side=tk.LEFT)
        
        subtitulo = tk.Label(
            header,
            text="Sistema de Biblioteca",
            font=("Georgia", 12, "italic"),
            bg=self.cores['principal'],
            fg=self.cores['titulo'],
            pady=10
        )
        subtitulo.pack(side=tk.LEFT, padx=10)
        
        # Data e hora
        self.label_data = tk.Label(
            header,
            font=("Arial", 10),
            bg=self.cores['principal'],
            fg=self.cores['titulo'],
            pady=10,
            padx=20
        )
        self.label_data.pack(side=tk.RIGHT)
        self.atualizar_relogio()
    
    def atualizar_relogio(self):
        """Atualiza o relógio no header"""
        agora = datetime.now()
        self.label_data.config(text=agora.strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.atualizar_relogio)
    
    def atualizar_tudo(self):
        """Atualiza todos os dados do sistema"""
        self.atualizar_lista_livros()
        self.atualizar_lista_usuarios()
        self.atualizar_lista_emprestimos()
        self.atualizar_lista_reservas()
        self.atualizar_relatorios()
        self.carregar_combos()
    
    def carregar_combos(self):
        """Carrega todos os comboboxes"""
        self.carregar_livros_emprestimo()
        self.carregar_usuarios_emprestimo()
        self.carregar_livros_reserva()
        self.carregar_usuarios_reserva()
    
    # ========== ABA LIVROS ==========
    
    def init_aba_livros(self):
        """Configura a aba de livros"""
        frame = self.aba_livros
        
        # Frame de formulário
        frame_form = ttk.LabelFrame(frame, text="📖 Cadastro de Livros", padding=15)
        frame_form.pack(fill=tk.X, pady=5)
        
        # Frame para organizar em grid
        grid_frame = ttk.Frame(frame_form)
        grid_frame.pack(fill=tk.X)
        
        self.campos_livro = {}
        
        # Linha 0
        ttk.Label(grid_frame, text="Título *:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Título'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Título'].grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Autor *:", font=("Arial", 10)).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.campos_livro['Autor'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Autor'].grid(row=0, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 1
        ttk.Label(grid_frame, text="ISBN:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['ISBN'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['ISBN'].grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Editora:", font=("Arial", 10)).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.campos_livro['Editora'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Editora'].grid(row=1, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 2
        ttk.Label(grid_frame, text="Ano:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Ano'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Ano'].grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Gênero:", font=("Arial", 10)).grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.campos_livro['Gênero'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Gênero'].grid(row=2, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 3
        ttk.Label(grid_frame, text="Idioma:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Idioma'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Idioma'].grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.campos_livro['Idioma'].insert(0, 'Português')
        
        ttk.Label(grid_frame, text="Edição:", font=("Arial", 10)).grid(row=3, column=2, sticky='w', padx=5, pady=5)
        self.campos_livro['Edição'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Edição'].grid(row=3, column=3, sticky='w', padx=5, pady=5)
        self.campos_livro['Edição'].insert(0, '1')
        
        # Linha 4
        ttk.Label(grid_frame, text="Páginas:", font=("Arial", 10)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Páginas'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Páginas'].grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Localização:", font=("Arial", 10)).grid(row=4, column=2, sticky='w', padx=5, pady=5)
        self.campos_livro['Localização'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Localização'].grid(row=4, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 5
        ttk.Label(grid_frame, text="Quantidade *:", font=("Arial", 10)).grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Quantidade'] = ttk.Entry(grid_frame, width=35, font=("Arial", 10))
        self.campos_livro['Quantidade'].grid(row=5, column=1, sticky='w', padx=5, pady=5)
        self.campos_livro['Quantidade'].insert(0, '1')
        
        # Descrição (ocupa todas as colunas)
        ttk.Label(grid_frame, text="Descrição:", font=("Arial", 10)).grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.campos_livro['Descrição'] = scrolledtext.ScrolledText(grid_frame, width=80, height=4, font=("Arial", 10))
        self.campos_livro['Descrição'].grid(row=6, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        botoes = [
            ("📚 Cadastrar", self.cadastrar_livro, self.cores['sucesso']),
            ("✏️ Atualizar", self.atualizar_livro, self.cores['destaque']),
            ("🗑️ Deletar", self.deletar_livro, self.cores['perigo']),
            ("🔄 Limpar", self.limpar_campos_livro, self.cores['atencao'])
        ]
        
        for texto, comando, cor in botoes:
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                          bg=cor, fg='white', font=('Arial', 10, 'bold'),
                          padx=20, pady=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Busca
        frame_busca = ttk.LabelFrame(frame, text="🔍 Busca Avançada", padding=10)
        frame_busca.pack(fill=tk.X, pady=5)
        
        busca_frame = ttk.Frame(frame_busca)
        busca_frame.pack(fill=tk.X)
        
        ttk.Label(busca_frame, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.busca_livro = ttk.Entry(busca_frame, width=40, font=("Arial", 10))
        self.busca_livro.pack(side=tk.LEFT, padx=5)
        self.busca_livro.bind('<Return>', lambda e: self.buscar_livros())
        
        # Campos de busca
        self.busca_campos = {}
        campos_busca = ['Título', 'Autor', 'ISBN', 'Editora', 'Gênero']
        for campo in campos_busca:
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(busca_frame, text=campo, variable=var)
            chk.pack(side=tk.LEFT, padx=5)
            self.busca_campos[campo.lower()] = var
        
        btn_buscar = tk.Button(busca_frame, text="Buscar", command=self.buscar_livros,
                             bg=self.cores['destaque'], fg='white', 
                             font=('Arial', 10, 'bold'), padx=20, pady=5,
                             cursor='hand2')
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        btn_todos = tk.Button(busca_frame, text="Listar Todos", command=self.atualizar_lista_livros,
                            bg=self.cores['principal'], fg='white',
                            font=('Arial', 10, 'bold'), padx=20, pady=5,
                            cursor='hand2')
        btn_todos.pack(side=tk.LEFT, padx=5)
        
        # Lista de livros
        frame_lista = ttk.LabelFrame(frame, text="📚 Acervo de Livros", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tree_frame = ttk.Frame(frame_lista)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        colunas = ("ID", "Título", "Autor", "ISBN", "Editora", "Ano", "Gênero", 
                  "Idioma", "Edição", "Páginas", "Local", "Total", "Disp.", "Empr.")
        self.tree_livros = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=12)
        
        larguras = [40, 180, 140, 120, 120, 60, 100, 80, 60, 60, 80, 60, 60, 60]
        for col, larg in zip(colunas, larguras):
            self.tree_livros.heading(col, text=col)
            self.tree_livros.column(col, width=larg)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_livros.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_livros.xview)
        self.tree_livros.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree_livros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree_livros.bind('<ButtonRelease-1>', self.selecionar_livro)
    
    def cadastrar_livro(self):
        """Cadastra um novo livro"""
        try:
            dados = {
                'Título': self.campos_livro['Título'].get().strip(),
                'Autor': self.campos_livro['Autor'].get().strip(),
                'ISBN': self.campos_livro['ISBN'].get().strip(),
                'Editora': self.campos_livro['Editora'].get().strip(),
                'Ano': self.campos_livro['Ano'].get().strip(),
                'Gênero': self.campos_livro['Gênero'].get().strip(),
                'Idioma': self.campos_livro['Idioma'].get().strip() or 'Português',
                'Edição': self.campos_livro['Edição'].get().strip() or '1',
                'Páginas': self.campos_livro['Páginas'].get().strip(),
                'Localização': self.campos_livro['Localização'].get().strip(),
                'Quantidade': self.campos_livro['Quantidade'].get().strip() or '1',
                'Descrição': self.campos_livro['Descrição'].get('1.0', tk.END).strip()
            }
            
            if not dados['Título'] or not dados['Autor']:
                messagebox.showwarning("⚠️ Atenção", "Título e Autor são obrigatórios!")
                return
            
            try:
                ano = int(dados['Ano']) if dados['Ano'] else None
                edicao = int(dados['Edição'])
                paginas = int(dados['Páginas']) if dados['Páginas'] else None
                quantidade = int(dados['Quantidade'])
            except ValueError as e:
                messagebox.showwarning("⚠️ Atenção", f"Valor inválido: {e}")
                return
            
            if quantidade <= 0:
                messagebox.showwarning("⚠️ Atenção", "Quantidade deve ser maior que zero!")
                return
            
            sucesso, mensagem = database.inserir_livro(
                dados['Título'], dados['Autor'], dados['ISBN'],
                dados['Editora'], ano, dados['Gênero'], dados['Idioma'],
                edicao, paginas, dados['Descrição'], dados['Localização'],
                quantidade
            )
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_livro()
                self.atualizar_tudo()
            else:
                messagebox.showerror("❌ Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao cadastrar: {e}")
    
    def selecionar_livro(self, event):
        """Preenche formulário com dados do livro selecionado"""
        selecionado = self.tree_livros.selection()
        if not selecionado:
            return
        
        valores = self.tree_livros.item(selecionado[0])['values']
        if not valores:
            return
        
        self.limpar_campos_livro()
        
        mapeamento = {
            'Título': 1, 'Autor': 2, 'ISBN': 3, 'Editora': 4,
            'Ano': 5, 'Gênero': 6, 'Idioma': 7, 'Edição': 8,
            'Páginas': 9, 'Localização': 10, 'Quantidade': 12
        }
        
        for campo, idx in mapeamento.items():
            if idx < len(valores) and valores[idx]:
                self.campos_livro[campo].insert(0, str(valores[idx]))
        
        # Descrição
        conexao = database.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT descricao FROM livros WHERE id = ?', (valores[0],))
        desc = cursor.fetchone()
        if desc and desc[0]:
            self.campos_livro['Descrição'].insert('1.0', desc[0])
        conexao.close()
        
        self.livro_selecionado = valores[0]
    
    def atualizar_livro(self):
        """Atualiza dados do livro selecionado"""
        if not hasattr(self, 'livro_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um livro para atualizar!")
            return
        
        try:
            dados = {
                'Título': self.campos_livro['Título'].get().strip(),
                'Autor': self.campos_livro['Autor'].get().strip(),
                'ISBN': self.campos_livro['ISBN'].get().strip(),
                'Editora': self.campos_livro['Editora'].get().strip(),
                'Ano': self.campos_livro['Ano'].get().strip(),
                'Gênero': self.campos_livro['Gênero'].get().strip(),
                'Idioma': self.campos_livro['Idioma'].get().strip() or 'Português',
                'Edição': self.campos_livro['Edição'].get().strip() or '1',
                'Páginas': self.campos_livro['Páginas'].get().strip(),
                'Localização': self.campos_livro['Localização'].get().strip(),
                'Quantidade': self.campos_livro['Quantidade'].get().strip() or '1',
                'Descrição': self.campos_livro['Descrição'].get('1.0', tk.END).strip()
            }
            
            if not dados['Título'] or not dados['Autor']:
                messagebox.showwarning("⚠️ Atenção", "Título e Autor são obrigatórios!")
                return
            
            ano = int(dados['Ano']) if dados['Ano'] else None
            edicao = int(dados['Edição'])
            paginas = int(dados['Páginas']) if dados['Páginas'] else None
            quantidade = int(dados['Quantidade'])
            
            sucesso, mensagem = database.atualizar_livro(
                self.livro_selecionado, dados['Título'], dados['Autor'],
                dados['ISBN'], dados['Editora'], ano, dados['Gênero'],
                dados['Idioma'], edicao, paginas, dados['Descrição'],
                dados['Localização'], quantidade
            )
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_livro()
                self.atualizar_tudo()
                delattr(self, 'livro_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao atualizar: {e}")
    
    def deletar_livro(self):
        """Deleta o livro selecionado"""
        if not hasattr(self, 'livro_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um livro para deletar!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar este livro?"):
            sucesso, mensagem = database.deletar_livro(self.livro_selecionado)
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_livro()
                self.atualizar_tudo()
                if hasattr(self, 'livro_selecionado'):
                    delattr(self, 'livro_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
    
    def limpar_campos_livro(self):
        """Limpa todos os campos do formulário de livros"""
        for campo, widget in self.campos_livro.items():
            if isinstance(widget, scrolledtext.ScrolledText):
                widget.delete('1.0', tk.END)
            else:
                widget.delete(0, tk.END)
        
        self.campos_livro['Idioma'].insert(0, 'Português')
        self.campos_livro['Edição'].insert(0, '1')
        self.campos_livro['Quantidade'].insert(0, '1')
    
    def atualizar_lista_livros(self):
        """Atualiza a lista de livros"""
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        livros = database.listar_livros()
        for livro in livros:
            valores = list(livro)
            if len(str(valores[10])) > 30:
                valores[10] = str(valores[10])[:27] + '...'
            self.tree_livros.insert("", tk.END, values=valores)
    
    def buscar_livros(self):
        """Busca livros com campos selecionados"""
        termo = self.busca_livro.get().strip()
        if not termo:
            self.atualizar_lista_livros()
            return
        
        campos_selecionados = []
        for campo, var in self.busca_campos.items():
            if var.get():
                campos_selecionados.append(campo)
        
        if not campos_selecionados:
            messagebox.showwarning("⚠️ Atenção", "Selecione pelo menos um campo para busca!")
            return
        
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        livros = database.buscar_livros_avancado(termo, campos_selecionados)
        for livro in livros:
            valores = list(livro)
            if len(str(valores[10])) > 30:
                valores[10] = str(valores[10])[:27] + '...'
            self.tree_livros.insert("", tk.END, values=valores)
        
        if not livros:
            messagebox.showinfo("🔍 Busca", "Nenhum livro encontrado!")
    
    # ========== ABA USUÁRIOS ==========
    
    def init_aba_usuarios(self):
        """Configura a aba de usuários"""
        frame = self.aba_usuarios
        
        # Formulário
        frame_form = ttk.LabelFrame(frame, text="👤 Cadastro de Usuários", padding=15)
        frame_form.pack(fill=tk.X, pady=5)
        
        grid_frame = ttk.Frame(frame_form)
        grid_frame.pack(fill=tk.X)
        
        self.campos_usuario = {}
        
        # Linha 0
        ttk.Label(grid_frame, text="Nome *:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Nome'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Nome'].grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Email *:", font=("Arial", 10)).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['Email'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Email'].grid(row=0, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 1
        ttk.Label(grid_frame, text="Telefone:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Telefone'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Telefone'].grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Celular:", font=("Arial", 10)).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['Celular'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Celular'].grid(row=1, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 2
        ttk.Label(grid_frame, text="CPF:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['CPF'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['CPF'].grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="RG:", font=("Arial", 10)).grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['RG'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['RG'].grid(row=2, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 3
        ttk.Label(grid_frame, text="Data Nasc.:", font=("Arial", 10)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Nascimento'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Nascimento'].grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Profissão:", font=("Arial", 10)).grid(row=3, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['Profissão'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Profissão'].grid(row=3, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 4
        ttk.Label(grid_frame, text="Endereço:", font=("Arial", 10)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Endereço'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Endereço'].grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="Cidade:", font=("Arial", 10)).grid(row=4, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['Cidade'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Cidade'].grid(row=4, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 5
        ttk.Label(grid_frame, text="Estado:", font=("Arial", 10)).grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Estado'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['Estado'].grid(row=5, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(grid_frame, text="CEP:", font=("Arial", 10)).grid(row=5, column=2, sticky='w', padx=5, pady=5)
        self.campos_usuario['CEP'] = ttk.Entry(grid_frame, width=30, font=("Arial", 10))
        self.campos_usuario['CEP'].grid(row=5, column=3, sticky='w', padx=5, pady=5)
        
        # Linha 6
        ttk.Label(grid_frame, text="Interesses:", font=("Arial", 10)).grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Interesses'] = ttk.Entry(grid_frame, width=70, font=("Arial", 10))
        self.campos_usuario['Interesses'].grid(row=6, column=1, columnspan=3, sticky='w', padx=5, pady=5)
        
        # Linha 7
        ttk.Label(grid_frame, text="Observações:", font=("Arial", 10)).grid(row=7, column=0, sticky='w', padx=5, pady=5)
        self.campos_usuario['Observações'] = scrolledtext.ScrolledText(grid_frame, width=80, height=3, font=("Arial", 10))
        self.campos_usuario['Observações'].grid(row=7, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # Linha 8
        ttk.Label(grid_frame, text="Status:", font=("Arial", 10)).grid(row=8, column=0, sticky='w', padx=5, pady=5)
        self.status_usuario = ttk.Combobox(grid_frame, values=['ativo', 'inativo'], width=27, font=("Arial", 10))
        self.status_usuario.set('ativo')
        self.status_usuario.grid(row=8, column=1, sticky='w', padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        botoes = [
            ("👤 Cadastrar", self.cadastrar_usuario, self.cores['sucesso']),
            ("✏️ Atualizar", self.atualizar_usuario, self.cores['destaque']),
            ("🗑️ Deletar", self.deletar_usuario, self.cores['perigo']),
            ("🔄 Limpar", self.limpar_campos_usuario, self.cores['atencao'])
        ]
        
        for texto, comando, cor in botoes:
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                          bg=cor, fg='white', font=('Arial', 10, 'bold'),
                          padx=20, pady=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Busca
        frame_busca = ttk.LabelFrame(frame, text="🔍 Buscar Usuários", padding=10)
        frame_busca.pack(fill=tk.X, pady=5)
        
        busca_frame = ttk.Frame(frame_busca)
        busca_frame.pack(fill=tk.X)
        
        ttk.Label(busca_frame, text="Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.busca_usuario = ttk.Entry(busca_frame, width=50, font=("Arial", 10))
        self.busca_usuario.pack(side=tk.LEFT, padx=5)
        self.busca_usuario.bind('<Return>', lambda e: self.buscar_usuarios())
        
        btn_buscar = tk.Button(busca_frame, text="Buscar", command=self.buscar_usuarios,
                             bg=self.cores['destaque'], fg='white',
                             font=('Arial', 10, 'bold'), padx=20, pady=5,
                             cursor='hand2')
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        btn_todos = tk.Button(busca_frame, text="Listar Todos", command=self.atualizar_lista_usuarios,
                            bg=self.cores['principal'], fg='white',
                            font=('Arial', 10, 'bold'), padx=20, pady=5,
                            cursor='hand2')
        btn_todos.pack(side=tk.LEFT, padx=5)
        
        # Lista de usuários
        frame_lista = ttk.LabelFrame(frame, text="👥 Usuários Cadastrados", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tree_frame = ttk.Frame(frame_lista)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        colunas = ("ID", "Nome", "Email", "Telefone", "Celular", "Cidade", "UF", "CPF", "Status", "Empréstimos", "Multa")
        self.tree_usuarios = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=10)
        
        larguras = [40, 140, 150, 100, 100, 100, 40, 100, 70, 80, 80]
        for col, larg in zip(colunas, larguras):
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=larg)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_usuarios.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_usuarios.xview)
        self.tree_usuarios.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree_usuarios.bind('<ButtonRelease-1>', self.selecionar_usuario)
    
    def cadastrar_usuario(self):
        """Cadastra um novo usuário"""
        try:
            dados = {
                'Nome': self.campos_usuario['Nome'].get().strip(),
                'Email': self.campos_usuario['Email'].get().strip(),
                'Telefone': self.campos_usuario['Telefone'].get().strip(),
                'Celular': self.campos_usuario['Celular'].get().strip(),
                'Endereço': self.campos_usuario['Endereço'].get().strip(),
                'Cidade': self.campos_usuario['Cidade'].get().strip(),
                'Estado': self.campos_usuario['Estado'].get().strip(),
                'CEP': self.campos_usuario['CEP'].get().strip(),
                'CPF': self.campos_usuario['CPF'].get().strip(),
                'RG': self.campos_usuario['RG'].get().strip(),
                'Nascimento': self.campos_usuario['Nascimento'].get().strip(),
                'Profissão': self.campos_usuario['Profissão'].get().strip(),
                'Interesses': self.campos_usuario['Interesses'].get().strip(),
                'Observações': self.campos_usuario['Observações'].get('1.0', tk.END).strip()
            }
            
            if not dados['Nome'] or not dados['Email']:
                messagebox.showwarning("⚠️ Atenção", "Nome e Email são obrigatórios!")
                return
            
            if '@' not in dados['Email'] or '.' not in dados['Email']:
                messagebox.showwarning("⚠️ Atenção", "Email inválido!")
                return
            
            sucesso, mensagem = database.inserir_usuario(
                dados['Nome'], dados['Email'], dados['Telefone'],
                dados['Celular'], dados['Endereço'], dados['Cidade'],
                dados['Estado'], dados['CEP'], dados['CPF'], dados['RG'],
                dados['Nascimento'], dados['Profissão'], dados['Interesses'],
                dados['Observações']
            )
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_usuario()
                self.atualizar_tudo()
            else:
                messagebox.showerror("❌ Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao cadastrar: {e}")
    
    def selecionar_usuario(self, event):
        """Preenche formulário com dados do usuário selecionado"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            return
        
        valores = self.tree_usuarios.item(selecionado[0])['values']
        if not valores:
            return
        
        self.limpar_campos_usuario()
        
        mapeamento = {
            'Nome': 1, 'Email': 2, 'Telefone': 3, 'Celular': 4,
            'Endereço': 5, 'Cidade': 6, 'Estado': 7, 'CEP': 8,
            'CPF': 9, 'RG': 10, 'Nascimento': 11, 'Profissão': 12,
            'Interesses': 13
        }
        
        for campo, idx in mapeamento.items():
            if idx < len(valores) and valores[idx]:
                self.campos_usuario[campo].insert(0, str(valores[idx]))
        
        # Observações
        conexao = database.conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT observacoes FROM usuarios WHERE id = ?', (valores[0],))
        obs = cursor.fetchone()
        if obs and obs[0]:
            self.campos_usuario['Observações'].insert('1.0', obs[0])
        conexao.close()
        
        self.status_usuario.set(valores[8] if len(valores) > 8 else 'ativo')
        self.usuario_selecionado = valores[0]
    
    def atualizar_usuario(self):
        """Atualiza dados do usuário selecionado"""
        if not hasattr(self, 'usuario_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um usuário para atualizar!")
            return
        
        try:
            dados = {
                'Nome': self.campos_usuario['Nome'].get().strip(),
                'Email': self.campos_usuario['Email'].get().strip(),
                'Telefone': self.campos_usuario['Telefone'].get().strip(),
                'Celular': self.campos_usuario['Celular'].get().strip(),
                'Endereço': self.campos_usuario['Endereço'].get().strip(),
                'Cidade': self.campos_usuario['Cidade'].get().strip(),
                'Estado': self.campos_usuario['Estado'].get().strip(),
                'CEP': self.campos_usuario['CEP'].get().strip(),
                'CPF': self.campos_usuario['CPF'].get().strip(),
                'RG': self.campos_usuario['RG'].get().strip(),
                'Nascimento': self.campos_usuario['Nascimento'].get().strip(),
                'Profissão': self.campos_usuario['Profissão'].get().strip(),
                'Interesses': self.campos_usuario['Interesses'].get().strip(),
                'Observações': self.campos_usuario['Observações'].get('1.0', tk.END).strip()
            }
            
            if not dados['Nome'] or not dados['Email']:
                messagebox.showwarning("⚠️ Atenção", "Nome e Email são obrigatórios!")
                return
            
            if '@' not in dados['Email'] or '.' not in dados['Email']:
                messagebox.showwarning("⚠️ Atenção", "Email inválido!")
                return
            
            sucesso, mensagem = database.atualizar_usuario(
                self.usuario_selecionado, dados['Nome'], dados['Email'],
                dados['Telefone'], dados['Celular'], dados['Endereço'],
                dados['Cidade'], dados['Estado'], dados['CEP'], dados['CPF'],
                dados['RG'], dados['Nascimento'], dados['Profissão'],
                dados['Interesses'], self.status_usuario.get(), dados['Observações']
            )
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_usuario()
                self.atualizar_tudo()
                delattr(self, 'usuario_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao atualizar: {e}")
    
    def deletar_usuario(self):
        """Deleta o usuário selecionado"""
        if not hasattr(self, 'usuario_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um usuário para deletar!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar este usuário?"):
            sucesso, mensagem = database.deletar_usuario(self.usuario_selecionado)
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.limpar_campos_usuario()
                self.atualizar_tudo()
                delattr(self, 'usuario_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
    
    def limpar_campos_usuario(self):
        """Limpa todos os campos do formulário de usuários"""
        for campo, widget in self.campos_usuario.items():
            if isinstance(widget, scrolledtext.ScrolledText):
                widget.delete('1.0', tk.END)
            else:
                widget.delete(0, tk.END)
        
        self.status_usuario.set('ativo')
    
    def atualizar_lista_usuarios(self):
        """Atualiza a lista de usuários"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        usuarios = database.listar_usuarios()
        for usuario in usuarios:
            self.tree_usuarios.insert("", tk.END, values=usuario)
    
    def buscar_usuarios(self):
        """Busca usuários"""
        termo = self.busca_usuario.get().strip()
        if not termo:
            self.atualizar_lista_usuarios()
            return
        
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        usuarios = database.buscar_usuarios_avancado(termo)
        for usuario in usuarios:
            self.tree_usuarios.insert("", tk.END, values=usuario)
        
        if not usuarios:
            messagebox.showinfo("🔍 Busca", "Nenhum usuário encontrado!")
    
    # ========== ABA EMPRÉSTIMOS ==========
    
    def init_aba_emprestimos(self):
        """Configura a aba de empréstimos"""
        frame = self.aba_emprestimos
        
        # Frame superior - Empréstimo
        frame_emprestimo = ttk.LabelFrame(frame, text="📚 Realizar Empréstimo", padding=15)
        frame_emprestimo.pack(fill=tk.X, pady=5)
        
        grid_emp = ttk.Frame(frame_emprestimo)
        grid_emp.pack(fill=tk.X)
        
        ttk.Label(grid_emp, text="Livro:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.livro_emprestimo = ttk.Combobox(grid_emp, width=60, font=("Arial", 10))
        self.livro_emprestimo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(grid_emp, text="Usuário:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.usuario_emprestimo = ttk.Combobox(grid_emp, width=60, font=("Arial", 10))
        self.usuario_emprestimo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(grid_emp, text="Dias:", font=("Arial", 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.dias_emprestimo = ttk.Combobox(grid_emp, values=[3, 5, 7, 10, 14, 21, 30], width=57, font=("Arial", 10))
        self.dias_emprestimo.set(7)
        self.dias_emprestimo.grid(row=2, column=1, padx=5, pady=5)
        
        # Botões
        frame_botoes_emp = ttk.Frame(frame_emprestimo)
        frame_botoes_emp.pack(pady=10)
        
        btn_emprestar = tk.Button(frame_botoes_emp, text="📚 Realizar Empréstimo", command=self.realizar_emprestimo,
                                 bg=self.cores['sucesso'], fg='white',
                                 font=('Arial', 10, 'bold'), padx=30, pady=8,
                                 cursor='hand2')
        btn_emprestar.pack(side=tk.LEFT, padx=5)
        
        btn_renovar = tk.Button(frame_botoes_emp, text="🔄 Renovar Empréstimo", command=self.renovar_emprestimo,
                               bg=self.cores['atencao'], fg='white',
                               font=('Arial', 10, 'bold'), padx=30, pady=8,
                               cursor='hand2')
        btn_renovar.pack(side=tk.LEFT, padx=5)
        
        # Devolução
        frame_devolucao = ttk.LabelFrame(frame, text="📤 Devolução", padding=15)
        frame_devolucao.pack(fill=tk.X, pady=5)
        
        btn_devolver = tk.Button(frame_devolucao, text="📤 Devolver Livro Selecionado", command=self.devolver_livro,
                                bg=self.cores['destaque'], fg='white',
                                font=('Arial', 10, 'bold'), padx=30, pady=8,
                                cursor='hand2')
        btn_devolver.pack()
        
        # Lista de empréstimos
        frame_lista = ttk.LabelFrame(frame, text="📋 Histórico de Empréstimos", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tree_frame = ttk.Frame(frame_lista)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        colunas = ("ID", "Livro", "Usuário", "Empréstimo", "Devolução Prev.", "Devolução Real", "Status", "Multa", "Renov.")
        self.tree_emprestimos = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=8)
        
        larguras = [40, 180, 150, 100, 120, 100, 80, 70, 60]
        for col, larg in zip(colunas, larguras):
            self.tree_emprestimos.heading(col, text=col)
            self.tree_emprestimos.column(col, width=larg)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_emprestimos.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_emprestimos.xview)
        self.tree_emprestimos.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree_emprestimos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree_emprestimos.bind('<ButtonRelease-1>', self.selecionar_emprestimo)
    
    def carregar_livros_emprestimo(self):
        """Carrega livros disponíveis para empréstimo"""
        livros = database.listar_livros()
        opcoes = []
        for livro in livros:
            if livro[12] > 0:  # disponíveis
                opcoes.append(f"{livro[0]} - {livro[1]} ({livro[12]} disponíveis)")
        self.livro_emprestimo['values'] = opcoes
    
    def carregar_usuarios_emprestimo(self):
        """Carrega usuários ativos para empréstimo"""
        usuarios = database.listar_usuarios("status = 'ativo'")
        opcoes = []
        for usuario in usuarios:
            opcoes.append(f"{usuario[0]} - {usuario[1]} ({usuario[3]})")
        self.usuario_emprestimo['values'] = opcoes
    
    def realizar_emprestimo(self):
        """Realiza um empréstimo"""
        livro_selecionado = self.livro_emprestimo.get()
        usuario_selecionado = self.usuario_emprestimo.get()
        
        if not livro_selecionado or not usuario_selecionado:
            messagebox.showwarning("⚠️ Atenção", "Selecione um livro e um usuário!")
            return
        
        try:
            livro_id = int(livro_selecionado.split(' - ')[0])
            usuario_id = int(usuario_selecionado.split(' - ')[0])
            dias = int(self.dias_emprestimo.get())
        except:
            messagebox.showerror("❌ Erro", "Dados inválidos!")
            return
        
        sucesso, mensagem = database.realizar_emprestimo(livro_id, usuario_id, dias)
        
        if sucesso:
            messagebox.showinfo("✅ Sucesso", mensagem)
            self.atualizar_tudo()
        else:
            messagebox.showerror("❌ Erro", mensagem)
    
    def selecionar_emprestimo(self, event):
        """Seleciona um empréstimo para devolução/renovação"""
        selecionado = self.tree_emprestimos.selection()
        if not selecionado:
            return
        
        valores = self.tree_emprestimos.item(selecionado[0])['values']
        if not valores:
            return
        
        self.emprestimo_selecionado = valores[0]
    
    def devolver_livro(self):
        """Devolve um livro"""
        if not hasattr(self, 'emprestimo_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um empréstimo para devolver!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja registrar a devolução deste livro?"):
            sucesso, mensagem = database.devolver_livro(self.emprestimo_selecionado)
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.atualizar_tudo()
                delattr(self, 'emprestimo_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
    
    def renovar_emprestimo(self):
        """Renova um empréstimo"""
        if not hasattr(self, 'emprestimo_selecionado'):
            messagebox.showwarning("⚠️ Atenção", "Selecione um empréstimo para renovar!")
            return
        
        dias = messagebox.askinteger("Renovação", "Quantos dias a mais?", initialvalue=7, minvalue=1, maxvalue=30)
        
        if dias:
            sucesso, mensagem = database.renovar_emprestimo(self.emprestimo_selecionado, dias)
            
            if sucesso:
                messagebox.showinfo("✅ Sucesso", mensagem)
                self.atualizar_tudo()
                delattr(self, 'emprestimo_selecionado')
            else:
                messagebox.showerror("❌ Erro", mensagem)
    
    def atualizar_lista_emprestimos(self):
        """Atualiza a lista de empréstimos"""
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        emprestimos = database.listar_emprestimos()
        for emprestimo in emprestimos:
            self.tree_emprestimos.insert("", tk.END, values=emprestimo)
    
    # ========== ABA RESERVAS ==========
    
    def init_aba_reservas(self):
        """Configura a aba de reservas"""
        frame = self.aba_reservas
        
        # Fazer reserva
        frame_reserva = ttk.LabelFrame(frame, text="🔖 Fazer Reserva", padding=15)
        frame_reserva.pack(fill=tk.X, pady=5)
        
        grid_res = ttk.Frame(frame_reserva)
        grid_res.pack(fill=tk.X)
        
        ttk.Label(grid_res, text="Livro:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.livro_reserva = ttk.Combobox(grid_res, width=60, font=("Arial", 10))
        self.livro_reserva.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(grid_res, text="Usuário:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.usuario_reserva = ttk.Combobox(grid_res, width=60, font=("Arial", 10))
        self.usuario_reserva.grid(row=1, column=1, padx=5, pady=5)
        
        btn_reservar = tk.Button(frame_reserva, text="🔖 Realizar Reserva", command=self.realizar_reserva,
                                bg=self.cores['atencao'], fg='white',
                                font=('Arial', 10, 'bold'), padx=30, pady=8,
                                cursor='hand2')
        btn_reservar.pack(pady=10)
        
        # Lista de reservas
        frame_lista = ttk.LabelFrame(frame, text="📋 Reservas Ativas", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tree_frame = ttk.Frame(frame_lista)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        colunas = ("ID", "Livro", "Usuário", "Data Reserva", "Data Limite", "Status")
        self.tree_reservas = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=10)
        
        larguras = [40, 180, 150, 120, 120, 100]
        for col, larg in zip(colunas, larguras):
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, width=larg)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scroll_y.set)
        
        self.tree_reservas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    def carregar_livros_reserva(self):
        """Carrega livros para reserva"""
        livros = database.listar_livros()
        opcoes = []
        for livro in livros:
            if livro[12] <= 0:  # indisponíveis
                opcoes.append(f"{livro[0]} - {livro[1]} (Indisponível)")
        self.livro_reserva['values'] = opcoes
    
    def carregar_usuarios_reserva(self):
        """Carrega usuários para reserva"""
        usuarios = database.listar_usuarios("status = 'ativo'")
        opcoes = []
        for usuario in usuarios:
            opcoes.append(f"{usuario[0]} - {usuario[1]}")
        self.usuario_reserva['values'] = opcoes
    
    def realizar_reserva(self):
        """Realiza uma reserva"""
        livro_selecionado = self.livro_reserva.get()
        usuario_selecionado = self.usuario_reserva.get()
        
        if not livro_selecionado or not usuario_selecionado:
            messagebox.showwarning("⚠️ Atenção", "Selecione um livro e um usuário!")
            return
        
        livro_id = int(livro_selecionado.split(' - ')[0])
        usuario_id = int(usuario_selecionado.split(' - ')[0])
        
        sucesso, mensagem = database.realizar_reserva(livro_id, usuario_id)
        
        if sucesso:
            messagebox.showinfo("✅ Sucesso", mensagem)
            self.atualizar_tudo()
        else:
            messagebox.showerror("❌ Erro", mensagem)
    
    def atualizar_lista_reservas(self):
        """Atualiza a lista de reservas"""
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        
        reservas = database.listar_reservas()
        for reserva in reservas:
            self.tree_reservas.insert("", tk.END, values=reserva)
    
    # ========== ABA RELATÓRIOS ==========
    
    def init_aba_relatorios(self):
        """Configura a aba de relatórios"""
        frame = self.aba_relatorios
        
        # Cards de estatísticas
        frame_stats = ttk.Frame(frame)
        frame_stats.pack(fill=tk.X, pady=10)
        
        self.stats = {}
        stats_info = [
            ("total_livros", "📚 Total de Livros", self.cores['destaque']),
            ("total_exemplares", "📖 Total de Exemplares", self.cores['info']),
            ("total_disponiveis", "✅ Exemplares Disponíveis", self.cores['sucesso']),
            ("usuarios_ativos", "👤 Usuários Ativos", self.cores['info']),
            ("emprestimos_ativos", "📋 Empréstimos Ativos", self.cores['atencao']),
            ("emprestimos_atrasados", "⚠️ Empréstimos Atrasados", self.cores['perigo']),
            ("reservas_ativas", "🔖 Reservas Ativas", self.cores['destaque']),
            ("total_multas", "💰 Total em Multas", self.cores['perigo'])
        ]
        
        # Criar container para os cards
        cards_container = ttk.Frame(frame_stats)
        cards_container.pack()
        
        # Criar cards em grid (4 colunas)
        for i, (chave, texto, cor) in enumerate(stats_info):
            row = i // 4
            col = i % 4
            
            card = tk.Frame(cards_container, bg=cor, padx=15, pady=12, relief=tk.RAISED, bd=2)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            lbl_texto = tk.Label(card, text=texto, font=("Arial", 9), bg=cor, fg='white')
            lbl_texto.pack()
            
            lbl_valor = tk.Label(card, text="0", font=("Arial", 18, "bold"), bg=cor, fg='white')
            lbl_valor.pack()
            
            self.stats[chave] = lbl_valor
        
        # Botões de relatórios
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        botoes_rel = [
            ("📊 Relatório Completo", self.mostrar_relatorio_completo, self.cores['principal']),
            ("⚠️ Empréstimos Atrasados", self.mostrar_relatorio_atrasados, self.cores['perigo']),
            ("📈 Livros Mais Populares", self.mostrar_livros_populares, self.cores['destaque']),
            ("👥 Usuários Mais Ativos", self.mostrar_usuarios_ativos, self.cores['info'])
        ]
        
        for texto, comando, cor in botoes_rel:
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                          bg=cor, fg='white', font=('Arial', 10, 'bold'),
                          padx=20, pady=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Área de exibição de relatórios
        frame_relatorio = ttk.LabelFrame(frame, text="📄 Detalhes do Relatório", padding=10)
        frame_relatorio.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.texto_relatorio = scrolledtext.ScrolledText(frame_relatorio, font=("Courier", 10), height=15)
        self.texto_relatorio.pack(fill=tk.BOTH, expand=True)
        
        # Informações iniciais
        self.texto_relatorio.insert('1.0', "📊 Clique em um botão acima para visualizar relatórios detalhados.\n\n")
        self.texto_relatorio.insert('1.0', "Sistema Pergamium - Biblioteca\n")
        self.texto_relatorio.insert('1.0', "="*60 + "\n\n")
    
    def atualizar_relatorios(self):
        """Atualiza os cards de estatísticas"""
        relatorio = database.relatorio_completo()
        
        if relatorio:
            for chave in self.stats:
                if chave in relatorio:
                    valor = relatorio[chave]
                    if chave == 'total_multas':
                        self.stats[chave].config(text=f"R$ {valor:.2f}")
                    else:
                        self.stats[chave].config(text=str(valor))
    
    def mostrar_relatorio_completo(self):
        """Mostra relatório completo"""
        relatorio = database.relatorio_completo()
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', "📊 RELATÓRIO COMPLETO DO SISTEMA\n")
        self.texto_relatorio.insert('1.0', "="*60 + "\n\n")
        
        # Estatísticas gerais
        self.texto_relatorio.insert('1.0', "📈 ESTATÍSTICAS GERAIS:\n")
        self.texto_relatorio.insert('1.0', f"  Total de Livros: {relatorio.get('total_livros', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Total de Exemplares: {relatorio.get('total_exemplares', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Exemplares Disponíveis: {relatorio.get('total_disponiveis', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Usuários Ativos: {relatorio.get('usuarios_ativos', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Usuários Inativos: {relatorio.get('usuarios_inativos', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Empréstimos Ativos: {relatorio.get('emprestimos_ativos', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Empréstimos Atrasados: {relatorio.get('emprestimos_atrasados', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Reservas Ativas: {relatorio.get('reservas_ativas', 0)}\n")
        self.texto_relatorio.insert('1.0', f"  Total em Multas: R$ {relatorio.get('total_multas', 0):.2f}\n\n")
        
        # Livros mais populares
        self.texto_relatorio.insert('1.0', "📚 LIVROS MAIS POPULARES:\n")
        livros_pop = relatorio.get('livros_populares', [])
        if livros_pop:
            for i, (titulo, total) in enumerate(livros_pop[:10], 1):
                self.texto_relatorio.insert('1.0', f"  {i:2d}. {titulo[:40]:<40} - {total} empréstimos\n")
        else:
            self.texto_relatorio.insert('1.0', "  Nenhum dado disponível\n")
        self.texto_relatorio.insert('1.0', "\n")
        
        # Usuários mais ativos
        self.texto_relatorio.insert('1.0', "👥 USUÁRIOS MAIS ATIVOS:\n")
        usuarios_top = relatorio.get('usuarios_ativos_top', [])
        if usuarios_top:
            for i, (nome, total) in enumerate(usuarios_top[:10], 1):
                self.texto_relatorio.insert('1.0', f"  {i:2d}. {nome[:30]:<30} - {total} empréstimos\n")
        else:
            self.texto_relatorio.insert('1.0', "  Nenhum dado disponível\n")
        self.texto_relatorio.insert('1.0', "\n")
        
        # Empréstimos por gênero
        self.texto_relatorio.insert('1.0', "📊 LIVROS POR GÊNERO:\n")
        generos = relatorio.get('livros_por_genero', [])
        if generos:
            for genero, total in generos:
                self.texto_relatorio.insert('1.0', f"  {genero:<20} - {total} livros\n")
        else:
            self.texto_relatorio.insert('1.0', "  Nenhum dado disponível\n")
        self.texto_relatorio.insert('1.0', "\n")
        
        # Empréstimos mensais
        self.texto_relatorio.insert('1.0', "📅 EMPRÉSTIMOS POR MÊS:\n")
        mensais = relatorio.get('emprestimos_mensais', [])
        if mensais:
            for mes, total in mensais:
                self.texto_relatorio.insert('1.0', f"  {mes:<10} - {total} empréstimos\n")
        else:
            self.texto_relatorio.insert('1.0', "  Nenhum dado disponível\n")
    
    def mostrar_relatorio_atrasados(self):
        """Mostra relatório de empréstimos atrasados"""
        atrasados = database.gerar_relatorio_atrasados()
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', "⚠️ EMPRÉSTIMOS ATRASADOS\n")
        self.texto_relatorio.insert('1.0', "="*60 + "\n\n")
        
        if not atrasados:
            self.texto_relatorio.insert('1.0', "✅ Nenhum empréstimo atrasado!\n")
            return
        
        self.texto_relatorio.insert('1.0', f"Total de empréstimos atrasados: {len(atrasados)}\n\n")
        
        for emp in atrasados:
            self.texto_relatorio.insert('1.0', f"ID: {emp[0]}\n")
            self.texto_relatorio.insert('1.0', f"  Livro: {emp[1]}\n")
            self.texto_relatorio.insert('1.0', f"  Usuário: {emp[2]}\n")
            self.texto_relatorio.insert('1.0', f"  Email: {emp[3]}\n")
            self.texto_relatorio.insert('1.0', f"  Telefone: {emp[4] or 'Não informado'}\n")
            self.texto_relatorio.insert('1.0', f"  Empréstimo: {emp[5]}\n")
            self.texto_relatorio.insert('1.0', f"  Devolução Prevista: {emp[6]}\n")
            self.texto_relatorio.insert('1.0', f"  Dias Atrasado: {int(emp[7])}\n")
            self.texto_relatorio.insert('1.0', f"  Multa: R$ {emp[8]:.2f}\n")
            self.texto_relatorio.insert('1.0', "-"*40 + "\n")
    
    def mostrar_livros_populares(self):
        """Mostra os livros mais populares"""
        relatorio = database.relatorio_completo()
        livros_pop = relatorio.get('livros_populares', [])
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', "📚 LIVROS MAIS POPULARES\n")
        self.texto_relatorio.insert('1.0', "="*60 + "\n\n")
        
        if not livros_pop:
            self.texto_relatorio.insert('1.0', "Nenhum dado disponível\n")
            return
        
        for i, (titulo, total) in enumerate(livros_pop, 1):
            self.texto_relatorio.insert('1.0', f"{i:3d}º - {titulo[:50]:<50} - {total} empréstimos\n")
    
    def mostrar_usuarios_ativos(self):
        """Mostra os usuários mais ativos"""
        relatorio = database.relatorio_completo()
        usuarios_top = relatorio.get('usuarios_ativos_top', [])
        
        self.texto_relatorio.delete('1.0', tk.END)
        self.texto_relatorio.insert('1.0', "👥 USUÁRIOS MAIS ATIVOS\n")
        self.texto_relatorio.insert('1.0', "="*60 + "\n\n")
        
        if not usuarios_top:
            self.texto_relatorio.insert('1.0', "Nenhum dado disponível\n")
            return
        
        for i, (nome, total) in enumerate(usuarios_top, 1):
            self.texto_relatorio.insert('1.0', f"{i:3d}º - {nome[:35]:<35} - {total} empréstimos\n")
    
    # ========== ABA CONFIGURAÇÕES ==========
    
    def init_aba_config(self):
        """Configura a aba de configurações"""
        frame = self.aba_config
        
        ttk.Label(frame, text="⚙️ Configurações do Sistema", font=("Arial", 14, "bold")).pack(pady=10)
        
        config_frame = ttk.LabelFrame(frame, text="Parâmetros do Sistema", padding=20)
        config_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Configurações
        configs = [
            ("dias_emprestimo_padrao", "Dias padrão para empréstimo:", 0),
            ("multa_dia", "Valor da multa por dia (R$):", 1),
            ("max_emprestimos", "Máximo de empréstimos por usuário:", 2),
            ("dias_reserva", "Dias para retirar reserva:", 3)
        ]
        
        self.config_entries = {}
        
        for chave, texto, row in configs:
            ttk.Label(config_frame, text=texto, font=("Arial", 10)).grid(row=row, column=0, sticky='w', padx=10, pady=5)
            
            entry = ttk.Entry(config_frame, width=20, font=("Arial", 10))
            entry.grid(row=row, column=1, sticky='w', padx=10, pady=5)
            
            self.config_entries[chave] = entry
        
        btn_salvar = tk.Button(config_frame, text="💾 Salvar Configurações", command=self.salvar_configuracoes,
                             bg=self.cores['sucesso'], fg='white',
                             font=('Arial', 10, 'bold'), padx=20, pady=8,
                             cursor='hand2')
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Carregar configurações
        self.carregar_configuracoes()
        
        # Informações do sistema
        info_frame = ttk.LabelFrame(frame, text="ℹ️ Informações do Sistema", padding=20)
        info_frame.pack(fill=tk.X, padx=50, pady=10)
        
        info_text = """
        📚 Pergamium - Sistema de Biblioteca
        Versão: 2.0
        Desenvolvido em: Python 3.6+
        Banco de Dados: SQLite
        Interface: Tkinter
        
        © 2024 - Todos os direitos reservados
        """
        
        lbl_info = tk.Label(info_frame, text=info_text, font=("Courier", 10), justify=tk.LEFT)
        lbl_info.pack()
    
    def carregar_configuracoes(self):
        """Carrega as configurações do banco"""
        conexao = database.conectar()
        cursor = conexao.cursor()
        
        for chave in self.config_entries:
            cursor.execute('SELECT valor FROM config WHERE chave = ?', (chave,))
            resultado = cursor.fetchone()
            if resultado:
                self.config_entries[chave].delete(0, tk.END)
                self.config_entries[chave].insert(0, resultado[0])
        
        conexao.close()
    
    def salvar_configuracoes(self):
        """Salva as configurações no banco"""
        try:
            conexao = database.conectar()
            cursor = conexao.cursor()
            
            for chave, entry in self.config_entries.items():
                valor = entry.get().strip()
                if not valor:
                    messagebox.showwarning("⚠️ Atenção", f"O campo {chave} não pode ficar vazio!")
                    return
                
                try:
                    float(valor)
                except ValueError:
                    messagebox.showwarning("⚠️ Atenção", f"O campo {chave} deve ser um número!")
                    return
                
                cursor.execute('UPDATE config SET valor = ? WHERE chave = ?', (valor, chave))
            
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("✅ Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar configurações: {e}")

def main():
    database.criar_banco()
    root = tk.Tk()
    app = Pergamium(root)
    root.mainloop()

if __name__ == "__main__":
    main()