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


def _field(hint: str, kb=None) -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=MUTED),
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        bgcolor=INPUT,
        border_radius=8,
        keyboard_type=kb,
        expand=True,
        text_size=14,
        content_padding=ft.Padding(left=12, right=12, top=10, bottom=10),
        border_width=1,
    )


def estoquista_view(page: ft.Page) -> ft.View:
    nome_usuario = get_state("nome") or "Estoquista"
    iniciais = "".join(p[0].upper() for p in nome_usuario.split()[:2]) or "ES"

    mode = {"value": "entrada"}

    # ── Campos ────────────────────────────────────────────────────────────
    f_codigo     = _field("Ex: 00412", kb=ft.KeyboardType.NUMBER)
    f_nome       = _field("Buscar por nome")
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

    feedback         = ft.Text("", size=13, visible=False)
    btn_label        = ft.Text("Registrar entrada", color=TEXT, size=14)
    btn_registrar    = ft.Button(
        content=btn_label,
        style=ft.ButtonStyle(
            bgcolor={"": "#3A3A3E", "hovered": "#4A4A4E"},
            color=TEXT,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
        ),
    )

    # ── Tabs ──────────────────────────────────────────────────────────────
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
            btn_label.value       = "Registrar entrada"
        else:
            tab_entrada_txt.color = MUTED
            tab_saida_txt.color   = TEXT
            ind_entrada.bgcolor   = "transparent"
            ind_saida.bgcolor     = ACCENT
            btn_label.value       = "Registrar saída"
        page.update()

    # ── Ações ─────────────────────────────────────────────────────────────
    def set_feedback(msg: str, ok: bool = True):
        feedback.value   = ("✓  " if ok else "✗  ") + msg
        feedback.color   = SUCC if ok else ERR
        feedback.visible = True
        page.update()

        def auto_hide():
            feedback.visible = False
            try:
                page.update()
            except Exception:
                pass

        threading.Timer(3.0, auto_hide).start()

    def limpar_campos():
        """Limpa apenas os campos, sem mexer no feedback."""
        for f in [f_codigo, f_nome, f_quantidade, f_obs]:
            f.value = ""
        f_unidade.value = None
        page.update()

    def limpar(e=None):
        limpar_campos()
        feedback.visible = False
        page.update()

    def registrar(e):
        feedback.visible = False
        page.update()

        try:
            codigo    = int(f_codigo.value or "0")
            nome_prod = (f_nome.value or "").strip()
            qtd       = int(f_quantidade.value or "0")
        except ValueError:
            set_feedback("Código e quantidade devem ser números.", ok=False)
            return

        if not codigo or not nome_prod or not qtd:
            set_feedback("Preencha código, nome e quantidade.", ok=False)
            return

        if mode["value"] == "entrada":
            res = api.registrar_entrada(codigo, nome_prod, qtd)
        else:
            res = api.registrar_saida(codigo, nome_prod, qtd)

        if "erro" in res:
            set_feedback(res["erro"], ok=False)
        else:
            # Limpa campos ANTES de mostrar feedback para não apagá-lo
            limpar_campos()
            set_feedback(res.get("mensagem", "Operação realizada com sucesso!"))

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

    formulario = ft.Container(
        content=ft.Column([
            ft.Text("Movimentação de estoque", size=18, color=TEXT, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            tabs_row,
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(height=8),
            ft.Row([
                ft.Column([
                    ft.Text("Código do produto", color=MUTED, size=12),
                    f_codigo,
                ], expand=True, spacing=4),
                ft.Column([
                    ft.Text("Nome do produto", color=MUTED, size=12),
                    f_nome,
                ], expand=True, spacing=4),
            ], spacing=16),
            ft.Row([
                ft.Column([
                    ft.Text("Quantidade", color=MUTED, size=12),
                    f_quantidade,
                ], expand=True, spacing=4),
                ft.Column([
                    ft.Text("Unidade", color=MUTED, size=12),
                    f_unidade,
                ], expand=True, spacing=4),
            ], spacing=16),
            ft.Column([
                ft.Text("Observação (opcional)", color=MUTED, size=12),
                f_obs,
            ], spacing=4),
            ft.Container(height=4),
            feedback,
            ft.Row([
                btn_registrar,
                ft.Button(
                    "Limpar",
                    on_click=limpar,
                    style=ft.ButtonStyle(
                        color=MUTED,
                        side=ft.BorderSide(1, BORDER),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                    ),
                ),
            ], spacing=12),
        ], spacing=8),
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

    # ── Consultar ─────────────────────────────────────────────────────────
    consultar_col = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    def carregar_consultar():
        """Recarrega os dados do banco toda vez que a aba Consultar é aberta."""
        consultar_col.controls.clear()
        consultar_col.controls.append(
            ft.Text("Estoque atual", size=18, color=TEXT, weight=ft.FontWeight.W_600)
        )
        consultar_col.controls.append(ft.Container(height=8))

        itens = api.get_estoque()
        if not itens:
            consultar_col.controls.append(
                ft.Text("Nenhum item no estoque ou erro ao conectar.", color=MUTED, size=14)
            )
        else:
            for item in itens:
                qtd    = item.get("quantidade", 0)
                status = "Normal" if qtd > 10 else "Baixo"
                s_c    = SUCC      if status == "Normal" else "#F59E0B"
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

    movimentacao_sec = ft.Container(content=formulario, expand=True, visible=True)
    consultar_sec    = ft.Container(
        content=consultar_col, expand=True, visible=False
    )

    # ── Navegação lateral ─────────────────────────────────────────────────
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

    def switch_nav(key: str):
        for k in nav_refs:
            active = k == key
            nav_txts[k].color  = TEXT if active else MUTED
            nav_txts[k].weight = ft.FontWeight.W_500 if active else ft.FontWeight.NORMAL
            nav_refs[k].bgcolor = "#2A2A30" if active else None

        movimentacao_sec.visible = key in ("entrada", "saida")
        consultar_sec.visible    = key == "consultar"

        if key in ("entrada", "saida"):
            switch_mode(key)
        elif key == "consultar":
            carregar_consultar()

        page.update()

    # Inicia na aba Entrada
    nav_entrada   = make_nav("entrada",   "Entrada",  active=True)
    nav_saida     = make_nav("saida",     "Saída")
    nav_consultar = make_nav("consultar", "Consultar")

    nav_entrada.on_click   = lambda e: switch_nav("entrada")
    nav_saida.on_click     = lambda e: switch_nav("saida")
    nav_consultar.on_click = lambda e: switch_nav("consultar")

    def logout(e):
        api.clear()
        clear_state()
        page.go("/login")

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("G-Estoque", size=15, color=TEXT, weight=ft.FontWeight.BOLD),
                padding=ft.Padding(left=20, right=0, top=20, bottom=16),
            ),
            ft.Divider(color=BORDER, thickness=0.5, height=1),
            ft.Container(height=8),
            ft.Container(
                content=ft.Column([nav_entrada, nav_saida, nav_consultar], spacing=2),
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
            ft.Text("Estoquista — movimentação de estoque", color=MUTED, size=12),
            ft.Row([
                ft.Container(
                    content=ft.Text("Estoquista", size=11, color=SUCC, weight=ft.FontWeight.W_600),
                    bgcolor="#14532D",
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
                content=ft.Column([movimentacao_sec, consultar_sec], expand=True),
                expand=True,
                padding=20,
            ),
        ], spacing=0, expand=True),
        expand=True,
    )

    return ft.View(
        route="/estoquista",
        controls=[ft.Row([sidebar, main_area], expand=True, spacing=0)],
        bgcolor=BG,
        padding=0,
    )