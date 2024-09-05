import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.models.base import Base


class Author(Base):
    __tablename__ = "author"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        sa.Uuid(as_uuid=True),
        primary_key=True,
    )
    fio: Mapped[str]
    url: Mapped[str]
    poems: Mapped[list["Poem"]] = relationship(back_populates="author")


class Poem(Base):
    __tablename__ = "poem"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        sa.Uuid(as_uuid=True),
        primary_key=True,
    )
    author_uuid: Mapped[str] = mapped_column(sa.ForeignKey("author.uuid"))
    author: Mapped["Author"] = relationship(back_populates="poems")
    text: Mapped[str] = mapped_column(sa.Text)
    url: Mapped[str]
