from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.itemEstoque import ItemEstoque
from app.models.fornecedor import Fornecedor
from app.models.estoque import Estoque
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# ── Produto ──────────────────────────────────────────────

def _get_or_create_estoque(db: Session) -> int:
    """Retorna o id do primeiro registro de Estoque, criando um se não existir."""
    estoque = db.query(Estoque).first()
    if not estoque:
        estoque = Estoque()
        db.add(estoque)
        db.flush()
    return estoque.id


def cadastrar_produto(db: Session, codigo: int, nome: str, quantidade: int):
    produto_existente = db.query(Produto).filter(Produto.codigo == codigo).first()
    if produto_existente:
        return {"erro": "Código já existente"}

    novo_produto = Produto(codigo=codigo, nome=nome)
    db.add(novo_produto)
    db.flush()

    estoque_id = _get_or_create_estoque(db)
    novo_item = ItemEstoque(
        produto_codigo=novo_produto.codigo,
        estoque_id=estoque_id,
        quantidade=quantidade,
    )
    db.add(novo_item)
    db.commit()

    return {"mensagem": "Produto cadastrado", "produto": {"codigo": codigo, "nome": nome, "quantidade": quantidade}}


def atualizar_produto(db: Session, codigo: int, nome: str, quantidade: int):
    item = (
        db.query(ItemEstoque)
        .join(Produto)
        .filter(Produto.codigo == codigo)
        .first()
    )

    if not item:
        return {"erro": "Código inexistente"}

    item.produto.nome = nome
    item.quantidade = quantidade
    db.commit()
    db.refresh(item)

    return {
        "mensagem": "Produto atualizado",
        "produto": {
            "codigo": item.produto.codigo,
            "nome": item.produto.nome,
            "quantidade": item.quantidade
        }
    }


def deletar_produto(db: Session, codigo: int):
    produto = db.query(Produto).filter(Produto.codigo == codigo).first()

    if not produto:
        return {"erro": "Código inexistente"}

    item = db.query(ItemEstoque).filter(ItemEstoque.produto_codigo == produto.codigo).first()
    if item:
        db.delete(item)

    db.delete(produto)
    db.commit()

    return {"mensagem": "Produto deletado"}


def listar_produtos(db: Session):
    itens = db.query(ItemEstoque).join(Produto).all()

    return [
        {
            "codigo": item.produto.codigo,
            "nome": item.produto.nome,
            "quantidade": item.quantidade
        }
        for item in itens
    ]


# ── Fornecedor ───────────────────────────────────────────

def validar_formato_cnpj(cnpj: str) -> bool:
    return bool(re.match(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", cnpj))


def cadastrar_fornecedor(db: Session, cnpj: str, nome: str, telefone: str):
    if not validar_formato_cnpj(cnpj):
        return {"erro": "Formato incorreto de CNPJ"}

    existente = db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()
    if existente:
        return {"erro": "CNPJ já cadastrado"}

    novo = Fornecedor(cnpj=cnpj, nome=nome, telefone=telefone)
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"mensagem": "Fornecedor cadastrado", "fornecedor": {"cnpj": cnpj, "nome": nome, "telefone": telefone}}


def atualizar_fornecedor(db: Session, cnpj: str, nome: str, telefone: str):
    if not validar_formato_cnpj(cnpj):
        return {"erro": "Formato incorreto de CNPJ"}

    fornecedor = db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()
    if not fornecedor:
        return {"erro": "CNPJ inexistente"}

    fornecedor.nome = nome
    fornecedor.telefone = telefone
    db.commit()
    db.refresh(fornecedor)

    return {"mensagem": "Fornecedor atualizado", "fornecedor": {"cnpj": cnpj, "nome": nome, "telefone": telefone}}


def deletar_fornecedor(db: Session, cnpj: str):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()
    if not fornecedor:
        return {"erro": "CNPJ inexistente"}

    db.delete(fornecedor)
    db.commit()

    return {"mensagem": "Fornecedor deletado"}


def listar_fornecedores(db: Session):
    fornecedores = db.query(Fornecedor).all()

    return [
        {"cnpj": f.cnpj, "nome": f.nome, "telefone": f.telefone}
        for f in fornecedores
    ]


# ── Relatório ────────────────────────────────────────────
def gerar_relatorio_pdf(db: Session):
    produtos = listar_produtos(db)
    fornecedores = listar_fornecedores(db)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, altura - 50, "Relatório de Estoque")

    # Produtos
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, altura - 100, "Produtos:")
    pdf.setFont("Helvetica", 10)

    y = altura - 120
    for p in produtos:
        pdf.drawString(50, y, f"Código: {p['codigo']} | Nome: {p['nome']} | Quantidade: {p['quantidade']}")
        y -= 20
        if y < 100:
            pdf.showPage()
            y = altura - 50

    # Fornecedores
    pdf.setFont("Helvetica-Bold", 12)
    y -= 20
    pdf.drawString(50, y, "Fornecedores:")
    pdf.setFont("Helvetica", 10)
    y -= 20

    for f in fornecedores:
        pdf.drawString(50, y, f"CNPJ: {f['cnpj']} | Nome: {f['nome']} | Telefone: {f['telefone']}")
        y -= 20
        if y < 100:
            pdf.showPage()
            y = altura - 50

    pdf.save()
    buffer.seek(0)
    return buffer