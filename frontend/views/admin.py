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

ADMIN_COLOR = "#C084FC"   # roxo para o badge do admin
ADMIN_BG    = "#3B0764"

TIPO_LABEL = {
    "estoquista":    "Estoquista",
    "gerente":       "Gerente",
    "administrador": "Admin",
}
TIPO_COLOR = {
    "estoquista":    ("#30D158", "#14532D"),
    "gerente":       ("#E8A838", "#4A3200"),
    "administrador": ("#C084FC", "#3B0764"),
}


def _field(hint: str, kb=None, password: bool = False) -> ft.TextField:
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
        can_reveal_password=password,
        expand=True,
        text_size=14,
        content_padding=ft.Padding(left=12, right=12, top=10, bottom=10),
        border_width=1,
    )


def _card(content: ft.Control) -> ft.Container:
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


def _nav_group(label: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, size=10, color="#555560", weight=ft.FontWeight.W_600),
        padding=ft.Padding(left=20, right=20, top=10, bottom=2),
    )


def admin_view(page: ft.Page) -> ft.View:
    nome_usuario = get_state("nome") or "Admin"
    iniciais = "".join(p[0].upper() for p in nome_usuario.split()[:2]) or "AD"

    # ── estado interno ────────────────────────────────────────────────────────
    mode = {"value": "entrada"}

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Movimentação de Estoque (herdada)
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
        border_color=BORDER, focused_border_color=ACCENT,
        text_style=ft.TextStyle(color=TEXT),
        bgcolor=INPUT, border_radius=8, expand=True,
    )

    fb_mov   = ft.Text("", size=13, visible=False)
    btn_lbl  = ft.Text("Registrar entrada", color=TEXT, size=14)
    btn_reg  = ft.Button(
        content=btn_lbl,
        style=ft.ButtonStyle(
            bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"}, color=TEXT,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
        ),
    )

    tab_ent_txt = ft.Text("Entrada", size=14, color=TEXT, weight=ft.FontWeight.W_500)
    tab_sai_txt = ft.Text("Saída",   size=14, color=MUTED)
    ind_ent     = ft.Container(height=2, bgcolor=ACCENT)
    ind_sai     = ft.Container(height=2, bgcolor="transparent")

    def _auto_hide(ctrl: ft.Text):
        def _hide():
            ctrl.visible = False
            try: page.update()
            except Exception: pass
        threading.Timer(3.0, _hide).start()

    def _fb(ctrl: ft.Text, msg: str, ok: bool = True):
        ctrl.value   = ("✓  " if ok else "✗  ") + msg
        ctrl.color   = SUCC if ok else ERR
        ctrl.visible = True
        page.update()
        _auto_hide(ctrl)

    def switch_mode(m: str):
        mode["value"] = m
        if m == "entrada":
            tab_ent_txt.color = TEXT; tab_sai_txt.color = MUTED
            ind_ent.bgcolor = ACCENT; ind_sai.bgcolor = "transparent"
            btn_lbl.value = "Registrar entrada"
        else:
            tab_ent_txt.color = MUTED; tab_sai_txt.color = TEXT
            ind_ent.bgcolor = "transparent"; ind_sai.bgcolor = ACCENT
            btn_lbl.value = "Registrar saída"
        page.update()

    def limpar_mov(e=None):
        for f in [f_codigo, f_nome_mov, f_quantidade, f_obs]:
            f.value = ""
        f_unidade.value = None
        fb_mov.visible = False
        page.update()

    def registrar(e):
        fb_mov.visible = False; page.update()
        try:
            cod = int(f_codigo.value or "0")
            qtd = int(f_quantidade.value or "0")
        except ValueError:
            _fb(fb_mov, "Código e quantidade devem ser números.", ok=False); return
        nome = (f_nome_mov.value or "").strip()
        if not cod or not nome or not qtd:
            _fb(fb_mov, "Preencha código, nome e quantidade.", ok=False); return

        if mode["value"] == "entrada":
            res = api.registrar_entrada_gerente(cod, nome, qtd)
        else:
            res = api.registrar_saida_gerente(cod, nome, qtd)

        if "erro" in res:
            _fb(fb_mov, res["erro"], ok=False)
        else:
            for f in [f_codigo, f_nome_mov, f_quantidade, f_obs]:
                f.value = ""
            f_unidade.value = None
            _fb(fb_mov, res.get("mensagem", "Operação realizada com sucesso!"))

    btn_reg.on_click = registrar

    tabs_row = ft.Row([
        ft.Column([
            ft.Container(content=tab_ent_txt, padding=ft.Padding(4,0,4,6),
                         on_click=lambda e: switch_mode("entrada"), ink=True),
            ind_ent,
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column([
            ft.Container(content=tab_sai_txt, padding=ft.Padding(4,0,4,6),
                         on_click=lambda e: switch_mode("saida"), ink=True),
            ind_sai,
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], spacing=16)

    formulario = _card(ft.Column([
        ft.Text("Movimentação de estoque", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        tabs_row,
        ft.Divider(color=BORDER, thickness=0.5, height=1),
        ft.Container(height=8),
        ft.Row([
            ft.Column([ft.Text("Código", color=MUTED, size=12), f_codigo],   expand=True, spacing=4),
            ft.Column([ft.Text("Nome",   color=MUTED, size=12), f_nome_mov], expand=True, spacing=4),
        ], spacing=16),
        ft.Row([
            ft.Column([ft.Text("Quantidade", color=MUTED, size=12), f_quantidade], expand=True, spacing=4),
            ft.Column([ft.Text("Unidade",    color=MUTED, size=12), f_unidade],    expand=True, spacing=4),
        ], spacing=16),
        ft.Column([ft.Text("Observação (opcional)", color=MUTED, size=12), f_obs], spacing=4),
        ft.Container(height=4),
        fb_mov,
        ft.Row([
            btn_reg,
            ft.Button("Limpar", on_click=limpar_mov,
                      style=ft.ButtonStyle(color=MUTED, side=ft.BorderSide(1, BORDER),
                                           shape=ft.RoundedRectangleBorder(radius=8),
                                           padding=ft.Padding(left=20, right=20, top=12, bottom=12))),
        ], spacing=12),
    ], spacing=8))

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Consultar estoque (herdada)
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
                qtd = item.get("quantidade", 0)
                status = "Normal" if qtd > 10 else "Baixo"
                s_c  = SUCC if status == "Normal" else WARN
                s_bg = "#14532D" if status == "Normal" else "#78350F"
                consultar_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(str(item.get("codigo", "")), color=TEXT,  size=13, width=70),
                            ft.Text(item.get("nome", ""),        color=TEXT,  size=13, expand=True),
                            ft.Text(f"Qtd: {qtd}",               color=MUTED, size=13),
                            ft.Container(
                                content=ft.Text(status, size=11, color=s_c, weight=ft.FontWeight.W_600),
                                bgcolor=s_bg, border_radius=6,
                                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            ),
                        ], spacing=12),
                        bgcolor=CARD, border_radius=8,
                        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
                        border=ft.Border(
                            left=ft.BorderSide(1, BORDER), right=ft.BorderSide(1, BORDER),
                            top=ft.BorderSide(1, BORDER),  bottom=ft.BorderSide(1, BORDER),
                        ),
                    )
                )
        page.update()

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Produtos (herdada do gerente)
    # ══════════════════════════════════════════════════════════════════════════
    fb_prod  = ft.Text("", size=13, visible=False)
    fp_cod   = _field("Ex: 1001", kb=ft.KeyboardType.NUMBER)
    fp_nome  = _field("Ex: Caneta Azul")
    fp_qtd   = _field("0", kb=ft.KeyboardType.NUMBER)
    prod_lista = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def carregar_produtos():
        prod_lista.controls.clear()
        itens = api.get_produtos_gerente()
        if not itens:
            prod_lista.controls.append(ft.Text("Nenhum produto cadastrado.", color=MUTED, size=14))
        else:
            for p in itens:
                cod = p.get("codigo", ""); nome = p.get("nome", ""); qtd = p.get("quantidade", 0)

                def _fill(e, c=cod, n=nome, q=qtd):
                    fp_cod.value = str(c); fp_nome.value = n; fp_qtd.value = str(q); page.update()

                def _del(e, c=cod):
                    res = api.deletar_produto(c)
                    if "erro" in res: _fb(fb_prod, res["erro"], ok=False)
                    else: _fb(fb_prod, "Produto removido."); carregar_produtos(); page.update()

                prod_lista.controls.append(ft.Container(
                    content=ft.Row([
                        ft.Text(str(cod), color=TEXT,  size=13, width=65),
                        ft.Text(nome,     color=TEXT,  size=13, expand=True),
                        ft.Text(f"Qtd: {qtd}", color=MUTED, size=13, width=80),
                        ft.IconButton(ft.Icons.EDIT_OUTLINED,    icon_color=ACCENT, icon_size=18, tooltip="Editar",  on_click=_fill),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE,   icon_color=ERR,    icon_size=18, tooltip="Remover", on_click=_del),
                    ], spacing=4),
                    bgcolor=CARD, border_radius=8,
                    padding=ft.Padding(left=12, right=8, top=10, bottom=10),
                    border=ft.Border(left=ft.BorderSide(1,BORDER), right=ft.BorderSide(1,BORDER),
                                     top=ft.BorderSide(1,BORDER),  bottom=ft.BorderSide(1,BORDER)),
                ))
        page.update()

    def cad_produto(e):
        try: cod = int(fp_cod.value or "0"); qtd = int(fp_qtd.value or "0")
        except ValueError: _fb(fb_prod, "Código e quantidade devem ser números.", ok=False); return
        nome = (fp_nome.value or "").strip()
        if not cod or not nome: _fb(fb_prod, "Preencha código e nome.", ok=False); return
        res = api.cadastrar_produto_gerente(cod, nome, qtd)
        if "erro" in res: _fb(fb_prod, res["erro"], ok=False)
        else:
            _fb(fb_prod, "Produto cadastrado!")
            fp_cod.value = ""; fp_nome.value = ""; fp_qtd.value = ""; page.update()
            carregar_produtos()

    def atu_produto(e):
        try: cod = int(fp_cod.value or "0"); qtd = int(fp_qtd.value or "0")
        except ValueError: _fb(fb_prod, "Código e quantidade devem ser números.", ok=False); return
        nome = (fp_nome.value or "").strip()
        if not cod or not nome: _fb(fb_prod, "Preencha código e nome.", ok=False); return
        res = api.atualizar_produto(cod, nome, qtd)
        if "erro" in res: _fb(fb_prod, res["erro"], ok=False)
        else:
            _fb(fb_prod, "Produto atualizado!")
            fp_cod.value = ""; fp_nome.value = ""; fp_qtd.value = ""; page.update()
            carregar_produtos()

    def _btn_style_accent():
        return ft.ButtonStyle(
            bgcolor={"": ACCENT, "hovered": "#3DA89E"}, color=TEXT,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(left=18, right=18, top=10, bottom=10),
        )

    def _btn_style_neutral():
        return ft.ButtonStyle(
            bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"}, color=TEXT,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.Padding(left=18, right=18, top=10, bottom=10),
        )

    def _btn_style_ghost():
        return ft.ButtonStyle(color=MUTED, side=ft.BorderSide(1, BORDER),
                              shape=ft.RoundedRectangleBorder(radius=8),
                              padding=ft.Padding(left=16, right=16, top=10, bottom=10))

    produtos_sec_content = ft.Column([
        ft.Text("Produtos", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card(ft.Column([
            ft.Text("Cadastrar / Editar produto", size=14, color=MUTED, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("Código", color=MUTED, size=12), fp_cod],  expand=1, spacing=4),
                ft.Column([ft.Text("Nome",   color=MUTED, size=12), fp_nome], expand=2, spacing=4),
                ft.Column([ft.Text("Qtd",    color=MUTED, size=12), fp_qtd],  expand=1, spacing=4),
            ], spacing=12),
            ft.Container(height=4),
            fb_prod,
            ft.Row([
                ft.Button(content=ft.Text("Cadastrar", color=TEXT, size=13), on_click=cad_produto, style=_btn_style_accent()),
                ft.Button(content=ft.Text("Atualizar", color=TEXT, size=13), on_click=atu_produto, style=_btn_style_neutral()),
                ft.Button("Limpar", on_click=lambda e: (setattr(fp_cod, 'value', ''), setattr(fp_nome, 'value', ''), setattr(fp_qtd, 'value', ''), page.update()), style=_btn_style_ghost()),
            ], spacing=8),
        ], spacing=8)),
        ft.Container(height=12),
        ft.Text("Produtos cadastrados", size=14, color=MUTED),
        ft.Container(height=4),
        prod_lista,
    ], spacing=4, scroll=ft.ScrollMode.AUTO)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Fornecedores (herdada do gerente)
    # ══════════════════════════════════════════════════════════════════════════
    fb_forn = ft.Text("", size=13, visible=False)
    ff_cnpj = _field("00.000.000/0001-00")
    ff_nome = _field("Ex: Distribuidora XYZ")
    ff_tel  = _field("(11) 90000-0000", kb=ft.KeyboardType.PHONE)
    forn_lista = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def carregar_fornecedores():
        forn_lista.controls.clear()
        itens = api.get_fornecedores_gerente()
        if not itens:
            forn_lista.controls.append(ft.Text("Nenhum fornecedor cadastrado.", color=MUTED, size=14))
        else:
            for f in itens:
                cnpj = f.get("cnpj", ""); nome = f.get("nome", ""); tel = f.get("telefone", "")

                def _fill_f(e, c=cnpj, n=nome, t=tel):
                    ff_cnpj.value = c; ff_nome.value = n; ff_tel.value = t; page.update()

                def _del_f(e, c=cnpj):
                    res = api.deletar_fornecedor(c)
                    if "erro" in res: _fb(fb_forn, res["erro"], ok=False)
                    else: _fb(fb_forn, "Fornecedor removido."); carregar_fornecedores(); page.update()

                forn_lista.controls.append(ft.Container(
                    content=ft.Row([
                        ft.Text(cnpj, color=MUTED, size=12, width=140),
                        ft.Text(nome, color=TEXT,  size=13, expand=True),
                        ft.Text(tel,  color=MUTED, size=12, width=130),
                        ft.IconButton(ft.Icons.EDIT_OUTLINED,  icon_color=ACCENT, icon_size=18, tooltip="Editar",  on_click=_fill_f),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ERR,    icon_size=18, tooltip="Remover", on_click=_del_f),
                    ], spacing=4),
                    bgcolor=CARD, border_radius=8,
                    padding=ft.Padding(left=12, right=8, top=10, bottom=10),
                    border=ft.Border(left=ft.BorderSide(1,BORDER), right=ft.BorderSide(1,BORDER),
                                     top=ft.BorderSide(1,BORDER),  bottom=ft.BorderSide(1,BORDER)),
                ))
        page.update()

    def cad_fornecedor(e):
        cnpj = (ff_cnpj.value or "").strip(); nome = (ff_nome.value or "").strip(); tel = (ff_tel.value or "").strip()
        if not cnpj or not nome: _fb(fb_forn, "Preencha CNPJ e nome.", ok=False); return
        res = api.cadastrar_fornecedor_gerente(cnpj, nome, tel)
        if "erro" in res: _fb(fb_forn, res["erro"], ok=False)
        else:
            _fb(fb_forn, "Fornecedor cadastrado!")
            ff_cnpj.value = ""; ff_nome.value = ""; ff_tel.value = ""; page.update()
            carregar_fornecedores()

    def atu_fornecedor(e):
        cnpj = (ff_cnpj.value or "").strip(); nome = (ff_nome.value or "").strip(); tel = (ff_tel.value or "").strip()
        if not cnpj or not nome: _fb(fb_forn, "Preencha CNPJ e nome.", ok=False); return
        res = api.atualizar_fornecedor(cnpj, nome, tel)
        if "erro" in res: _fb(fb_forn, res["erro"], ok=False)
        else:
            _fb(fb_forn, "Fornecedor atualizado!")
            ff_cnpj.value = ""; ff_nome.value = ""; ff_tel.value = ""; page.update()
            carregar_fornecedores()

    fornecedores_sec_content = ft.Column([
        ft.Text("Fornecedores", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card(ft.Column([
            ft.Text("Cadastrar / Editar fornecedor", size=14, color=MUTED, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("CNPJ",     color=MUTED, size=12), ff_cnpj], expand=2, spacing=4),
                ft.Column([ft.Text("Nome",     color=MUTED, size=12), ff_nome], expand=3, spacing=4),
                ft.Column([ft.Text("Telefone", color=MUTED, size=12), ff_tel],  expand=2, spacing=4),
            ], spacing=12),
            ft.Container(height=4),
            fb_forn,
            ft.Row([
                ft.Button(content=ft.Text("Cadastrar", color=TEXT, size=13), on_click=cad_fornecedor, style=_btn_style_accent()),
                ft.Button(content=ft.Text("Atualizar", color=TEXT, size=13), on_click=atu_fornecedor, style=_btn_style_neutral()),
                ft.Button("Limpar", on_click=lambda e: (setattr(ff_cnpj,'value',''), setattr(ff_nome,'value',''), setattr(ff_tel,'value',''), page.update()), style=_btn_style_ghost()),
            ], spacing=8),
        ], spacing=8)),
        ft.Container(height=12),
        ft.Text("Fornecedores cadastrados", size=14, color=MUTED),
        ft.Container(height=4),
        forn_lista,
    ], spacing=4, scroll=ft.ScrollMode.AUTO)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Relatório PDF (herdada do gerente, usa prefixo admin)
    # ══════════════════════════════════════════════════════════════════════════
    rel_status = ft.Text("", size=14, visible=False)
    rel_prog   = ft.ProgressRing(width=24, height=24, stroke_width=3, color=ACCENT, visible=False)

    def gerar_relatorio(e):
        rel_status.visible = False; rel_prog.visible = True; page.update()
        caminho = api.baixar_relatorio_pdf(prefixo="admin")
        rel_prog.visible = False
        if caminho and not caminho.startswith("erro"):
            rel_status.value = f"✓  PDF salvo em:\n{caminho}"; rel_status.color = SUCC
        else:
            rel_status.value = f"✗  {caminho or 'Falha ao gerar relatório.'}"; rel_status.color = ERR
        rel_status.visible = True; page.update()

    relatorio_sec_content = ft.Column([
        ft.Text("Relatório", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card(ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PICTURE_AS_PDF_OUTLINED, color=ERR, size=36),
                ft.Column([
                    ft.Text("Exportar relatório de estoque", color=TEXT, size=15, weight=ft.FontWeight.W_500),
                    ft.Text("Gera um PDF com todos os itens e movimentações.", color=MUTED, size=12),
                ], spacing=2, expand=True),
            ], spacing=16),
            ft.Container(height=12),
            ft.Row([
                ft.Button(
                    content=ft.Row([ft.Icon(ft.Icons.DOWNLOAD_OUTLINED, color=TEXT, size=16),
                                    ft.Text("Baixar PDF", color=TEXT, size=14)], spacing=8, tight=True),
                    on_click=gerar_relatorio,
                    style=ft.ButtonStyle(
                        bgcolor={"": "#C0392B", "hovered": "#E74C3C"}, color=TEXT,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                    ),
                ),
                rel_prog,
            ], spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=4),
            rel_status,
        ], spacing=8)),
    ], spacing=4)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO: Usuários (exclusiva do admin)
    # ══════════════════════════════════════════════════════════════════════════
    fb_usr  = ft.Text("", size=13, visible=False)
    fu_nome = _field("Ex: João Silva")
    fu_login = _field("Ex: joao.silva")
    fu_senha = _field("Mínimo 6 caracteres", password=True)

    fu_tipo = ft.Dropdown(
        hint_text="Cargo",
        hint_style=ft.TextStyle(color=MUTED),
        options=[
            ft.dropdown.Option("estoquista",    "Estoquista"),
            ft.dropdown.Option("gerente",       "Gerente"),
            ft.dropdown.Option("administrador", "Administrador"),
        ],
        border_color=BORDER, focused_border_color=ACCENT,
        text_style=ft.TextStyle(color=TEXT),
        bgcolor=INPUT, border_radius=8, expand=True,
    )

    usuarios_lista = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)

    def carregar_usuarios():
        usuarios_lista.controls.clear()
        itens = api.get_usuarios()
        if not itens:
            usuarios_lista.controls.append(ft.Text("Nenhum usuário encontrado.", color=MUTED, size=14))
        else:
            for u in itens:
                uid  = u.get("id", 0)
                nome = u.get("nome", "")
                login = u.get("login", "")
                tipo  = u.get("tipo", "estoquista")
                tc, tb = TIPO_COLOR.get(tipo, ("#8E8E93", "#2A2A30"))
                tlbl   = TIPO_LABEL.get(tipo, tipo.capitalize())

                # Dropdown inline de cargo para cada usuário
                cargo_dd = ft.Dropdown(
                    value=tipo,
                    options=[
                        ft.dropdown.Option("estoquista",    "Estoquista"),
                        ft.dropdown.Option("gerente",       "Gerente"),
                        ft.dropdown.Option("administrador", "Administrador"),
                    ],
                    border_color=BORDER, focused_border_color=ACCENT,
                    text_style=ft.TextStyle(color=TEXT, size=13),
                    bgcolor=INPUT, border_radius=6, width=150,
                    content_padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                )

                # Identifica se esta linha é o próprio usuário logado
                eh_eu = (login == get_state("login"))

                def _alterar_tipo(e, uid_=uid, dd=cargo_dd, n=nome):
                    novo_tipo = dd.value
                    if not novo_tipo:
                        return
                    res = api.alterar_tipo_usuario(uid_, novo_tipo)
                    if "erro" in res:
                        _fb(fb_usr, res["erro"], ok=False)
                    else:
                        _fb(fb_usr, f"Cargo de '{n}' alterado para {TIPO_LABEL.get(novo_tipo, novo_tipo)}.")
                        carregar_usuarios()


                def _del_usr(e, uid_=uid, n=nome):
                    res = api.deletar_usuario(uid_)
                    if "erro" in res:
                        _fb(fb_usr, res["erro"], ok=False)
                    else:
                        _fb(fb_usr, f"Usuário '{n}' removido.")
                        carregar_usuarios()

                btn_del = ft.IconButton(
                    ft.Icons.PERSON_REMOVE_OUTLINED if eh_eu else ft.Icons.DELETE_OUTLINE,
                    icon_color="#555560" if eh_eu else ERR,
                    icon_size=20,
                    tooltip="Não é possível excluir sua própria conta" if eh_eu else "Remover usuário",
                    on_click=(lambda e: None) if eh_eu else _del_usr,
                    disabled=eh_eu,
                )

                usuarios_lista.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(nome[0].upper() if nome else "?", size=13,
                                                color=TEXT, weight=ft.FontWeight.BOLD),
                                bgcolor="#4A235A" if eh_eu else "#1A5276", border_radius=20,
                                width=32, height=32, alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column([
                                ft.Row([
                                    ft.Text(nome,  color=TEXT,  size=14, weight=ft.FontWeight.W_500),
                                    *([ ft.Container(
                                            content=ft.Text("você", size=10, color=ADMIN_COLOR,
                                                            weight=ft.FontWeight.W_600),
                                            bgcolor=ADMIN_BG, border_radius=4,
                                            padding=ft.Padding(left=6, right=6, top=2, bottom=2),
                                        ) ] if eh_eu else []),
                                ], spacing=6),
                                ft.Text(login, color=MUTED, size=12),
                            ], spacing=1, expand=True),
                            ft.Container(
                                content=ft.Text(tlbl, size=11, color=tc, weight=ft.FontWeight.W_600),
                                bgcolor=tb, border_radius=6,
                                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            ),
                            cargo_dd,
                            ft.IconButton(
                                ft.Icons.CHECK_CIRCLE_OUTLINE,
                                icon_color=SUCC, icon_size=20,
                                tooltip="Confirmar cargo",
                                on_click=_alterar_tipo,
                                disabled=eh_eu,
                            ),
                            btn_del,
                        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=CARD, border_radius=8,
                        padding=ft.Padding(left=16, right=8, top=12, bottom=12),
                        border=ft.Border(left=ft.BorderSide(1,BORDER), right=ft.BorderSide(1,BORDER),
                                         top=ft.BorderSide(1,BORDER),  bottom=ft.BorderSide(1,BORDER)),
                    )
                )
        page.update()

    def criar_usuario(e):
        nome  = (fu_nome.value or "").strip()
        login = (fu_login.value or "").strip()
        senha = (fu_senha.value or "").strip()
        tipo  = fu_tipo.value

        if not nome or not login or not senha:
            _fb(fb_usr, "Preencha nome, login e senha.", ok=False); return
        if not tipo:
            _fb(fb_usr, "Selecione um cargo.", ok=False); return
        if len(senha) < 6:
            _fb(fb_usr, "Senha deve ter no mínimo 6 caracteres.", ok=False); return

        res = api.criar_usuario(nome, login, senha, tipo)
        if "erro" in res:
            _fb(fb_usr, res["erro"], ok=False)
        else:
            _fb(fb_usr, f"Usuário '{nome}' criado com sucesso!")
            fu_nome.value = ""; fu_login.value = ""; fu_senha.value = ""; fu_tipo.value = None
            page.update()
            carregar_usuarios()

    usuarios_sec_content = ft.Column([
        ft.Text("Usuários", size=18, color=TEXT, weight=ft.FontWeight.W_600),
        ft.Container(height=8),
        _card(ft.Column([
            ft.Text("Criar novo usuário", size=14, color=MUTED, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            ft.Row([
                ft.Column([ft.Text("Nome completo", color=MUTED, size=12), fu_nome],  expand=3, spacing=4),
                ft.Column([ft.Text("Login",         color=MUTED, size=12), fu_login], expand=2, spacing=4),
            ], spacing=12),
            ft.Row([
                ft.Column([ft.Text("Senha",  color=MUTED, size=12), fu_senha], expand=3, spacing=4),
                ft.Column([ft.Text("Cargo",  color=MUTED, size=12), fu_tipo],  expand=2, spacing=4),
            ], spacing=12),
            ft.Container(height=4),
            fb_usr,
            ft.Row([
                ft.Button(
                    content=ft.Row([ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, color=TEXT, size=16),
                                    ft.Text("Criar usuário", color=TEXT, size=14)], spacing=8, tight=True),
                    on_click=criar_usuario,
                    style=ft.ButtonStyle(
                        bgcolor={"": ADMIN_COLOR, "hovered": "#A855F7"}, color="#1C1C1E",
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                    ),
                ),
                ft.Button("Limpar", on_click=lambda e: (
                    setattr(fu_nome,'value',''), setattr(fu_login,'value',''),
                    setattr(fu_senha,'value',''), setattr(fu_tipo,'value', None), page.update()
                ), style=_btn_style_ghost()),
            ], spacing=12),
        ], spacing=8)),
        ft.Container(height=16),
        ft.Row([
            ft.Text("Usuários cadastrados", size=14, color=MUTED, expand=True),
            ft.TextButton(
                "Atualizar lista",
                icon=ft.Icons.REFRESH,
                on_click=lambda e: carregar_usuarios(),
                style=ft.ButtonStyle(color=ACCENT),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Container(height=4),
        usuarios_lista,
    ], spacing=4, scroll=ft.ScrollMode.AUTO)

    # ══════════════════════════════════════════════════════════════════════════
    # Contêineres de seção
    # ══════════════════════════════════════════════════════════════════════════
    movimentacao_sec   = ft.Container(content=formulario,               expand=True, visible=True)
    consultar_sec      = ft.Container(content=consultar_col,            expand=True, visible=False)
    produtos_sec       = ft.Container(content=produtos_sec_content,     expand=True, visible=False)
    fornecedores_sec   = ft.Container(content=fornecedores_sec_content, expand=True, visible=False)
    relatorio_sec      = ft.Container(content=relatorio_sec_content,    expand=True, visible=False)
    usuarios_sec       = ft.Container(content=usuarios_sec_content,     expand=True, visible=False)

    _all_secs = [movimentacao_sec, consultar_sec, produtos_sec,
                 fornecedores_sec, relatorio_sec, usuarios_sec]

    _sec_map = {
        "entrada":      movimentacao_sec,
        "saida":        movimentacao_sec,
        "consultar":    consultar_sec,
        "produtos":     produtos_sec,
        "fornecedores": fornecedores_sec,
        "relatorio":    relatorio_sec,
        "usuarios":     usuarios_sec,
    }

    # ══════════════════════════════════════════════════════════════════════════
    # Navegação lateral
    # ══════════════════════════════════════════════════════════════════════════
    nav_refs = {}
    nav_txts = {}

    def make_nav(key: str, label: str, active: bool = False) -> ft.Container:
        txt = ft.Text(label, color=TEXT if active else MUTED, size=14,
                      weight=ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL)
        nav_txts[key] = txt
        c = ft.Container(content=txt,
                         padding=ft.Padding(left=20, right=20, top=11, bottom=11),
                         bgcolor="#2A2A30" if active else None,
                         border_radius=6, ink=True)
        nav_refs[key] = c
        return c

    def switch_nav(key: str):
        for k in nav_refs:
            a = k == key
            nav_txts[k].color  = TEXT if a else MUTED
            nav_txts[k].weight = ft.FontWeight.W_500 if a else ft.FontWeight.NORMAL
            nav_refs[k].bgcolor = "#2A2A30" if a else None

        for s in _all_secs:
            s.visible = False
        _sec_map[key].visible = True

        if key in ("entrada", "saida"): switch_mode(key)
        elif key == "consultar":    carregar_consultar()
        elif key == "produtos":     carregar_produtos()
        elif key == "fornecedores": carregar_fornecedores()
        elif key == "usuarios":     carregar_usuarios()

        page.update()

    nav_entrada      = make_nav("entrada",      "Entrada",      active=True)
    nav_saida        = make_nav("saida",        "Saída")
    nav_consultar    = make_nav("consultar",    "Consultar")
    nav_produtos     = make_nav("produtos",     "Produtos")
    nav_fornecedores = make_nav("fornecedores", "Fornecedores")
    nav_relatorio    = make_nav("relatorio",    "Relatório")
    nav_usuarios     = make_nav("usuarios",     "Usuários")

    nav_entrada.on_click      = lambda e: switch_nav("entrada")
    nav_saida.on_click        = lambda e: switch_nav("saida")
    nav_consultar.on_click    = lambda e: switch_nav("consultar")
    nav_produtos.on_click     = lambda e: switch_nav("produtos")
    nav_fornecedores.on_click = lambda e: switch_nav("fornecedores")
    nav_relatorio.on_click    = lambda e: switch_nav("relatorio")
    nav_usuarios.on_click     = lambda e: switch_nav("usuarios")

    def logout(e):
        api.clear(); clear_state(); page.go("/login")

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
                    _nav_group("ESTOQUE"),
                    nav_entrada, nav_saida, nav_consultar,
                    ft.Container(height=4),
                    _nav_group("GESTÃO"),
                    nav_produtos, nav_fornecedores, nav_relatorio,
                    ft.Container(height=4),
                    _nav_group("ADMINISTRAÇÃO"),
                    nav_usuarios,
                ], spacing=2),
                padding=ft.Padding(left=8, right=8, top=0, bottom=0),
            ),
            ft.Container(expand=True),
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(
                content=ft.TextButton("Sair", icon=ft.Icons.LOGOUT, on_click=logout,
                                      style=ft.ButtonStyle(color=MUTED)),
                padding=ft.Padding(left=8, right=8, top=8, bottom=8),
            ),
        ], spacing=0, expand=True),
        width=200, bgcolor=SB,
        border=ft.Border(right=ft.BorderSide(1, BORDER)),
    )

    top_bar = ft.Container(
        content=ft.Row([
            ft.Text("Administrador — gestão completa do sistema", color=MUTED, size=12),
            ft.Row([
                ft.Container(
                    content=ft.Text("Admin", size=11, color=ADMIN_COLOR, weight=ft.FontWeight.W_600),
                    bgcolor=ADMIN_BG, border_radius=6,
                    padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                ),
                ft.Container(
                    content=ft.Text(iniciais, size=12, color=TEXT, weight=ft.FontWeight.BOLD),
                    bgcolor="#4A235A", border_radius=20, width=32, height=32,
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
                    movimentacao_sec, consultar_sec,
                    produtos_sec, fornecedores_sec,
                    relatorio_sec, usuarios_sec,
                ], expand=True),
                expand=True, padding=20,
            ),
        ], spacing=0, expand=True),
        expand=True,
    )

    return ft.View(
        route="/admin",
        controls=[ft.Row([sidebar, main_area], expand=True, spacing=0)],
        bgcolor=BG,
        padding=0,
    )
