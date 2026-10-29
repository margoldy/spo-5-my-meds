from pydantic import BaseModel, ConfigDict, Field, model_validator


class MedicationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    international_name: str | None = Field(default=None, max_length=255)
    manufacturer: str | None = Field(default=None, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    instruction_url: str | None = Field(default=None, max_length=2048)
    form: str | None = Field(default=None, max_length=100)
    strength: str | None = Field(default=None, max_length=100)


class MedicationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    international_name: str | None = Field(default=None, max_length=255)
    manufacturer: str | None = Field(default=None, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    instruction_url: str | None = Field(default=None, max_length=2048)
    form: str | None = Field(default=None, max_length=100)
    strength: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_active(self):
        if "is_active" in self.model_fields_set and self.is_active is None:
            raise ValueError("Состояние лекарства не может быть пустым")
        return self


class MedicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    international_name: str | None
    manufacturer: str | None
    category: str | None
    instruction_url: str | None
    form: str | None
    strength: str | None
    is_active: bool


class MedicationListResponse(BaseModel):
    items: list[MedicationResponse]
    total: int
