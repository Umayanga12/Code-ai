from uuid import uuid4, UUID
from typing import Optional
from pydantic import BaseModel, Field

"""Project Information"""


class projectInfo(BaseModel):
    """Project basic information"""

    projectid: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(..., description="Project description")
    isUseDocker: bool = Field(
        False, description="Whether the project need to use docker"
    )


class deployment(BaseModel):
    """User preference about deployment"""

    isDeploying: bool = Field(
        False, description="Whether the project need to deploy or not"
    )

    need_terraform: bool = Field(
        False, description="Whether the project need to use terraform"
    )
    cloudprovider: Optional[str] = Field(None, description="Cloud provider")


class cicd(BaseModel):
    """User preference about cicd"""

    need_cicd: bool = Field(False, description="Whether the project need to use cicd")
    ci_provider: Optional[str] = Field(None, description="CI provider")


class MetaData(BaseModel):
    """Complete information about project"""

    projectInfo: projectInfo = Field(..., description="Project information")
    language: str = Field(..., description="Project language")
    database: str = Field(..., description="Project database")
    deployment: deployment = Field(..., description="Project deployment")
    cicd: cicd = Field(..., description="Project cicd")
