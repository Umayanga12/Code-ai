from posix import access
from ssl import Options
from typing import List, Optional

from pydantic import BaseModel, Field

""" Project Information Models """


class isPublicUse(BaseModel):
    """Public use information"""

    public: str = Field(
        ...,
        description="Indicates if the project is publicly accessible or limited to a specific group",
    )
    user_number: int = Field(
        ...,
        description="Number of users expected to use the project approximately",
    )
    expect_traffic: str = Field(
        ...,
        description="Indicates if the project expects high traffic",
    )


class ProjectInfo(BaseModel):
    """Basic information about the project"""

    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(
        None, description="Detailed description of the project"
    )
    type: str = Field(
        ...,
        description="Type of application system. mobile app or web based system or desktop application or all",
    )
    systemUse: isPublicUse = Field(
        ...,
        description="Information about the system's usage for planning the project",
    )


class UserAccess(BaseModel):
    """User access information"""

    role: str = Field(..., description="Role of the user")
    access_level: str = Field(
        ...,
        description="Access level of the user. what does that user role allow them to do",
    )


class SystemUser(BaseModel):
    """User information about the system"""

    login_Data: str = Field(
        ...,
        description="What are the data use to loginto system. such as username/email password etc.",
    )
    user_types: List[UserAccess] = Field(
        ...,
        description="List of user types that can access the system",
    )


class DeploymentPreferences(BaseModel):
    """User preferences regarding deployment strategy"""

    use_docker: bool = Field(
        False, description="Indicates if the project should be dockerized"
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


class techstack(BaseModel):
    for_frontend: str = Field(
        ...,
        description="technology that need to use for the frontend. default is React",
    )
    for_backend: str = Field(
        ..., description="technology that need to use for backend. default python"
    )


class ProjectMetadata(BaseModel):
    """Comprehensive metadata describing overall project setup"""

    project_info: ProjectInfo = Field(
        ..., description="Core information about the project"
    )
    programming_language: techstack = Field(
        ..., description="Primary tech stack used in the project"
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
        default_factory=list,
        description="Possible options or values for this property. for example for genders, male, female, other",
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
    """Missing information - ask ONE question at a time."""

    missing_item: str = Field(
        default="",
        description="The SINGLE most important missing or ambiguous field that you need clarification on RIGHT NOW. Ask about ONE thing at a time, not multiple things."
    )
    question: str = Field(
        default="",
        description="A SINGLE, specific question to ask the user to provide the ONE missing piece of information identified in missing_item. If all information is complete, leave this empty."
    )


class CompleteRequirement(BaseModel):
    project_metadata: ProjectMetadata = Field(
        ...,
        description="Full metadata and configuration of the project. getting the idea about the user's technology preferaces for the project",
    )
    sys_user: List[SystemUser] = Field(
        ..., description="System users and there details like access rights and roles"
    )
    entities: List[Entity] = Field(
        ..., description="List of entities involved in the project"
    )
    relationships: List[Relationship] = Field(
        ..., description="Relationships connecting the entities"
    )
    missing_info: MissingInfo = Field(..., description="Missing information")

class SpecialNote(BaseModel):
    special_ppoints: List[str] = Field(
        ...,
        description="special notes or points that need to consider which is mentioned by the user"
    )

class RequirmentAgentResponceModel(BaseModel):
    requirements: CompleteRequirement = Field(..., description="Complete requirements")
    SpecialNote: Optional[SpecialNote] 


