from typing import List, Optional

from pydantic import BaseModel, Field

""" Project Information Models """


class ProjectInfo(BaseModel):
    """Basic information about the project"""

    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(
        None, description="Detailed description of the project"
    )


class DeploymentPreferences(BaseModel):
    """User preferences regarding deployment strategy"""

    use_docker: Optional[bool] = Field(
        None, description="Indicates if the project should be dockerized"
    )
    deploy_project: bool = Field(
        False, description="Indicates if the project needs deployment"
    )
    use_terraform: bool = Field(
        False,
        description="Indicates if Terraform will be used for infrastructure as code",
    )
    cloud_provider: Optional[str] = Field(
        None, description="Name of the cloud provider (e.g., AWS, Azure, GCP)"
    )


class CICDPreferences(BaseModel):
    """Preferences for Continuous Integration and Continuous Deployment (CI/CD)"""

    enable_cicd: bool = Field(
        False, description="Indicates if CI/CD pipelines are required"
    )
    ci_cd_provider: Optional[str] = Field(
        None, description="CI/CD service provider name (e.g., Jenkins, GitHub Actions)"
    )


class ProjectMetadata(BaseModel):
    """Comprehensive metadata describing overall project setup"""

    project_info: ProjectInfo = Field(
        ..., description="Core information about the project"
    )
    programming_language: str = Field(
        ..., description="Primary language used in the project"
    )
    database_type: str = Field(
        ..., description="Primary database technology for the project"
    )
    deployment: DeploymentPreferences = Field(
        ..., description="Deployment-related preferences"
    )
    cicd: CICDPreferences = Field(..., description="CI/CD-related preferences")


""" Domain Modeling for Requirements """


class Property(BaseModel):
    name: str = Field(..., description="Name of the property/attribute")
    options: List[str] = Field(
        default_factory=list, description="Possible options or values for this property"
    )


class Behavior(BaseModel):
    description: str = Field(
        ..., description="Description of an entity's behavior or function"
    )


class Entity(BaseModel):
    name: str = Field(..., description="Name of the entity")
    description: str = Field(..., description="Brief description of the entity")
    properties: List[Property] = Field(
        default_factory=list, description="Attributes or properties of the entity"
    )
    behaviors: List[Behavior] = Field(
        default_factory=list,
        description="Behaviors or functions associated with the entity",
    )


class Relationship(BaseModel):
    source: str = Field(..., description="ID of the source entity in the relationship")
    target: str = Field(..., description="ID of the target entity in the relationship")
    description: str = Field(
        ...,
        description="Explanation of the relationship's nature or role or purpose or what it represents",
    )


class MissingInfo(BaseModel):
    """Missing information."""

    missing_info: List[str] = Field(
        ..., description="List of missing or ambiguous fields"
    )
    question: str = Field(
        ..., description="Question to ask the user to provide the missing information"
    )


class CompleteRequirement(BaseModel):
    project_metadata: ProjectMetadata = Field(
        ..., description="Full metadata and configuration of the project"
    )
    entities: List[Entity] = Field(
        ..., description="List of entities involved in the project"
    )
    relationships: List[Relationship] = Field(
        ..., description="Relationships connecting the entities"
    )
    missing_info: MissingInfo = Field(..., description="Missing information")


class RequirmentAgentResponceModel(BaseModel):
    requirements: CompleteRequirement = Field(..., description="Complete requirements")
