"""OpenAPI documentation configuration for the Mood Tracker application."""

from pydantic import BaseModel


class ProjectDocs(BaseModel):
    """Container for OpenAPI specification metadata."""

    # Info for OpenAPI specification
    class OpenAPI:
        """OpenAPI specification fields: title, version, contact, license, and tags."""

        VERSION = "0.1.0"
        WEBSITE_URL = "https://example.com"
        TITLE = "Mood Tracker"
        DESCRIPTION = (
            """A  lightweight  internal  tool  designed  for  agile  teams  to monitor collective well-being"""
        )

        @property
        def CONTACT_INFO(self) -> dict:
            """Return contact information dict for the OpenAPI spec."""
            return {
                "name": "Contact Name",
                "url": self.WEBSITE_URL,
                "email": "contact@gmail.com",
            }

        LICENSE_INFO = {
            "name": "MIT License",
        }

        TAGS_INFO: list[dict[str, str]] = [
            # {
            #     "name": "Example Tag",
            #     "description": "Example Tag Description",
            # }
        ]

        @property
        def specification(self) -> dict:
            """Return the full OpenAPI specification dict for the inner OpenAPI class."""
            return {
                "title": self.TITLE,
                "description": self.DESCRIPTION,
                "version": self.VERSION,
                "contact": self.CONTACT_INFO,
                "license_info": self.LICENSE_INFO,
                "openapi_tags": self.TAGS_INFO,
            }

    @property
    def specification(self) -> dict:
        """Return the merged OpenAPI specification dict."""
        return {**self.OpenAPI().specification}


project_docs = ProjectDocs()
