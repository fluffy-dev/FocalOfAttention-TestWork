import json
from typing import List, Any, Type, Tuple

from pydantic import Field
from pydantic.fields import FieldInfo

from pydantic_settings import BaseSettings, EnvSettingsSource, PydanticBaseSettingsSource


class MyCustomSource(EnvSettingsSource):
    """A custom settings source to parse specific environment variables.

    This class extends Pydantic's `EnvSettingsSource` to provide custom
    parsing logic. It is specifically designed to handle environment variables
    that contain comma-separated lists, such as the CORS settings, and convert
    them into proper Python lists. It also includes a fallback to attempt
    JSON decoding for other values.
    """
    def prepare_field_value(
            self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        """Parses a raw value from an environment variable for a given field.

        If the field is one of the designated CORS list fields, this method
        splits the comma-separated string value into a list of strings. For
        any other field, it attempts to parse the value as a JSON object,
        which allows for structured data to be passed via environment
        variables. If the value is empty or not set, it is returned as is.

        Args:
            field_name (str): The name of the settings field being processed.
            field (FieldInfo): The Pydantic field information object.
            value (Any): The raw value obtained from the environment.
            value_is_complex (bool): A flag indicating if the value is complex.

        Returns:
            Any: The processed value, converted to a list or parsed from JSON
                where applicable.
        """
        if field_name in ["allow_origins", "allow_methods", "allow_headers", "expose_headers"]:
            if isinstance(value, str):
                return [item.strip() for item in value.split(",")]

        return value


class Settings(BaseSettings):
    """A Pydantic model for Cross-Origin Resource Sharing (CORS) settings.

    This class centralizes all CORS-related configuration for the application.
    It uses `pydantic-settings` to load values from environment variables,
    mapping them from aliases like `CORS_ALLOW_ORIGINS`. It is configured to
    use `MyCustomSource` for custom parsing of these variables.

    Attributes:
        allow_origins (List[str]): A list of origins that are permitted to make
            cross-site requests. Defaults to ["*"].
        allow_methods (List[str]): A list of HTTP methods that are allowed for
            cross-site requests. Defaults to ["GET"].
        allow_headers (List[str]): A list of HTTP headers that can be used in
            cross-site requests. Defaults to ["*"].
        allow_credentials (bool): Indicates whether cookies should be supported
            for cross-site requests. Defaults to False.
        allow_origin_regex (str | None): A regex string to match against origins
            that are allowed to make cross-site requests. Defaults to None.
        expose_headers (List[str]): A list of headers that browsers are allowed
            to access in responses to cross-site requests. Defaults to ["*"].
        max_age (int): The maximum time in seconds that the results of a
            preflight request can be cached by a client. Defaults to 600.
    """
    allow_origins: List[str] = Field(default=["*"], alias="CORS_ALLOW_ORIGINS")
    allow_methods: List[str] = Field(default=["GET"], alias="CORS_ALLOW_METHODS")
    allow_headers: List[str] = Field(default=["*"], alias="CORS_ALLOW_HEADERS")
    allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")
    allow_origin_regex: str | None = Field(None, alias="CORS_ALLOW_ORIGIN_REGEX")
    expose_headers: List[str] = Field(default=["*"], alias="CORS_EXPOSE_HEADERS")
    max_age: int = Field(default=600, alias="CORS_MAX_AGE")

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Customizes the settings sources for the `Settings` class.

        This method overrides the default source loading behavior of Pydantic.
        It is configured to exclusively use `MyCustomSource`, ensuring that all
        settings are loaded from environment variables and processed with the
        custom parsing logic defined in that class.

        Args:
            settings_cls (Type[BaseSettings]): The settings class itself.
            init_settings (PydanticBaseSettingsSource): Source for settings
                passed during model initialization.
            env_settings (PydanticBaseSettingsSource): The default environment
                variable source.
            dotenv_settings (PydanticBaseSettingsSource): Source for settings
                from a .env file.
            file_secret_settings (PydanticBaseSettingsSource): Source for
                settings from secrets files.

        Returns:
            Tuple[PydanticBaseSettingsSource, ...]: A tuple containing only
                the custom source to be used.
        """
        return (MyCustomSource(settings_cls),)


# A singleton instance of the Settings class that will be imported
# and used across the application to access CORS configuration.
settings = Settings()