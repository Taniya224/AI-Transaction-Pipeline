from app.database.database import engine, Base
from app.database.models import Job

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")