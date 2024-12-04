"""Fix circular import and update schema

Revision ID: 12bd874109e4
Revises: 9a0cb255ff6f
Create Date: 2024-11-30 02:46:31.196702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '12bd874109e4'
down_revision: Union[str, None] = '9a0cb255ff6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_nutritional_plan_id', table_name='nutritional_plan')
    op.drop_index('ix_nutritional_plan_plan_name', table_name='nutritional_plan')
    op.drop_table('nutritional_plan')
    op.drop_index('ix_meal_plans_meal_plan_id', table_name='meal_plans')
    op.drop_table('meal_plans')
    op.drop_index('ix_nutritional_plans_plan_id', table_name='nutritional_plans')
    op.drop_table('nutritional_plans')
    op.drop_index('ix_mealplans_id', table_name='mealplans')
    op.drop_table('mealplans')
    op.drop_index('ix_recipes_recipe_id', table_name='recipes')
    op.drop_table('recipes')
    op.drop_index('ix_motivations_message_id', table_name='motivations')
    op.drop_table('motivations')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('preference', postgresql.ENUM('vegan', 'vegetarian', 'omnivorous', name='preference_enum'), autoincrement=False, nullable=False),
    sa.Column('user_type', postgresql.ENUM('Nutritionist', 'Client', name='user_type_enum'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('username', name='users_username_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('motivations',
    sa.Column('message_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('message_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('message_id', name='motivations_pkey')
    )
    op.create_index('ix_motivations_message_id', 'motivations', ['message_id'], unique=False)
    op.create_table('recipes',
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('meal_plan_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name_recipe', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('portion', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('calories', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('carbohydrates', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('fats', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('type', postgresql.ENUM('vegan', 'vegetarian', 'omnivorous', name='recipe_type_enum'), autoincrement=False, nullable=False),
    sa.Column('ingredients', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('instructions', sa.TEXT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.meal_plan_id'], name='recipes_meal_plan_id_fkey'),
    sa.PrimaryKeyConstraint('recipe_id', name='recipes_pkey')
    )
    op.create_index('ix_recipes_recipe_id', 'recipes', ['recipe_id'], unique=False)
    op.create_table('mealplans',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='mealplans_pkey')
    )
    op.create_index('ix_mealplans_id', 'mealplans', ['id'], unique=False)
    op.create_table('nutritional_plans',
    sa.Column('plan_id', sa.INTEGER(), server_default=sa.text("nextval('nutritional_plans_plan_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nutritionist', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('calories', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('protein', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('carbohydrates', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('fats', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['nutritionist'], ['users.id'], name='nutritional_plans_nutritionist_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='nutritional_plans_user_id_fkey'),
    sa.PrimaryKeyConstraint('plan_id', name='nutritional_plans_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_nutritional_plans_plan_id', 'nutritional_plans', ['plan_id'], unique=False)
    op.create_table('meal_plans',
    sa.Column('meal_plan_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('plan_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['plan_id'], ['nutritional_plans.plan_id'], name='meal_plans_plan_id_fkey'),
    sa.PrimaryKeyConstraint('meal_plan_id', name='meal_plans_pkey')
    )
    op.create_index('ix_meal_plans_meal_plan_id', 'meal_plans', ['meal_plan_id'], unique=False)
    op.create_table('nutritional_plan',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('plan_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='nutritional_plan_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='nutritional_plan_pkey')
    )
    op.create_index('ix_nutritional_plan_plan_name', 'nutritional_plan', ['plan_name'], unique=False)
    op.create_index('ix_nutritional_plan_id', 'nutritional_plan', ['id'], unique=False)
    # ### end Alembic commands ###