from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, Date, Numeric, Boolean, Index, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, relationship, validates, Mapped
from datetime import date
from datetime import datetime
import enum
from sqlalchemy import Enum as SQLAlchemyEnum
from src.schemas.enums import ResourceAllocationStatus
from typing import Optional, ClassVar
from decimal import Decimal

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
    CANCELLED = "CANCELLED"

class BillingType(enum.Enum):
    TIME_AND_MATERIALS = "TIME_AND_MATERIALS"
    FIXED_PRICE = "FIXED_PRICE"

class ConsultantRoleEnum(enum.Enum):
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    MASTER = "MASTER"
    PRINCIPAL = "PRINCIPAL"

class ConsultantRole(Base):
    __tablename__ = "consultant_roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')
    
    # Relazioni
    project_users = relationship("ProjectUser", back_populates="role")
    resource_allocations = relationship("ResourceAllocation", back_populates="role")

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String, unique=True, nullable=False)
    name: Mapped[str] = Column(String)
    role: Mapped[str] = Column(String, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now())
    
    # Campi privati per caching - non mappati nel DB
    _current_billing_rate: ClassVar[Optional[float]] = None
    _current_cost_rate: ClassVar[Optional[float]] = None
    
    # Relazioni corrette
    user_billing_rates = relationship(
        "UserBillingRate",
        back_populates="user"
    )
    user_cost_rates = relationship(
        "UserCostRate",
        back_populates="user"
    )
    # Aggiungi queste relazioni
    project_users = relationship("ProjectUser", back_populates="user")
    projects = relationship(
        "Project",
        secondary="project_users",
        back_populates="users",
        viewonly=True
    )
    allocations = relationship("ResourceAllocation", back_populates="user")
    time_entries = relationship("TimeEntry", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    
    @property
    def current_billing_rate(self) -> Optional[float]:
        if self._current_billing_rate is not None:
            return self._current_billing_rate
            
        today = date.today()
        current_rate = next(
            (rate for rate in sorted(
                self.user_billing_rates,
                key=lambda x: x.valid_from,
                reverse=True
            )
            if rate.valid_from <= today 
            and (rate.valid_to is None or rate.valid_to >= today)
            ),
            None
        )
        self._current_billing_rate = float(current_rate.billing_rate.rate) if current_rate else None
        return self._current_billing_rate
    
    @property
    def current_cost_rate(self) -> Optional[float]:
        if self._current_cost_rate is not None:
            return self._current_cost_rate
            
        today = date.today()
        current_rate = next(
            (rate for rate in sorted(
                self.user_cost_rates,
                key=lambda x: x.valid_from,
                reverse=True
            )
            if rate.valid_from <= today 
            and (rate.valid_to is None or rate.valid_to >= today)
            ),
            None
        )
        self._current_cost_rate = float(current_rate.cost_rate.rate) if current_rate else None
        return self._current_cost_rate

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
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("consultant_roles.id"))  # Rinominato da role a role_id
    
    # Relazioni
    project = relationship("Project", back_populates="project_users")
    user = relationship("User", back_populates="project_users")
    role = relationship("ConsultantRole", back_populates="project_users")

# Tabella di associazione per project_billing_rates
project_billing_rates = Table(
    'project_billing_rates', 
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE')),
    Column('billing_rate_id', Integer, ForeignKey('billing_rates.id', ondelete='CASCADE')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('active', Boolean, default=True)
)

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
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    client = relationship("Client", back_populates="projects")
    time_entries = relationship("TimeEntry", back_populates="project", cascade="all, delete-orphan")
    allocations = relationship("ResourceAllocation", back_populates="project")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
    project_users = relationship("ProjectUser", back_populates="project")
    team = relationship("Team", back_populates="projects")

    @validates('end_date')
    def validate_end_date(self, key, value):
        if value and self.start_date and value < self.start_date:
            raise ValueError("End date must be after start date")
        return value
    
    # Relazione many-to-many con User attraverso ProjectUser
    users = relationship(
        "User",
        secondary="project_users",
        viewonly=True,  # Questa è importante
        back_populates="projects"
    )

    # Aggiungi la relazione many-to-many
    billing_rates = relationship(
        "BillingRate",
        secondary=project_billing_rates,
        back_populates="projects"
    )

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
    role_id = Column(Integer, ForeignKey("consultant_roles.id"))  # Rinominato da role a role_id
    status = Column(SQLAlchemyEnum(ResourceAllocationStatus), nullable=False, 
                   default=ResourceAllocationStatus.PLANNED)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    user = relationship("User", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")
    role = relationship("ConsultantRole", back_populates="resource_allocations")

    @validates('allocation_percentage')
    def validate_allocation(self, key, value):
        if not 0 <= value <= 1:
            raise ValueError("Allocation must be between 0 and 1")
        return value

class BillingRate(Base):
    __tablename__ = "billing_rates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    rate = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="EUR")
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    user_billing_rates = relationship("UserBillingRate", back_populates="billing_rate")

    # Aggiungi la relazione inversa
    projects = relationship(
        "Project",
        secondary=project_billing_rates,
        back_populates="billing_rates"
    )

class CostRate(Base):
    __tablename__ = "cost_rates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    rate = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="EUR")
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    user_cost_rates = relationship("UserCostRate", back_populates="cost_rate")

class UserCostRate(Base):
    __tablename__ = "user_cost_rates"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cost_rate_id = Column(Integer, ForeignKey("cost_rates.id"), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    
    # Correzione della relazione
    user = relationship("User", back_populates="user_cost_rates")
    cost_rate = relationship("CostRate", back_populates="user_cost_rates")

class UserBillingRate(Base):
    __tablename__ = "user_billing_rates"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    billing_rate_id = Column(Integer, ForeignKey("billing_rates.id"), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)
    
    # Correzione della relazione
    user = relationship("User", back_populates="user_billing_rates")
    billing_rate = relationship("BillingRate", back_populates="user_billing_rates")

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
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    description = Column(String)
    quantity = Column(Numeric(10, 2))
    rate = Column(Numeric(10, 2))
    amount = Column(Numeric(10, 2))
    billing_rate_id = Column(Integer, ForeignKey("billing_rates.id"))
    billing_rate = relationship("BillingRate", backref="line_items")
    rate_at_creation = Column(Numeric(10, 2))
    currency_at_creation = Column(String)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.billing_rate:
            self.rate_at_creation = self.billing_rate.rate
            self.currency_at_creation = self.billing_rate.currency
    
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

    line_item = relationship(
        "InvoiceLineItem",
        back_populates="time_entry_links",
        overlaps="invoice_line_items,time_entries"
    )
    
    time_entry = relationship(
        "TimeEntry",
        back_populates="line_item_links",
        overlaps="invoice_line_items,time_entries"
    )

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    members = relationship("TeamMember", back_populates="team")
    projects = relationship("Project", back_populates="team")

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("consultant_roles.id"))
    join_date = Column(Date, nullable=False)
    leave_date = Column(Date)
    
    # Relazioni
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")
    role = relationship("ConsultantRole")
