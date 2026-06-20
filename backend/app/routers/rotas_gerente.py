from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.gerente import (
    ProdutoSchema,
    ProdutoDeleteSchema,
    FornecedorSchema,
    FornecedorDeleteSchema
)
from app.services.gerente import (
    cadastrar_produto,
    atualizar_produto,
    deletar_produto,
    listar_produtos,
    cadastrar_fornecedor,
    atualizar_fornecedor,
    deletar_fornecedor,
    listar_fornecedores,
    gerar_relatorio
)

from fastapi.responses import StreamingResponse
from app.services.gerente import gerar_relatorio_pdf

router = APIRouter()

# ── Produto ──────────────────────────────────────────────

@router.get("/produtos")
def get_produtos(db: Session = Depends(get_db)):
    return listar_produtos(db)

@router.post("/produto")
def post_produto(dados: ProdutoSchema, db: Session = Depends(get_db)):
    return cadastrar_produto(db, dados.codigo, dados.nome, dados.quantidade)

@router.put("/produto")
def put_produto(dados: ProdutoSchema, db: Session = Depends(get_db)):
    return atualizar_produto(db, dados.codigo, dados.nome, dados.quantidade)

@router.delete("/produto")
def del_produto(dados: ProdutoDeleteSchema, db: Session = Depends(get_db)):
    return deletar_produto(db, dados.codigo)

# ── Fornecedor ───────────────────────────────────────────

@router.get("/fornecedores")
def get_fornecedores(db: Session = Depends(get_db)):
    return listar_fornecedores(db)

@router.post("/fornecedor")
def post_fornecedor(dados: FornecedorSchema, db: Session = Depends(get_db)):
    return cadastrar_fornecedor(db, dados.cnpj, dados.nome, dados.telefone)

@router.put("/fornecedor")
def put_fornecedor(dados: FornecedorSchema, db: Session = Depends(get_db)):
    return atualizar_fornecedor(db, dados.cnpj, dados.nome, dados.telefone)

@router.delete("/fornecedor")
def del_fornecedor(dados: FornecedorDeleteSchema, db: Session = Depends(get_db)):
    return deletar_fornecedor(db, dados.cnpj)

# ── Relatório ────────────────────────────────────────────

@router.get("/relatorio/pdf")
def get_relatorio_pdf(db: Session = Depends(get_db)):
    buffer = gerar_relatorio_pdf(db)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio.pdf"}
    )