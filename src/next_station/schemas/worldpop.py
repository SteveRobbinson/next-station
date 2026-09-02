from collections.abc import Sequence
from typing import Annotated

from pydantic import (
    AfterValidator,
    AliasChoices,
    AliasPath,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
)


def ensure_one_element(value: Sequence[str] | str) -> str:
    if isinstance(value, str):
        return value

    if len(value) != 1:
        raise ValueError(f"Expected one file url, got: {len(value)}.")

    return value[0]


class FileUrl(BaseModel):
    file_url: Annotated[str, BeforeValidator(ensure_one_element), Field(alias="files")]


class GetFileUrl(BaseModel):
    list_url: Annotated[list[FileUrl], Field(alias="data", min_length=1)]

    def __getitem__(self, index: int) -> str:
        return self.list_url[index].file_url


def clean_string(value: str) -> str:
    return value.strip(' \t\n\r"')


class ApiMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    etag: Annotated[
        str,
        Field(validation_alias=AliasChoices("ETag", "etag", "Etag")),
        AfterValidator(clean_string),
    ]


class S3Etag(BaseModel):
    s3_etag: Annotated[
        str, AfterValidator(clean_string), Field(AliasPath("Metadata", "ETag"))
    ]
