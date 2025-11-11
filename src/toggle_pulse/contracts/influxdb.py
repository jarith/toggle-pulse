from pydantic import BaseModel, ConfigDict


class InfluxDBBaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
    )


class InfluxDBPoint(InfluxDBBaseModel):
    measurement: str
    tags: dict[str, str]
    fields: dict[str, int | float | str | bool]
    time: int

    def to_line_protocol(self) -> str:
        sorted_tags = sorted(self.tags.items())
        tags_str = ",".join(f"{key}={value}" for key, value in sorted_tags)

        fields_parts: list[str] = []
        for key, value in self.fields.items():
            if isinstance(value, str):
                escaped_value = value.replace('"', '\\"')
                fields_parts.append(f'{key}="{escaped_value}"')
            elif isinstance(value, bool):
                fields_parts.append(f"{key}={str(value).lower()}")
            else:
                fields_parts.append(f"{key}={value}")

        fields_str = ",".join(fields_parts)

        return f"{self.measurement},{tags_str} {fields_str} {self.time}"


class InfluxDBBatch(InfluxDBBaseModel):
    points: list[InfluxDBPoint]

    def __len__(self) -> int:
        return len(self.points)

    def to_line_protocol(self) -> str:
        if not self.points:
            return ""
        return "\n".join(point.to_line_protocol() for point in self.points)
