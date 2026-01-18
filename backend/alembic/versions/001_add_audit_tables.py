"""Add audit and XAI tables

Revision ID: 001
Revises:
Create Date: 2024-01-18 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add audit tables"""

    # Create users table if not exists
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(100), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('api_key_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(100), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=True),
        sa.Column('resource_id', sa.String(100), nullable=True),
        sa.Column('request_data', postgresql.JSON(), nullable=True),
        sa.Column('response_summary', postgresql.JSON(), nullable=True),
        sa.Column('metadata', postgresql.JSON(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='success'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('duration_ms', sa.Integer(), nullable=True)
    )

    # Create ai_request_traces table
    op.create_table(
        'ai_request_traces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('request_id', sa.String(50), unique=True, nullable=False),
        sa.Column('audit_log_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('api_key_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('input_messages', postgresql.JSON(), nullable=False),
        sa.Column('input_tokens', sa.Integer(), default=0),
        sa.Column('system_prompt', sa.Text(), nullable=True),
        sa.Column('requested_provider', sa.String(50), nullable=True),
        sa.Column('selected_provider', sa.String(50), nullable=False),
        sa.Column('selected_model', sa.String(100), nullable=False),
        sa.Column('routing_reason', sa.String(200), nullable=True),
        sa.Column('routing_metadata', postgresql.JSON(), nullable=True),
        sa.Column('context_sources_used', postgresql.JSON(), nullable=True),
        sa.Column('context_data_summary', postgresql.JSON(), nullable=True),
        sa.Column('output_content', sa.Text(), nullable=True),
        sa.Column('output_tokens', sa.Integer(), default=0),
        sa.Column('finish_reason', sa.String(50), nullable=True),
        sa.Column('cost_usd', sa.Float(), default=0.0),
        sa.Column('cost_breakdown', postgresql.JSON(), nullable=True),
        sa.Column('total_latency_ms', sa.Integer(), nullable=True),
        sa.Column('provider_latency_ms', sa.Integer(), nullable=True),
        sa.Column('context_fetch_latency_ms', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('error_type', sa.String(100), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True)
    )

    # Create ai_explanations table
    op.create_table(
        'ai_explanations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('trace_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ai_request_traces.id'), nullable=False),
        sa.Column('explanation_ar', sa.Text(), nullable=True),
        sa.Column('explanation_en', sa.Text(), nullable=True),
        sa.Column('routing_factors', postgresql.JSON(), nullable=True),
        sa.Column('context_relevance_scores', postgresql.JSON(), nullable=True),
        sa.Column('response_confidence', sa.Float(), nullable=True),
        sa.Column('response_categories', postgresql.JSON(), nullable=True),
        sa.Column('potential_issues', postgresql.JSON(), nullable=True),
        sa.Column('pii_detected', sa.Boolean(), default=False),
        sa.Column('pii_types', postgresql.JSON(), nullable=True),
        sa.Column('data_sensitivity', sa.String(20), nullable=True),
        sa.Column('compliance_flags', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Create usage_metrics table
    op.create_table(
        'usage_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('period_type', sa.String(20), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('provider', sa.String(50), nullable=True),
        sa.Column('total_requests', sa.Integer(), default=0),
        sa.Column('successful_requests', sa.Integer(), default=0),
        sa.Column('failed_requests', sa.Integer(), default=0),
        sa.Column('total_input_tokens', sa.Integer(), default=0),
        sa.Column('total_output_tokens', sa.Integer(), default=0),
        sa.Column('total_cost_usd', sa.Float(), default=0.0),
        sa.Column('avg_latency_ms', sa.Float(), nullable=True),
        sa.Column('p95_latency_ms', sa.Float(), nullable=True),
        sa.Column('p99_latency_ms', sa.Float(), nullable=True),
        sa.Column('requests_by_provider', postgresql.JSON(), nullable=True),
        sa.Column('cost_by_provider', postgresql.JSON(), nullable=True),
        sa.Column('requests_by_status', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Create indexes
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('ix_ai_request_traces_user_id', 'ai_request_traces', ['user_id'])
    op.create_index('ix_ai_request_traces_created_at', 'ai_request_traces', ['created_at'])
    op.create_index('ix_ai_request_traces_request_id', 'ai_request_traces', ['request_id'])
    op.create_index('ix_usage_metrics_user_id', 'usage_metrics', ['user_id'])
    op.create_index('ix_usage_metrics_period', 'usage_metrics', ['period_start', 'period_end'])


def downgrade():
    """Drop audit tables"""
    op.drop_index('ix_usage_metrics_period')
    op.drop_index('ix_usage_metrics_user_id')
    op.drop_index('ix_ai_request_traces_request_id')
    op.drop_index('ix_ai_request_traces_created_at')
    op.drop_index('ix_ai_request_traces_user_id')
    op.drop_index('ix_audit_logs_created_at')
    op.drop_index('ix_audit_logs_user_id')

    op.drop_table('usage_metrics')
    op.drop_table('ai_explanations')
    op.drop_table('ai_request_traces')
    op.drop_table('audit_logs')
    op.drop_table('users')
