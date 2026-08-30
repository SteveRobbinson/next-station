from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field, ConfigDict, AliasChoices, AfterValidator, AliasPath

def ensure_one_element(value: Any) -> str:
    if isinstance(value, list):
        if len(value) != 1:
            raise ValueError(f"Expected one file url, got: {len(value)}.")

        else:
            return value[0]

    else:
        return value


class FileUrl(BaseModel):
    file_url: Annotated[str, BeforeValidator(ensure_one_element), Field(alias='files')]


class GetFileUrl(BaseModel):
    list_url: Annotated[list[FileUrl], Field(alias='data', min_length = 1)]
    def __getitem__(self, index):
        return self.list_url[index].file_url


def ensure_string(value: Any) -> str:
    if isinstance(value, str):
        return value.strip().strip('"')

    else:
        return value


class ApiMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    etag: Annotated[str,
                    Field(validation_alias=AliasChoices('ETag', 'etag', 'Etag')),
                    AfterValidator(ensure_string)]


class S3Etag(BaseModel):
    s3_etag: Annotated[str, AfterValidator(ensure_string), Field(AliasPath('Metadata', 'ETag'))]
