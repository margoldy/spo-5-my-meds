from fastapi import FastAPI

from app.api import auth, courses, intakes, medications, schedules, users


app = FastAPI(
    title="Моя аптечка API",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(medications.router)
app.include_router(courses.router)
app.include_router(schedules.router)
app.include_router(intakes.router)
