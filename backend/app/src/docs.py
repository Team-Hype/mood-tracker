from pydantic import BaseModel


class ProjectDocs(BaseModel):
    # Info for OpenAPI specification
    class OpenAPI:
        VERSION = "0.1.0"
        WEBSITE_URL = "https://example.com"
        TITLE = "Mood Tracker"
        DESCRIPTION = """A  lightweight  internal  tool  designed  for  agile  teams  to monitor collective well-being"""

        @property
        def CONTACT_INFO(self) -> dict:
            return {
                "name": "Contact Name",
                "url": self.WEBSITE_URL,
                "email": "contact@gmail.com",
            }

        LICENSE_INFO = {
            "name": "MIT License",
        }

        TAGS_INFO = [
            # {
            #     "name": "Example Tag",
            #     "description": "Example Tag Description",
            # }
        ]

        @property
        def specification(self) -> dict:
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
        return {**self.OpenAPI().specification}


project_docs = ProjectDocs()
