"""
Database models for Jobs Watcher
"""

import os
import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()    

def init_db(app):
    """Initialize database with app configuration"""
    logger.info("Initializing database...")
    
    # Database configuration
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable is required!")
        raise ValueError("DATABASE_URL environment variable must be set")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db, migrate

@dataclass
class User(db.Model):
    """User model for Telegram users"""
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    def __repr__(self):
        return f'<User {self.telegram_id}: {self.first_name}>'
    
    @classmethod
    def find_or_create(cls, telegram_user):
        """Find existing user or create new one from Telegram user data"""
        user = cls.query.filter_by(telegram_id=telegram_user.id).first()
        
        if not user:
            user = cls(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            db.session.add(user)
            db.session.commit()
        else:
            # Update user info if changed
            user.username = telegram_user.username
            user.first_name = telegram_user.first_name
            user.last_name = telegram_user.last_name
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
        return user
