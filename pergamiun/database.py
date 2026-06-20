import sqlite3
from datetime import datetime, timedelta

DATABASE = 'pergamium.db'

def criar_banco():
    """Cria todas as tabelas do sistema Pergamium"""
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    
    # Tabela de livros (com todas as colunas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE,
            editora TEXT,
            ano INTEGER,
            genero TEXT,
            idioma TEXT DEFAULT 'Português',
            edicao INTEGER DEFAULT 1,
            paginas INTEGER,
            descricao TEXT,
            localizacao TEXT,
            quantidade INTEGER DEFAULT 1,
            disponiveis INTEGER DEFAULT 1,
            emprestimos_total INTEGER DEFAULT 0,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_emprestimo DATE,
            status TEXT DEFAULT 'ativo'
        )
    ''')
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            celular TEXT,
            endereco TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT,
            cpf TEXT UNIQUE,
            rg TEXT,
            data_nascimento DATE,
            profissao TEXT,
            interesses TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'ativo',
            emprestimos_total INTEGER DEFAULT 0,
            multas_pendentes REAL DEFAULT 0,
            ultimo_emprestimo DATE,
            observacoes TEXT
        )
    ''')
    
    # Tabela de empréstimos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_emprestimo DATE NOT NULL,
            data_devolucao_prevista DATE NOT NULL,
            data_devolucao_real DATE,
            status TEXT DEFAULT 'ativo',
            multa REAL DEFAULT 0,
            renovacoes INTEGER DEFAULT 0,
            observacao TEXT,
            FOREIGN KEY(livro_id) REFERENCES livros(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabela de reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_limite DATE,
            status TEXT DEFAULT 'ativa',
            FOREIGN KEY(livro_id) REFERENCES livros(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabela de histórico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emprestimo_id INTEGER,
            usuario_id INTEGER,
            livro_id INTEGER,
            acao TEXT NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            detalhes TEXT,
            FOREIGN KEY(emprestimo_id) REFERENCES emprestimos(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    ''')
    
    # Tabela de configurações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            chave TEXT PRIMARY KEY,
            valor TEXT,
            descricao TEXT
        )
    ''')
    
    # Inserir configurações padrão
    configs = [
        ('dias_emprestimo_padrao', '7', 'Dias padrão para empréstimo'),
        ('multa_dia', '2.00', 'Valor da multa por dia de atraso'),
        ('max_emprestimos', '5', 'Máximo de empréstimos por usuário'),
        ('dias_reserva', '3', 'Dias para retirar reserva'),
        ('taxa_renovacao', '1.00', 'Taxa para renovação'),
        ('notificacao_dias', '2', 'Dias antes para notificar devolução')
    ]
    
    for chave, valor, descricao in configs:
        cursor.execute('''
            INSERT OR IGNORE INTO config (chave, valor, descricao)
            VALUES (?, ?, ?)
        ''', (chave, valor, descricao))
    
    # Criar índices para performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_emprestimos_status ON emprestimos(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_emprestimos_datas ON emprestimos(data_emprestimo, data_devolucao_prevista)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_livros_titulo ON livros(titulo)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_livros_autor ON livros(autor)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_nome ON usuarios(nome)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)')
    
    conexao.commit()
    conexao.close()
    print("📚 Banco de dados Pergamium criado com sucesso!")

def atualizar_banco():
    """Atualiza o banco de dados com novas colunas (para versões antigas)"""
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Lista de colunas para adicionar
    colunas = [
        ('idioma', "TEXT DEFAULT 'Português'"),
        ('edicao', "INTEGER DEFAULT 1"),
        ('paginas', "INTEGER"),
        ('descricao', "TEXT"),
        ('localizacao', "TEXT"),
        ('emprestimos_total', "INTEGER DEFAULT 0"),
        ('ultimo_emprestimo', "DATE"),
        ('status', "TEXT DEFAULT 'ativo'")
    ]
    
    for coluna, tipo in colunas:
        try:
            cursor.execute(f"ALTER TABLE livros ADD COLUMN {coluna} {tipo}")
            print(f"✅ Coluna '{coluna}' adicionada!")
        except sqlite3.OperationalError:
            pass  # Coluna já existe
    
    conexao.commit()
    conexao.close()
    print("✅ Banco de dados atualizado com sucesso!")

def conectar():
    return sqlite3.connect(DATABASE)

# ========== FUNÇÕES PARA LIVROS ==========

def inserir_livro(titulo, autor, isbn, editora, ano, genero, idioma, edicao, 
                  paginas, descricao, localizacao, quantidade):
    """Insere um novo livro com todos os campos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO livros (
                titulo, autor, isbn, editora, ano, genero, idioma, edicao,
                paginas, descricao, localizacao, quantidade, disponiveis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, autor, isbn, editora, ano, genero, idioma, edicao,
              paginas, descricao, localizacao, quantidade, quantidade))
        
        livro_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO historico (livro_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (livro_id, 'cadastro_livro', f'Livro "{titulo}" cadastrado'))
        
        conexao.commit()
        conexao.close()
        return True, f"✅ Livro '{titulo}' cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ ISBN já cadastrado!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def listar_livros(filtro=None):
    """Lista livros com opção de filtro"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        if filtro:
            query = f"""
                SELECT * FROM livros 
                WHERE {filtro}
                ORDER BY id DESC
            """
            cursor.execute(query)
        else:
            cursor.execute('SELECT * FROM livros ORDER BY id DESC')
        
        livros = cursor.fetchall()
        conexao.close()
        return livros
    except Exception as e:
        print(f"Erro ao listar livros: {e}")
        return []

def buscar_livros_avancado(termo, campos=None):
    """Busca avançada em múltiplos campos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        if not campos:
            campos = ['titulo', 'autor', 'isbn', 'editora', 'genero']
        
        condicoes = []
        for campo in campos:
            condicoes.append(f"{campo} LIKE ?")
        
        where_clause = " OR ".join(condicoes)
        params = [f'%{termo}%'] * len(campos)
        
        query = f"SELECT * FROM livros WHERE {where_clause} ORDER BY titulo"
        cursor.execute(query, params)
        
        livros = cursor.fetchall()
        conexao.close()
        return livros
    except Exception as e:
        print(f"Erro na busca avançada: {e}")
        return []

def atualizar_livro(id, titulo, autor, isbn, editora, ano, genero, idioma, 
                   edicao, paginas, descricao, localizacao, quantidade):
    """Atualiza todos os dados de um livro"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT disponiveis, quantidade FROM livros WHERE id = ?', (id,))
        dados_atuais = cursor.fetchone()
        
        if not dados_atuais:
            return False, "❌ Livro não encontrado!"
        
        disponiveis_atual = dados_atuais[0]
        quantidade_atual = dados_atuais[1]
        
        diferenca = quantidade - quantidade_atual
        novos_disponiveis = disponiveis_atual + diferenca
        
        if novos_disponiveis < 0:
            return False, "❌ Não é possível reduzir a quantidade abaixo dos exemplares emprestados!"
        
        cursor.execute('''
            UPDATE livros 
            SET titulo = ?, autor = ?, isbn = ?, editora = ?, ano = ?, 
                genero = ?, idioma = ?, edicao = ?, paginas = ?,
                descricao = ?, localizacao = ?, quantidade = ?, disponiveis = ?
            WHERE id = ?
        ''', (titulo, autor, isbn, editora, ano, genero, idioma, edicao,
              paginas, descricao, localizacao, quantidade, novos_disponiveis, id))
        
        cursor.execute('''
            INSERT INTO historico (livro_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (id, 'atualizacao_livro', f'Livro "{titulo}" atualizado'))
        
        conexao.commit()
        conexao.close()
        return True, "✅ Livro atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ ISBN já cadastrado para outro livro!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def deletar_livro(id):
    """Remove um livro com verificação de empréstimos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE livro_id = ? AND status = "ativo"', (id,))
        if cursor.fetchone()[0] > 0:
            return False, "❌ Não é possível deletar livro com empréstimos ativos!"
        
        cursor.execute('SELECT COUNT(*) FROM reservas WHERE livro_id = ? AND status = "ativa"', (id,))
        if cursor.fetchone()[0] > 0:
            return False, "❌ Não é possível deletar livro com reservas ativas!"
        
        cursor.execute('SELECT titulo FROM livros WHERE id = ?', (id,))
        titulo = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
        
        cursor.execute('''
            INSERT INTO historico (livro_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (id, 'exclusao_livro', f'Livro "{titulo}" removido'))
        
        conexao.commit()
        conexao.close()
        return True, "✅ Livro removido com sucesso!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

# ========== FUNÇÕES PARA USUÁRIOS ==========

def inserir_usuario(nome, email, telefone, celular, endereco, cidade, estado,
                   cep, cpf, rg, data_nascimento, profissao, interesses, observacoes):
    """Insere um novo usuário com todos os campos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO usuarios (
                nome, email, telefone, celular, endereco, cidade, estado,
                cep, cpf, rg, data_nascimento, profissao, interesses, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, celular, endereco, cidade, estado,
              cep, cpf, rg, data_nascimento, profissao, interesses, observacoes))
        
        usuario_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO historico (usuario_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (usuario_id, 'cadastro_usuario', f'Usuário "{nome}" cadastrado'))
        
        conexao.commit()
        conexao.close()
        return True, f"✅ Usuário '{nome}' cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        if 'email' in str(e):
            return False, "❌ Email já cadastrado!"
        elif 'cpf' in str(e):
            return False, "❌ CPF já cadastrado!"
        else:
            return False, f"❌ Erro de integridade: {e}"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def listar_usuarios(filtro=None):
    """Lista usuários com opção de filtro"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        if filtro:
            cursor.execute(f"SELECT * FROM usuarios WHERE {filtro} ORDER BY id DESC")
        else:
            cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
        
        usuarios = cursor.fetchall()
        conexao.close()
        return usuarios
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []

def buscar_usuarios_avancado(termo):
    """Busca avançada em múltiplos campos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT * FROM usuarios 
            WHERE nome LIKE ? OR email LIKE ? OR telefone LIKE ? 
            OR celular LIKE ? OR cpf LIKE ? OR cidade LIKE ?
            ORDER BY nome
        ''', (f'%{termo}%', f'%{termo}%', f'%{termo}%', 
              f'%{termo}%', f'%{termo}%', f'%{termo}%'))
        
        usuarios = cursor.fetchall()
        conexao.close()
        return usuarios
    except Exception as e:
        print(f"Erro na busca avançada: {e}")
        return []

def atualizar_usuario(id, nome, email, telefone, celular, endereco, cidade, estado,
                     cep, cpf, rg, data_nascimento, profissao, interesses, status, observacoes):
    """Atualiza todos os dados de um usuário"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET nome = ?, email = ?, telefone = ?, celular = ?, endereco = ?, 
                cidade = ?, estado = ?, cep = ?, cpf = ?, rg = ?,
                data_nascimento = ?, profissao = ?, interesses = ?, 
                status = ?, observacoes = ?
            WHERE id = ?
        ''', (nome, email, telefone, celular, endereco, cidade, estado,
              cep, cpf, rg, data_nascimento, profissao, interesses,
              status, observacoes, id))
        
        cursor.execute('''
            INSERT INTO historico (usuario_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (id, 'atualizacao_usuario', f'Usuário "{nome}" atualizado'))
        
        conexao.commit()
        conexao.close()
        return True, "✅ Usuário atualizado com sucesso!"
    except sqlite3.IntegrityError as e:
        if 'email' in str(e):
            return False, "❌ Email já cadastrado para outro usuário!"
        elif 'cpf' in str(e):
            return False, "❌ CPF já cadastrado para outro usuário!"
        else:
            return False, f"❌ Erro de integridade: {e}"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def deletar_usuario(id):
    """Remove um usuário com verificação de empréstimos"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE usuario_id = ? AND status = "ativo"', (id,))
        if cursor.fetchone()[0] > 0:
            return False, "❌ Não é possível deletar usuário com empréstimos ativos!"
        
        cursor.execute('SELECT COUNT(*) FROM reservas WHERE usuario_id = ? AND status = "ativa"', (id,))
        if cursor.fetchone()[0] > 0:
            return False, "❌ Não é possível deletar usuário com reservas ativas!"
        
        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (id,))
        nome = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        
        cursor.execute('''
            INSERT INTO historico (usuario_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (id, 'exclusao_usuario', f'Usuário "{nome}" removido'))
        
        conexao.commit()
        conexao.close()
        return True, "✅ Usuário removido com sucesso!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

# ========== FUNÇÕES PARA EMPRÉSTIMOS ==========

def realizar_emprestimo(livro_id, usuario_id, dias_emprestimo=None):
    """Realiza um empréstimo com todas as verificações"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        if not dias_emprestimo:
            cursor.execute('SELECT valor FROM config WHERE chave = "dias_emprestimo_padrao"')
            dias_emprestimo = int(cursor.fetchone()[0])
        
        cursor.execute('SELECT disponiveis, titulo FROM livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()
        
        if not livro:
            return False, "❌ Livro não encontrado!"
        
        if livro[0] <= 0:
            return False, "❌ Livro indisponível para empréstimo!"
        
        cursor.execute('SELECT status, nome FROM usuarios WHERE id = ?', (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            return False, "❌ Usuário não encontrado!"
        
        if usuario[0] != 'ativo':
            return False, "❌ Usuário inativo!"
        
        cursor.execute('SELECT valor FROM config WHERE chave = "max_emprestimos"')
        max_emprestimos = int(cursor.fetchone()[0])
        
        cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE usuario_id = ? AND status = "ativo"', (usuario_id,))
        emprestimos_ativos = cursor.fetchone()[0]
        
        if emprestimos_ativos >= max_emprestimos:
            return False, f"❌ Usuário atingiu o limite máximo de {max_emprestimos} empréstimos!"
        
        cursor.execute('''
            SELECT COUNT(*) FROM emprestimos 
            WHERE livro_id = ? AND usuario_id = ? AND status = "ativo"
        ''', (livro_id, usuario_id))
        
        if cursor.fetchone()[0] > 0:
            return False, "❌ Usuário já tem este livro emprestado!"
        
        cursor.execute('SELECT multas_pendentes FROM usuarios WHERE id = ?', (usuario_id,))
        multas = cursor.fetchone()[0]
        
        if multas > 0:
            return False, f"❌ Usuário possui multa pendente de R$ {multas:.2f}!"
        
        data_emprestimo = datetime.now().date()
        data_devolucao_prevista = data_emprestimo + timedelta(days=dias_emprestimo)
        
        cursor.execute('''
            INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, data_devolucao_prevista)
            VALUES (?, ?, ?, ?)
        ''', (livro_id, usuario_id, data_emprestimo, data_devolucao_prevista))
        
        emprestimo_id = cursor.lastrowid
        
        cursor.execute('''
            UPDATE livros 
            SET disponiveis = disponiveis - 1, 
                emprestimos_total = emprestimos_total + 1,
                ultimo_emprestimo = ?
            WHERE id = ?
        ''', (data_emprestimo, livro_id))
        
        cursor.execute('''
            UPDATE usuarios 
            SET emprestimos_total = emprestimos_total + 1,
                ultimo_emprestimo = ?
            WHERE id = ?
        ''', (data_emprestimo, usuario_id))
        
        cursor.execute('''
            INSERT INTO historico (emprestimo_id, usuario_id, livro_id, acao, detalhes)
            VALUES (?, ?, ?, ?, ?)
        ''', (emprestimo_id, usuario_id, livro_id, 'emprestimo',
              f'Empréstimo realizado. Devolução prevista: {data_devolucao_prevista}'))
        
        conexao.commit()
        conexao.close()
        return True, f"✅ Empréstimo realizado! Devolução prevista: {data_devolucao_prevista.strftime('%d/%m/%Y')}"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def listar_emprestimos(filtro=None):
    """Lista empréstimos com detalhes"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        query = '''
            SELECT 
                e.id,
                l.titulo,
                u.nome,
                e.data_emprestimo,
                e.data_devolucao_prevista,
                e.data_devolucao_real,
                e.status,
                CASE 
                    WHEN e.status = 'ativo' AND date('now') > e.data_devolucao_prevista 
                    THEN 'ATRASADO' 
                    ELSE e.status 
                END as status_real,
                e.multa,
                e.renovacoes,
                e.observacao
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
        '''
        
        if filtro:
            query += f" WHERE {filtro}"
        
        query += " ORDER BY e.id DESC"
        
        cursor.execute(query)
        emprestimos = cursor.fetchall()
        conexao.close()
        return emprestimos
    except Exception as e:
        print(f"Erro ao listar empréstimos: {e}")
        return []

def devolver_livro(emprestimo_id):
    """Registra a devolução de um livro com cálculo de multa"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT livro_id, usuario_id, data_devolucao_prevista, status 
            FROM emprestimos 
            WHERE id = ? AND status = "ativo"
        ''', (emprestimo_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "❌ Empréstimo não encontrado ou já finalizado!"
        
        livro_id = resultado[0]
        usuario_id = resultado[1]
        data_prevista = datetime.strptime(resultado[2], '%Y-%m-%d').date()
        
        cursor.execute('SELECT valor FROM config WHERE chave = "multa_dia"')
        valor_multa = float(cursor.fetchone()[0])
        
        data_hoje = datetime.now().date()
        multa = 0
        dias_atraso = 0
        
        if data_hoje > data_prevista:
            dias_atraso = (data_hoje - data_prevista).days
            multa = dias_atraso * valor_multa
        
        cursor.execute('''
            UPDATE emprestimos 
            SET data_devolucao_real = ?, status = 'finalizado', multa = ?
            WHERE id = ?
        ''', (data_hoje, multa, emprestimo_id))
        
        cursor.execute('UPDATE livros SET disponiveis = disponiveis + 1 WHERE id = ?', (livro_id,))
        
        if multa > 0:
            cursor.execute('''
                UPDATE usuarios 
                SET multas_pendentes = multas_pendentes + ?
                WHERE id = ?
            ''', (multa, usuario_id))
        
        mensagem_multa = f"Multa de R$ {multa:.2f}" if multa > 0 else "Sem multa"
        cursor.execute('''
            INSERT INTO historico (emprestimo_id, usuario_id, livro_id, acao, detalhes)
            VALUES (?, ?, ?, ?, ?)
        ''', (emprestimo_id, usuario_id, livro_id, 'devolucao',
              f'Devolução realizada. {mensagem_multa}. Dias de atraso: {dias_atraso}'))
        
        conexao.commit()
        conexao.close()
        
        if multa > 0:
            return True, f"✅ Devolução realizada! Multa de R$ {multa:.2f} por {dias_atraso} dias de atraso."
        else:
            return True, "✅ Devolução realizada com sucesso!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def renovar_emprestimo(emprestimo_id, dias_extras=None):
    """Renova um empréstimo"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT livro_id, usuario_id, data_devolucao_prevista, status, renovacoes
            FROM emprestimos 
            WHERE id = ? AND status = "ativo"
        ''', (emprestimo_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "❌ Empréstimo não encontrado ou já finalizado!"
        
        if not dias_extras:
            dias_extras = 7
        
        data_atual = datetime.strptime(resultado[2], '%Y-%m-%d').date()
        nova_data = data_atual + timedelta(days=dias_extras)
        
        cursor.execute('''
            UPDATE emprestimos 
            SET data_devolucao_prevista = ?, renovacoes = renovacoes + 1
            WHERE id = ?
        ''', (nova_data, emprestimo_id))
        
        cursor.execute('''
            INSERT INTO historico (emprestimo_id, acao, detalhes)
            VALUES (?, ?, ?)
        ''', (emprestimo_id, 'renovacao', f'Renovado por mais {dias_extras} dias. Nova devolução: {nova_data}'))
        
        conexao.commit()
        conexao.close()
        return True, f"✅ Empréstimo renovado! Nova data: {nova_data.strftime('%d/%m/%Y')}"
    except Exception as e:
        return False, f"❌ Erro: {e}"

# ========== FUNÇÕES PARA RESERVAS ==========

def realizar_reserva(livro_id, usuario_id):
    """Realiza uma reserva de livro"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT disponiveis FROM livros WHERE id = ?', (livro_id,))
        disponiveis = cursor.fetchone()
        
        if not disponiveis:
            return False, "❌ Livro não encontrado!"
        
        if disponiveis[0] > 0:
            return False, "❌ Livro está disponível, faça um empréstimo!"
        
        cursor.execute('''
            SELECT COUNT(*) FROM reservas 
            WHERE livro_id = ? AND usuario_id = ? AND status = "ativa"
        ''', (livro_id, usuario_id))
        
        if cursor.fetchone()[0] > 0:
            return False, "❌ Você já tem uma reserva para este livro!"
        
        cursor.execute('SELECT valor FROM config WHERE chave = "dias_reserva"')
        dias_reserva = int(cursor.fetchone()[0])
        
        data_limite = datetime.now().date() + timedelta(days=dias_reserva)
        
        cursor.execute('''
            INSERT INTO reservas (livro_id, usuario_id, data_limite)
            VALUES (?, ?, ?)
        ''', (livro_id, usuario_id, data_limite))
        
        conexao.commit()
        conexao.close()
        return True, f"✅ Reserva realizada! Retirar até: {data_limite.strftime('%d/%m/%Y')}"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def listar_reservas():
    """Lista reservas ativas"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT 
                r.id,
                l.titulo,
                u.nome,
                r.data_reserva,
                r.data_limite,
                r.status,
                CASE 
                    WHEN r.status = 'ativa' AND date('now') > r.data_limite 
                    THEN 'EXPIRADA' 
                    ELSE r.status 
                END as status_real
            FROM reservas r
            JOIN livros l ON r.livro_id = l.id
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.status = 'ativa'
            ORDER BY r.data_reserva
        ''')
        
        reservas = cursor.fetchall()
        conexao.close()
        return reservas
    except Exception as e:
        print(f"Erro ao listar reservas: {e}")
        return []

# ========== FUNÇÕES PARA RELATÓRIOS ==========

def relatorio_completo():
    """Gera relatório completo do sistema"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        relatorio = {}
        
        cursor.execute('SELECT COUNT(*) FROM livros')
        relatorio['total_livros'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(quantidade) FROM livros')
        relatorio['total_exemplares'] = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(disponiveis) FROM livros')
        relatorio['total_disponiveis'] = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE status = "ativo"')
        relatorio['usuarios_ativos'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE status = "inativo"')
        relatorio['usuarios_inativos'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE status = "ativo"')
        relatorio['emprestimos_ativos'] = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM emprestimos 
            WHERE status = "ativo" AND date('now') > data_devolucao_prevista
        ''')
        relatorio['emprestimos_atrasados'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM reservas WHERE status = "ativa"')
        relatorio['reservas_ativas'] = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT l.titulo, l.emprestimos_total
            FROM livros l
            ORDER BY l.emprestimos_total DESC
            LIMIT 10
        ''')
        relatorio['livros_populares'] = cursor.fetchall()
        
        cursor.execute('''
            SELECT u.nome, u.emprestimos_total
            FROM usuarios u
            ORDER BY u.emprestimos_total DESC
            LIMIT 10
        ''')
        relatorio['usuarios_ativos_top'] = cursor.fetchall()
        
        cursor.execute('SELECT SUM(multas_pendentes) FROM usuarios')
        relatorio['total_multas'] = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT strftime('%Y-%m', data_emprestimo) as mes,
                   COUNT(*) as total
            FROM emprestimos
            WHERE data_emprestimo >= date('now', '-6 months')
            GROUP BY mes
            ORDER BY mes
        ''')
        relatorio['emprestimos_mensais'] = cursor.fetchall()
        
        cursor.execute('''
            SELECT genero, COUNT(*) as total
            FROM livros
            WHERE genero IS NOT NULL AND genero != ''
            GROUP BY genero
            ORDER BY total DESC
        ''')
        relatorio['livros_por_genero'] = cursor.fetchall()
        
        conexao.close()
        return relatorio
    except Exception as e:
        print(f"Erro no relatório: {e}")
        return {}

def gerar_relatorio_atrasados():
    """Gera relatório de empréstimos atrasados"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT 
                e.id,
                l.titulo,
                u.nome,
                u.email,
                u.telefone,
                e.data_emprestimo,
                e.data_devolucao_prevista,
                julianday('now') - julianday(e.data_devolucao_prevista) as dias_atraso,
                e.multa
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.status = 'ativo' AND date('now') > e.data_devolucao_prevista
            ORDER BY dias_atraso DESC
        ''')
        
        atrasados = cursor.fetchall()
        conexao.close()
        return atrasados
    except Exception as e:
        print(f"Erro no relatório de atrasados: {e}")
        return []

def main():
    criar_banco()
    atualizar_banco()
    root = tk.Tk()
    app = Pergamium(root)
    root.mainloop()

if __name__ == "__main__":
    main()