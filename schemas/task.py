from datetime import date
from enum import IntEnum

from pydantic import BaseModel, model_validator


class Priority(IntEnum):
    low = 1
    medium = 2
    high = 3


class TaskBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class NewTask(BaseModel):
    title: str
    description: str
    priority: Priority
    due_date: date
    completed: bool | None

    @model_validator(mode='after')
    def check_date(self):
        if self.due_date == date.today():
            self.completed = True
        return self


class CreatedTask(NewTask):
    id: int
    completed: bool
