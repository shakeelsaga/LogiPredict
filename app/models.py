from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime
from datetime import datetime, timezone

# I'm initializing the db object here, but not attaching it to the Flask app yet.
# This is my strategy to prevent circular import errors in Python.
db = SQLAlchemy()

class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'

    # I've set up the primary key for this model.
    id: Mapped[int] = mapped_column(primary_key=True)

    # These are the inputs I'll be using for my predictions.
    origin_city: Mapped[str] = mapped_column(String(100), nullable=False)
    destination_city: Mapped[str] = mapped_column(String(100), nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # This is where I'll store the AI's output.
    predicted_hours: Mapped[float] = mapped_column(Float, nullable=False)

    # I need an audit trail, so this column automatically records when I make a prediction.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<PredictionLog {self.origin_city} -> {self.destination_city}: {self.predicted_hours}h>"