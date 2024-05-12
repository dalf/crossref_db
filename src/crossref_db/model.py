from sqlmodel import Field, SQLModel


class Paper(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    doi: str = Field(index=True)
    title: str | None = Field(index=True)


class ReferenceTmp(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    doi: str
    ref_to_doi: str


class Reference(SQLModel, table=True):
    paper_id: int | None = Field(default=None, foreign_key="paper.id", primary_key=True)
    ref_id: int | None = Field(default=None, foreign_key="paper.id", primary_key=True)
