import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base

def gen_uuid():
    return str(uuid.uuid4())

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer")
    progress = relationship("CustomerProgress", back_populates="customer")
    tickets = relationship("SupportTicket", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    product_code = Column(String(100), default="koryxa-assistant-ia")
    amount_minor = Column(Integer, default=11000)  # 11 000 XOF
    currency = Column(String(10), default="XOF")
    status = Column(String(30), default="pending")  # pending, succeeded, failed, cancelled
    idempotency_key = Column(String(150), unique=True, index=True, nullable=False)
    checkout_id = Column(String(150), nullable=True)
    checkout_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    payments = relationship("PaymentRecord", back_populates="order")

class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    payment_id = Column(String(150), unique=True, index=True, nullable=False)
    provider = Column(String(50), nullable=True)
    amount_received = Column(Integer, nullable=False)
    currency = Column(String(10), default="XOF")
    status = Column(String(30), nullable=False)
    event_id = Column(String(150), nullable=True, index=True)
    raw_payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="payments")

class CustomerProgress(Base):
    __tablename__ = "customer_progress"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    step_number = Column(Integer, nullable=False)  # 1 to 6
    step_title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="progress")

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    conversation_json = Column(Text, nullable=False)  # Diagnostic logs & chat history
    status = Column(String(30), default="open")  # open, resolved
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="tickets")

class OutboxEmail(Base):
    __tablename__ = "outbox_emails"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    email_type = Column(String(50), nullable=False)  # access, drip_j2, drip_j5, drip_j10
    recipient = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(30), default="pending")  # pending, sent, cancelled, failed
    retry_count = Column(Integer, default=0)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)

class DownloadLog(Base):
    __tablename__ = "download_logs"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    customer_id = Column(String(36), nullable=False)
    asset_name = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=True)
    downloaded_at = Column(DateTime, default=datetime.utcnow)
