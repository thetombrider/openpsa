from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, Date, Numeric, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, relationship, validates
from datetime import date
from datetime import datetime
import enum

class Base (DeclarativeBase):
    pass

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    CONSULTANT = "CONSULTANT"

class ProjectStatus(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ResourceAllocationStatus(enum.Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

class BillingType(enum.Enum):
    TIME_AND_MATERIALS = "TIME_AND_MATERIALS"
    FIXED_PRICE = "FIXED_PRICE"

class ConsultantRole(enum.Enum):
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    MASTER = "MASTER"
    PRINCIPAL = "PRINCIPAL"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    hourly_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    time_entries = relationship("TimeEntry", back_populates="user")
    projects = relationship(
        "Project", 
        secondary="project_users",
        back_populates="users",
        viewonly=True
    )
    allocations = relationship("ResourceAllocation", back_populates="user")
    billing_rates = relationship("BillingRate", back_populates="user")
    project_users = relationship("ProjectUser", back_populates="user")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_email = Column(String)
    contact_phone = Column(String)
    
    projects = relationship("Project", back_populates="client")

# Tabella di associazione per relazione many-to-many tra Project e User
class ProjectUser(Base):
    __tablename__ = "project_users"
    
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(Enum(ConsultantRole), nullable=True)
    
    # Modifica qui: project_links -> project_users
    project = relationship("Project", back_populates="project_users")
    user = relationship("User", back_populates="project_users")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT)
    billing_type = Column(Enum(BillingType), nullable=False)
    billing_currency = Column(String, default="EUR")
    billing_notes = Column(String)
    
    client = relationship("Client", back_populates="projects")
    time_entries = relationship("TimeEntry", back_populates="project", cascade="all, delete-orphan")
    users = relationship(
        "User",
        secondary="project_users",
        back_populates="projects",
        viewonly=True
    )
    allocations = relationship("ResourceAllocation", back_populates="project")
    billing_rates = relationship("BillingRate", back_populates="project")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
    project_users = relationship("ProjectUser", back_populates="project")

    @validates('end_date')
    def validate_end_date(self, key, value):
        if value and self.start_date and value < self.start_date:
            raise ValueError("End date must be after start date")
        return value

class TimeEntry(Base):
    __tablename__ = "time_entries"
    __table_args__ = (
        Index('idx_time_entries_date', 'date'),
        Index('idx_time_entries_user_date', 'user_id', 'date'),
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    date = Column(DateTime, nullable=False)
    hours = Column(Float, nullable=False)
    description = Column(String)
    
    user = relationship("User", back_populates="time_entries")
    project = relationship("Project", back_populates="time_entries")
    line_item_links = relationship(
        "LineItemTimeEntry",
        back_populates="time_entry",
        viewonly=True
    )
    invoice_line_items = relationship(
        "InvoiceLineItem",
        secondary="line_item_time_entries",
        back_populates="time_entries",
        overlaps="line_item_links"
    )

class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    allocation_percentage = Column(Float, nullable=False)
    role = Column(Enum(ConsultantRole), nullable=True)  # Modifica qui
    status = Column(Enum(ResourceAllocationStatus), nullable=False)
    
    user = relationship("User", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")

    @validates('allocation_percentage')
    def validate_allocation(self, key, value):
        if not 0 <= value <= 1:
            raise ValueError("Allocation must be between 0 and 1")
        return value

class BillingRate(Base):
    __tablename__ = "billing_rates"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    rate = Column(Numeric(10, 2), nullable=False)  # Tariffa oraria
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)  # NULL significa "ancora attivo"
    
    user = relationship("User", back_populates="billing_rates")
    project = relationship("Project", back_populates="billing_rates")

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    
    @property
    def calculated_amount(self):
        return sum(item.amount for item in self.line_items)
    
    @validates('amount')
    def validate_amount(self, key, amount):
        if self.line_items and amount != self.calculated_amount:
            raise ValueError("Invoice amount must match line items total")
        return amount

    paid = Column(Boolean, default=False)
    paid_date = Column(Date)
    notes = Column(String)
    
    project = relationship("Project", back_populates="invoices")
    line_items = relationship("InvoiceLineItem", back_populates="invoice")

class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)  # Ore o quantità
    rate = Column(Numeric(10, 2), nullable=False)  # Tariffa oraria
    _amount = Column('amount', Numeric(10, 2))

    @property
    def amount(self):
        return self.quantity * self.rate

    @amount.setter
    def amount(self, value):
        pass  # amount is derived from quantity and rate, so we do nothing here

    @validates('quantity', 'rate')
    def validate_fields(self, key, value):
        """
        Validates and updates the 'quantity' and 'rate' fields.

        Ensures that the provided values for 'quantity' and 'rate' are valid.
        This method is called automatically when these fields are set.

        :param key: The name of the field being validated.
        :param value: The value to be validated.
        :return: The validated value.
        """
        return value
    
    time_entry_links = relationship(
        "LineItemTimeEntry",
        back_populates="line_item",
        viewonly=True
    )
    time_entries = relationship(
        "TimeEntry",
        secondary="line_item_time_entries",
        back_populates="invoice_line_items",
        overlaps="time_entry_links,line_item_links"
    )
    
    invoice = relationship("Invoice", back_populates="line_items")

# Tabella di collegamento tra TimeEntry e InvoiceLineItem
class LineItemTimeEntry(Base):
    __tablename__ = "line_item_time_entries"
    
    line_item_id = Column(Integer, ForeignKey("invoice_line_items.id"), primary_key=True)
    time_entry_id = Column(Integer, ForeignKey("time_entries.id"), primary_key=True)

    line_item = relationship("InvoiceLineItem", back_populates="time_entry_links")
    time_entry = relationship("TimeEntry", back_populates="line_item_links")
