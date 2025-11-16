from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Component(BaseModel):
    """Basic building block/component of the system architecture"""

    name: str = Field(..., description="Component name")
    type: str = Field(
        ...,
        description="Type of component: service, database, cache, messaging, front-end,queues,messag brokers, third-party, etc.",
    )
    description: Optional[str] = Field(
        None, description="Detailed description of the component"
    )
    technologies: List[str] = Field(
        default_factory=list, description="Tech stack or frameworks used"
    )
    responsibilities: List[str] = Field(
        default_factory=list, description="Primary responsibilities or functions"
    )


class CommunicationProtocol(BaseModel):
    protocol: str = Field(
        ...,
        description="Protocol/communication method such as HTTP, gRPC, MQ, WebSocket",
    )
    description: Optional[str] = Field(
        None, description="Additional information about communication method"
    )


class IntegrationPoint(BaseModel):
    source_component: str = Field(..., description="Name of the source component")
    target_component: str = Field(..., description="Name of the target component")
    communication_protocol: CommunicationProtocol = Field(
        ..., description="How components communicate"
    )
    data_formats: List[str] = Field(
        default_factory=list,
        description="Data formats exchanged e.g., JSON, XML, Protobuf",
    )
    description: Optional[str] = Field(
        None, description="Details about the integration"
    )


class DeploymentNode(BaseModel):
    name: str = Field(..., description="Name or identifier of the deployment node")
    type: str = Field(
        ...,
        description="Type of deployment node; e.g., container, VM, serverless function, edge device",
    )
    platform: Optional[str] = Field(
        None, description="Platform or provider e.g., AWS EC2, Kubernetes Pod"
    )
    components_deployed: List[str] = Field(
        default_factory=list,
        description="Components deployed on this node",
    )
    scaling_policy: Optional[str] = Field(
        None, description="Scaling strategy for this node"
    )


class SystemArchitectureModel(BaseModel):
    architectural_style: str = Field(
        ...,
        description="Main architectural paradigm or style e.g., layered, microservices, event-driven, serverless",
    )
    components: List[Component] = Field(..., description="List of system components")
    integration_points: List[IntegrationPoint] = Field(
        ..., description="Inter-component connections and communication details"
    )
    deployment_topology: List[DeploymentNode] = Field(
        ..., description="Definition of deployment nodes with hosted components"
    )
    non_functional_requirements: Optional[Dict[str, str]] = Field(
        None,
        description="Non-functional requirements relevant to architecture e.g., latency, availability",
    )
    security_measures: Optional[Dict[str, str]] = Field(
        None,
        description="Security mechanisms integrated into architecture e.g., encryption, secure communication",
    )
    monitoring_logging: Optional[Dict[str, str]] = Field(
        None, description="Monitoring and logging tools and strategies"
    )
    notes: Optional[str] = Field(
        None, description="Additional comments or architecture considerations"
    )
