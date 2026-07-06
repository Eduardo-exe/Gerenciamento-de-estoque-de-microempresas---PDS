import flet as ft
import threading
from api.client import api
from state import get_state, clear_state

BG     = "#1C1C1E"
SB     = "#1E1E22"
CARD   = "#252529"
INPUT  = "#2C2C2E"
ACCENT = "#4DB6AC"
TEXT   = "#F2F2F7"
MUTED  = "#8E8E93"
SUCC   = "#30D158"
BORDER = "#3A3A3E"
ERR    = "#FF453A"
WARN   = "#F59E0B"

# Cor diferenciada do gerente para destaque no badge
GERENTE_COLOR  = "#E8A838"
GERENTE_BG     = "#4A3200"


def _field(hint: str, kb=None, password=False) -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=MUTED),
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        bgcolor=INPUT,
        border_radius=8,
        keyboard_type=kb,
        password=password,
        expand=True,
        text_size=14,
        content_padding=ft.Padding(left=12, right=12, top=10, bottom=10),
        border_width=1,
    )


def _card_container(content: ft.Control) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=10,
        padding=20,
        border=ft.Border(
            left=ft.BorderSide(1, BORDER),
            right=ft.BorderSide(1, BORDER),
            top=ft.BorderSide(1, BORDER),
            bottom=ft.BorderSide(1, BORDER),
        ),
    )


def gerente_view(page: ft.Page) -> ft.View:
    nome_usuario = get_state("nome") or "Gerente"
    iniciais = "".join(p[0].upper() for p in nome_usuario.split()[:2]) or "GE"

    # ── Estado interno ────────────────────────────────────────────────────────
    mode = {"value": "entrada"}

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Movimentação de Estoque (herdada do estoquista)
    # ══════════════════════════════════════════════════════════════════════════
    f_codigo     = _field("Ex: 00412", kb=ft.KeyboardType.NUMBER)
    f_nome_mov   = _field("Buscar por nome")
    f_quantidade = _field("0", kb=ft.KeyboardType.NUMBER)
    f_obs        = _field("Ex: Nota fiscal nº 2031")
    f_unidade = ft.Dropdown(
        hint_text="Unidade",
        hint_style=ft.TextStyle(color=MUTED),
        options=[
            ft.dropdown.Option("un", "Unidade"),
            ft.dropdown.Option("kg", "Kg"),
            ft.dropdown.Option("l",  "Litro"),
            ft.dropdown.Option("m",  "Metro"),
            ft.dropdown.Option("cx", "Caixa"),
        ],
        border_color=BORDER,
        focused_border_color=ACCENT,
        text_style=ft.TextStyle(color=TEXT),
        bgcolor=INPUT,
        border_radius=8,
        expand=True,
    )

    feedback_mov  = ft.Text("", size=13, visible=False)
    btn_label_mov = ft.Text("Registrar entrada", color=TEXT, size=14)
    btn_registrar = ft.Button(
        content=btn_label_mov,
        style=ft.ButtonStyle(
            bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"},
            color=TEXT,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
        ),
    )

    # ── Tabs Entrada / Saída ────────────────────────────────────────────────
    tab_entrada_txt = ft.Text("Entrada", size=14, color=TEXT, weight=ft.FontWeight.W_500)
    tab_saida_txt   = ft.Text("Saída",   size=14, color=MUTED)
    ind_entrada     = ft.Container(height=2, bgcolor=ACCENT)
    ind_saida       = ft.Container(height=2, bgcolor="transparent")

    def switch_mode(m: str):
        mode["value"] = m
        if m == "entrada":
            tab_entrada_txt.color = TEXT
            tab_saida_txt.color   = MUTED
            ind_entrada.bgcolor   = ACCENT
            ind_saida.bgcolor     = "transparent"
            btn_label_mov.value   = "Registrar entrada"
        else:
            tab_entrada_txt.color = MUTED
            tab_saida_txt.color   = TEXT
            ind_entrada.bgcolor   = "transparent"
            ind_saida.bgcolor     = ACCENT
            btn_label_mov.value   = "Registrar saída"
        page.update()

    def _auto_hide(feedback_ctrl: ft.Text):
        def hide():
            feedback_ctrl.visible = False
            try:
                page.update()
            except Exception:
                pass
        threading.Timer(3.0, hide).start()

    def set_feedback_mov(msg: str, ok: bool = True):
        feedback_mov.value   = ("✓  " if ok else "✗  ") + msg
        feedback_mov.color   = SUCC if ok else ERR
        feedback_mov.visible = True
        page.update()
        _auto_hide(feedback_mov)

    def limpar_mov_campos():
        for f in [f_codigo, f_nome_mov, f_quantidade, f_obs]:
            f.value = ""
        f_unidade.value = None
        page.update()

    def limpar_mov(e=None):
        limpar_mov_campos()
        feedback_mov.visible = False
        page.update()

    def registrar(e):
        feedback_mov.visible = False
        page.update()
        try:
            codigo    = int(f_codigo.value or "0")
            nome_prod = (f_nome_mov.value or "").strip()
            qtd       = int(f_quantidade.value or "0")
        except ValueError:
            set_feedback_mov("Código e quantidade devem ser números.", ok=False)
            return

        if not codigo or not nome_prod or not qtd:
            set_feedback_mov("Preencha código, nome e quantidade.", ok=False)
            return

        if mode["value"] == "entrada":
            res = api.registrar_entrada_gerente(codigo, nome_prod, qtd)
        else:
            res = api.registrar_saida_gerente(codigo, nome_prod, qtd)

        if "erro" in res:
            set_feedback_mov(res["erro"], ok=False)
        else:
            limpar_mov_campos()
            set_feedback_mov(res.get("mensagem", "Operação realizada com sucesso!"))

    btn_registrar.on_click = registrar

    tabs_row = ft.Row([
        ft.Column([
            ft.Container(
                content=tab_entrada_txt,
                padding=ft.Padding(left=4, right=4, top=6, bottom=6),
                on_click=lambda e: switch_mode("entrada"),
                ink=True,
            ),
            ind_entrada,
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column([
            ft.Container(
                content=tab_saida_txt,
                padding=ft.Padding(left=4, right=4, top=6, bottom=6),
                on_click=lambda e: switch_mode("saida"),
                ink=True,
            ),
            ind_saida,
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], spacing=16)

    formulario = _card_container(
        ft.Column([
            ft.Text("Movimentação de estoque", size=18, color=TEXT, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            tabs_row,
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("Código do produto", color=MUTED, size=12), f_codigo],
                          expand=True, spacing=4),
                ft.Column([ft.Text("Nome do produto", color=MUTED, size=12), f_nome_mov],
                          expand=True, spacing=4),
            ], spacing=16),
            ft.Row([
                ft.Column([ft.Text("Quantidade", color=MUTED, size=12), f_quantidade],
                          expand=True, spacing=4),
                ft.Column([ft.Text("Unidade", color=MUTED, size=12), f_unidade],
                          expand=True, spacing=4),
            ], spacing=16),
            ft.Column([ft.Text("Observação (opcional)", color=MUTED, size=12), f_obs], spacing=4),
            ft.Container(height=4),
            feedback_mov,
            ft.Row([
                btn_registrar,
                ft.Button(
                    "Limpar",
                    on_click=limpar_mov,
                    style=ft.ButtonStyle(
                        color=MUTED,
                        side=ft.BorderSide(1, BORDER),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                    ),
                ),
            ], spacing=12),
        ], spacing=8)
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Consultar estoque (herdada do estoquista)
    # ══════════════════════════════════════════════════════════════════════════
    consultar_col = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    def carregar_consultar():
        consultar_col.controls.clear()
        consultar_col.controls.append(
            ft.Text("Estoque atual", size=18, color=TEXT, weight=ft.FontWeight.W_600)
        )
        consultar_col.controls.append(ft.Container(height=8))

        itens = api.get_estoque_gerente()
        if not itens:
            consultar_col.controls.append(
                ft.Text("Nenhum item no estoque ou erro ao conectar.", color=MUTED, size=14)
            )
        else:
            for item in itens:
                qtd    = item.get("quantidade", 0)
                status = "Normal" if qtd > 10 else "Baixo"
                s_c    = SUCC      if status == "Normal" else WARN
                s_bg   = "#14532D" if status == "Normal" else "#78350F"
                consultar_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(str(item.get("codigo", "")), color=TEXT,  size=13, width=70),
                            ft.Text(item.get("nome", ""),        color=TEXT,  size=13, expand=True),
                            ft.Text(f"Qtd: {qtd}",               color=MUTED, size=13),
                            ft.Container(
                                content=ft.Text(status, size=11, color=s_c, weight=ft.FontWeight.W_600),
                                bgcolor=s_bg,
                                border_radius=6,
                                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            ),
                        ], spacing=12),
                        bgcolor=CARD,
                        border_radius=8,
                        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
                        border=ft.Border(
                            left=ft.BorderSide(1, BORDER),
                            right=ft.BorderSide(1, BORDER),
                            top=ft.BorderSide(1, BORDER),
                            bottom=ft.BorderSide(1, BORDER),
                        ),
                    )
                )
        page.update()

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Produtos (CRUD)
    # ══════════════════════════════════════════════════════════════════════════
    feedback_prod = ft.Text("", size=13, visible=False)

    fp_codigo    = _field("Ex: 1001", kb=ft.KeyboardType.NUMBER)
    fp_nome      = _field("Ex: Caneta Azul")
    fp_quantidade = _field("0", kb=ft.KeyboardType.NUMBER)

    produtos_lista = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def set_feedback_prod(msg: str, ok: bool = True):
        feedback_prod.value   = ("✓  " if ok else "✗  ") + msg
        feedback_prod.color   = SUCC if ok else ERR
        feedback_prod.visible = True
        page.update()
        _auto_hide(feedback_prod)

    def limpar_form_prod(e=None):
        fp_codigo.value = ""
        fp_nome.value   = ""
        fp_quantidade.value = ""
        page.update()

    def carregar_produtos():
        produtos_lista.controls.clear()
        itens = api.get_produtos_gerente()
        if not itens:
            produtos_lista.controls.append(
                ft.Text("Nenhum produto cadastrado.", color=MUTED, size=14)
            )
        else:
            for p in itens:
                cod  = p.get("codigo", "")
                nome = p.get("nome", "")
                qtd  = p.get("quantidade", 0)

                def _fill(e, c=cod, n=nome, q=qtd):
                    fp_codigo.value    = str(c)
                    fp_nome.value      = n
                    fp_quantidade.value = str(q)
                    page.update()

                def _del(e, c=cod):
                    res = api.deletar_produto(c)
                    if "erro" in res:
                        set_feedback_prod(res["erro"], ok=False)
                    else:
                        set_feedback_prod("Produto removido.")
                        carregar_produtos()
                        page.update()

                produtos_lista.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(str(cod),  color=TEXT,  size=13, width=65),
                            ft.Text(nome,       color=TEXT,  size=13, expand=True),
                            ft.Text(f"Qtd: {qtd}", color=MUTED, size=13, width=80),
                            ft.IconButton(
                                ft.Icons.EDIT_OUTLINED,
                                icon_color=ACCENT,
                                icon_size=18,
                                tooltip="Editar",
                                on_click=_fill,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=ERR,
                                icon_size=18,
                                tooltip="Remover",
                                on_click=_del,
                            ),
                        ], spacing=4),
                        bgcolor=CARD,
                        border_radius=8,
                        padding=ft.Padding(left=12, right=8, top=10, bottom=10),
                        border=ft.Border(
                            left=ft.BorderSide(1, BORDER),
                            right=ft.BorderSide(1, BORDER),
                            top=ft.BorderSide(1, BORDER),
                            bottom=ft.BorderSide(1, BORDER),
                        ),
                    )
                )
        page.update()

    def cadastrar_produto(e):
        try:
            cod = int(fp_codigo.value or "0")
            qtd = int(fp_quantidade.value or "0")
        except ValueError:
            set_feedback_prod("Código e quantidade devem ser números.", ok=False)
            return
        nome = (fp_nome.value or "").strip()
        if not cod or not nome:
            set_feedback_prod("Preencha código e nome.", ok=False)
            return
        res = api.cadastrar_produto_gerente(cod, nome, qtd)
        if "erro" in res:
            set_feedback_prod(res["erro"], ok=False)
        else:
            set_feedback_prod("Produto cadastrado!")
            limpar_form_prod()
            carregar_produtos()

    def atualizar_produto(e):
        try:
            cod = int(fp_codigo.value or "0")
            qtd = int(fp_quantidade.value or "0")
        except ValueError:
            set_feedback_prod("Código e quantidade devem ser números.", ok=False)
            return
        nome = (fp_nome.value or "").strip()
        if not cod or not nome:
            set_feedback_prod("Preencha código e nome para atualizar.", ok=False)
            return
        res = api.atualizar_produto(cod, nome, qtd)
        if "erro" in res:
            set_feedback_prod(res["erro"], ok=False)
        else:
            set_feedback_prod("Produto atualizado!")
            limpar_form_prod()
            carregar_produtos()

    produtos_sec_content = ft.Column([
        ft.Text("Produtos", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card_container(ft.Column([
            ft.Text("Cadastrar / Editar produto", size=14, color=MUTED, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("Código", color=MUTED, size=12), fp_codigo],  expand=1, spacing=4),
                ft.Column([ft.Text("Nome",   color=MUTED, size=12), fp_nome],    expand=2, spacing=4),
                ft.Column([ft.Text("Qtd",    color=MUTED, size=12), fp_quantidade], expand=1, spacing=4),
            ], spacing=12),
            ft.Container(height=4),
            feedback_prod,
            ft.Row([
                ft.Button(
                    content=ft.Text("Cadastrar", color=TEXT, size=13),
                    on_click=cadastrar_produto,
                    style=ft.ButtonStyle(
                        bgcolor={"": ACCENT, "hovered": "#3DA89E"},
                        color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=18, right=18, top=10, bottom=10),
                    ),
                ),
                ft.Button(
                    content=ft.Text("Atualizar", color=TEXT, size=13),
                    on_click=atualizar_produto,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"},
                        color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, BORDER),
                        padding=ft.Padding(left=18, right=18, top=10, bottom=10),
                    ),
                ),
                ft.Button(
                    "Limpar",
                    on_click=limpar_form_prod,
                    style=ft.ButtonStyle(
                        color=MUTED,
                        side=ft.BorderSide(1, BORDER),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=16, right=16, top=10, bottom=10),
                    ),
                ),
            ], spacing=8),
        ], spacing=8)),
        ft.Container(height=12),
        ft.Text("Produtos cadastrados", size=14, color=MUTED),
        ft.Container(height=4),
        produtos_lista,
    ], spacing=4, scroll=ft.ScrollMode.AUTO)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Fornecedores (CRUD)
    # ══════════════════════════════════════════════════════════════════════════
    feedback_forn = ft.Text("", size=13, visible=False)

    ff_cnpj      = _field("00.000.000/0001-00")
    ff_nome      = _field("Ex: Distribuidora XYZ")
    ff_telefone  = _field("(11) 90000-0000", kb=ft.KeyboardType.PHONE)

    fornecedores_lista = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def set_feedback_forn(msg: str, ok: bool = True):
        feedback_forn.value   = ("✓  " if ok else "✗  ") + msg
        feedback_forn.color   = SUCC if ok else ERR
        feedback_forn.visible = True
        page.update()
        _auto_hide(feedback_forn)

    def limpar_form_forn(e=None):
        ff_cnpj.value     = ""
        ff_nome.value     = ""
        ff_telefone.value = ""
        page.update()

    def carregar_fornecedores():
        fornecedores_lista.controls.clear()
        itens = api.get_fornecedores_gerente()
        if not itens:
            fornecedores_lista.controls.append(
                ft.Text("Nenhum fornecedor cadastrado.", color=MUTED, size=14)
            )
        else:
            for f in itens:
                cnpj = f.get("cnpj", "")
                nome = f.get("nome", "")
                tel  = f.get("telefone", "")

                def _fill_f(e, c=cnpj, n=nome, t=tel):
                    ff_cnpj.value     = c
                    ff_nome.value     = n
                    ff_telefone.value = t
                    page.update()

                def _del_f(e, c=cnpj):
                    res = api.deletar_fornecedor(c)
                    if "erro" in res:
                        set_feedback_forn(res["erro"], ok=False)
                    else:
                        set_feedback_forn("Fornecedor removido.")
                        carregar_fornecedores()
                        page.update()

                fornecedores_lista.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(cnpj, color=MUTED, size=12, width=140),
                            ft.Text(nome, color=TEXT,  size=13, expand=True),
                            ft.Text(tel,  color=MUTED, size=12, width=130),
                            ft.IconButton(
                                ft.Icons.EDIT_OUTLINED,
                                icon_color=ACCENT,
                                icon_size=18,
                                tooltip="Editar",
                                on_click=_fill_f,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=ERR,
                                icon_size=18,
                                tooltip="Remover",
                                on_click=_del_f,
                            ),
                        ], spacing=4),
                        bgcolor=CARD,
                        border_radius=8,
                        padding=ft.Padding(left=12, right=8, top=10, bottom=10),
                        border=ft.Border(
                            left=ft.BorderSide(1, BORDER),
                            right=ft.BorderSide(1, BORDER),
                            top=ft.BorderSide(1, BORDER),
                            bottom=ft.BorderSide(1, BORDER),
                        ),
                    )
                )
        page.update()

    def cadastrar_fornecedor(e):
        cnpj = (ff_cnpj.value or "").strip()
        nome = (ff_nome.value or "").strip()
        tel  = (ff_telefone.value or "").strip()
        if not cnpj or not nome:
            set_feedback_forn("Preencha CNPJ e nome.", ok=False)
            return
        res = api.cadastrar_fornecedor_gerente(cnpj, nome, tel)
        if "erro" in res:
            set_feedback_forn(res["erro"], ok=False)
        else:
            set_feedback_forn("Fornecedor cadastrado!")
            limpar_form_forn()
            carregar_fornecedores()

    def atualizar_fornecedor(e):
        cnpj = (ff_cnpj.value or "").strip()
        nome = (ff_nome.value or "").strip()
        tel  = (ff_telefone.value or "").strip()
        if not cnpj or not nome:
            set_feedback_forn("Preencha CNPJ e nome para atualizar.", ok=False)
            return
        res = api.atualizar_fornecedor(cnpj, nome, tel)
        if "erro" in res:
            set_feedback_forn(res["erro"], ok=False)
        else:
            set_feedback_forn("Fornecedor atualizado!")
            limpar_form_forn()
            carregar_fornecedores()

    fornecedores_sec_content = ft.Column([
        ft.Text("Fornecedores", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card_container(ft.Column([
            ft.Text("Cadastrar / Editar fornecedor", size=14, color=MUTED, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("CNPJ",     color=MUTED, size=12), ff_cnpj],     expand=2, spacing=4),
                ft.Column([ft.Text("Nome",     color=MUTED, size=12), ff_nome],     expand=3, spacing=4),
                ft.Column([ft.Text("Telefone", color=MUTED, size=12), ff_telefone], expand=2, spacing=4),
            ], spacing=12),
            ft.Container(height=4),
            feedback_forn,
            ft.Row([
                ft.Button(
                    content=ft.Text("Cadastrar", color=TEXT, size=13),
                    on_click=cadastrar_fornecedor,
                    style=ft.ButtonStyle(
                        bgcolor={"": ACCENT, "hovered": "#3DA89E"},
                        color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=18, right=18, top=10, bottom=10),
                    ),
                ),
                ft.Button(
                    content=ft.Text("Atualizar", color=TEXT, size=13),
                    on_click=atualizar_fornecedor,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"},
                        color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, BORDER),
                        padding=ft.Padding(left=18, right=18, top=10, bottom=10),
                    ),
                ),
                ft.Button(
                    "Limpar",
                    on_click=limpar_form_forn,
                    style=ft.ButtonStyle(
                        color=MUTED,
                        side=ft.BorderSide(1, BORDER),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=16, right=16, top=10, bottom=10),
                    ),
                ),
            ], spacing=8),
        ], spacing=8)),
        ft.Container(height=12),
        ft.Text("Fornecedores cadastrados", size=14, color=MUTED),
        ft.Container(height=4),
        fornecedores_lista,
    ], spacing=4, scroll=ft.ScrollMode.AUTO)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Relatório PDF
    # ══════════════════════════════════════════════════════════════════════════
    relatorio_status = ft.Text("", size=14, visible=False)
    progresso_rel    = ft.ProgressRing(width=24, height=24, stroke_width=3,
                                       color=ACCENT, visible=False)

    def gerar_relatorio(e):
        relatorio_status.visible  = False
        progresso_rel.visible     = True
        page.update()

        caminho = api.baixar_relatorio_pdf()

        progresso_rel.visible = False
        if caminho and not caminho.startswith("erro"):
            relatorio_status.value   = f"✓  PDF salvo em:\n{caminho}"
            relatorio_status.color   = SUCC
        else:
            relatorio_status.value   = f"✗  {caminho or 'Falha ao gerar relatório.'}"
            relatorio_status.color   = ERR
        relatorio_status.visible = True
        page.update()

    relatorio_sec_content = ft.Column([
        ft.Text("Relatório", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card_container(ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PICTURE_AS_PDF_OUTLINED, color=ERR, size=36),
                ft.Column([
                    ft.Text("Exportar relatório de estoque", color=TEXT, size=15,
                            weight=ft.FontWeight.W_500),
                    ft.Text("Gera um PDF com todos os itens e movimentações.",
                            color=MUTED, size=12),
                ], spacing=2, expand=True),
            ], spacing=16),
            ft.Container(height=12),
            ft.Row([
                ft.Button(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DOWNLOAD_OUTLINED, color=TEXT, size=16),
                        ft.Text("Baixar PDF", color=TEXT, size=14),
                    ], spacing=8, tight=True),
                    on_click=gerar_relatorio,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#C0392B", "hovered": "#E74C3C"},
                        color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                    ),
                ),
                progresso_rel,
            ], spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=4),
            relatorio_status,
        ], spacing=8)),
    ], spacing=4)

    # ══════════════════════════════════════════════════════════════════════════
    # Contêineres de seção (visibilidade controlada pela nav)
    # ══════════════════════════════════════════════════════════════════════════
    movimentacao_sec   = ft.Container(content=formulario,             expand=True, visible=True)
    consultar_sec      = ft.Container(content=consultar_col,          expand=True, visible=False)
    produtos_sec       = ft.Container(content=produtos_sec_content,   expand=True, visible=False)
    fornecedores_sec   = ft.Container(content=fornecedores_sec_content, expand=True, visible=False)
    relatorio_sec      = ft.Container(content=relatorio_sec_content,  expand=True, visible=False)

    # ══════════════════════════════════════════════════════════════════════════
    # Navegação lateral
    # ══════════════════════════════════════════════════════════════════════════
    nav_refs = {}
    nav_txts = {}

    def make_nav(key: str, label: str, active: bool = False) -> ft.Container:
        txt = ft.Text(
            label,
            color=TEXT if active else MUTED,
            size=14,
            weight=ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL,
        )
        nav_txts[key] = txt
        c = ft.Container(
            content=txt,
            padding=ft.Padding(left=20, right=20, top=11, bottom=11),
            bgcolor="#2A2A30" if active else None,
            border_radius=6,
            ink=True,
        )
        nav_refs[key] = c
        return c

    # Seções visíveis por chave de nav
    _sections = {
        "entrada":      movimentacao_sec,
        "saida":        movimentacao_sec,
        "consultar":    consultar_sec,
        "produtos":     produtos_sec,
        "fornecedores": fornecedores_sec,
        "relatorio":    relatorio_sec,
    }
    _all_unique = [movimentacao_sec, consultar_sec, produtos_sec, fornecedores_sec, relatorio_sec]

    def switch_nav(key: str):
        for k in nav_refs:
            active = k == key
            nav_txts[k].color  = TEXT if active else MUTED
            nav_txts[k].weight = ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL
            nav_refs[k].bgcolor = "#2A2A30" if active else None

        for sec in _all_unique:
            sec.visible = False
        _sections[key].visible = True

        if key in ("entrada", "saida"):
            switch_mode(key)
        elif key == "consultar":
            carregar_consultar()
        elif key == "produtos":
            carregar_produtos()
        elif key == "fornecedores":
            carregar_fornecedores()

        page.update()

    # Itens de nav — separadores visuais por grupo
    nav_entrada     = make_nav("entrada",      "Entrada",      active=True)
    nav_saida       = make_nav("saida",        "Saída")
    nav_consultar   = make_nav("consultar",    "Consultar")
    nav_produtos    = make_nav("produtos",     "Produtos")
    nav_fornecedores= make_nav("fornecedores", "Fornecedores")
    nav_relatorio   = make_nav("relatorio",    "Relatório")

    nav_entrada.on_click      = lambda e: switch_nav("entrada")
    nav_saida.on_click        = lambda e: switch_nav("saida")
    nav_consultar.on_click    = lambda e: switch_nav("consultar")
    nav_produtos.on_click     = lambda e: switch_nav("produtos")
    nav_fornecedores.on_click = lambda e: switch_nav("fornecedores")
    nav_relatorio.on_click    = lambda e: switch_nav("relatorio")

    def logout(e):
        api.clear()
        clear_state()
        page.go("/login")

    def _nav_group_label(label: str) -> ft.Container:
        return ft.Container(
            content=ft.Text(label, size=10, color="#555560", weight=ft.FontWeight.W_600),
            padding=ft.Padding(left=20, right=20, top=10, bottom=2),
        )

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("G-Estoque", size=15, color=TEXT, weight=ft.FontWeight.BOLD),
                padding=ft.Padding(left=20, right=0, top=20, bottom=16),
            ),
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(height=8),
            ft.Container(
                content=ft.Column([
                    _nav_group_label("ESTOQUE"),
                    nav_entrada,
                    nav_saida,
                    nav_consultar,
                    ft.Container(height=4),
                    _nav_group_label("GESTÃO"),
                    nav_produtos,
                    nav_fornecedores,
                    nav_relatorio,
                ], spacing=2),
                padding=ft.Padding(left=8, right=8, top=0, bottom=0),
            ),
            ft.Container(expand=True),
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(
                content=ft.TextButton(
                    "Sair",
                    icon=ft.Icons.LOGOUT,
                    on_click=logout,
                    style=ft.ButtonStyle(color=MUTED),
                ),
                padding=ft.Padding(left=8, right=8, top=8, bottom=8),
            ),
        ], spacing=0, expand=True),
        width=200,
        bgcolor=SB,
        border=ft.Border(right=ft.BorderSide(1, BORDER)),
    )

    top_bar = ft.Container(
        content=ft.Row([
            ft.Text("Gerente — gestão de estoque", color=MUTED, size=12),
            ft.Row([
                ft.Container(
                    content=ft.Text("Gerente", size=11, color=GERENTE_COLOR, weight=ft.FontWeight.W_600),
                    bgcolor=GERENTE_BG,
                    border_radius=6,
                    padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                ),
                ft.Container(
                    content=ft.Text(iniciais, size=12, color=TEXT, weight=ft.FontWeight.BOLD),
                    bgcolor="#1A5276",
                    border_radius=20,
                    width=32, height=32,
                    alignment=ft.Alignment(0, 0),
                ),
            ], spacing=8),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding(left=20, right=20, top=10, bottom=10),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
    )

    main_area = ft.Container(
        content=ft.Column([
            top_bar,
            ft.Container(
                content=ft.Column([
                    movimentacao_sec,
                    consultar_sec,
                    produtos_sec,
                    fornecedores_sec,
                    relatorio_sec,
                ], expand=True),
                expand=True,
                padding=20,
            ),
        ], spacing=0, expand=True),
        expand=True,
    )

    return ft.View(
        route="/gerente",
        controls=[ft.Row([sidebar, main_area], expand=True, spacing=0)],
        bgcolor=BG,
        padding=0,
    )
