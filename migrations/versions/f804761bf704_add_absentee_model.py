"""Add Absentee model

Revision ID: f804761bf704
Revises: be43cd401d59
Create Date: 2022-10-24 03:37:02.353659

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f804761bf704"
down_revision = "be43cd401d59"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "absentee",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("absent_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("absent_date", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("absentee")
    # ### end Alembic commands ###
