from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ScalabilityStrategy(BaseModel):
    strategy_name: str = Field(
        ..., description="Scalability approach (e.g., vertical, horizontal, hybrid)"
    )
    description: Optional[str] = Field(
        None, description="Details about how scaling is achieved"
    )
    components_scaled: List[str] = Field(
        default_factory=list, description="System components targeted for scaling"
    )


class MicroserviceDetails(BaseModel):
    name: str = Field(..., description="Name of the microservice")
    responsibility: str = Field(
        ..., description="Business capability handled by the microservice"
    )
    interfaces: List[str] = Field(
        default_factory=list, description="APIs or interfaces exposed/consumed"
    )
    expected_load_rps: Optional[int] = Field(
        None, description="Expected requests per second handled"
    )
    data_store: Optional[str] = Field(
        None, description="Primary database or data store used"
    )


class SystemArchitecture(BaseModel):
    architecture_type: str = Field(
        ..., description="E.g., monolithic, microservices, serverless, etc."
    )
    services: Optional[List[MicroserviceDetails]] = Field(
        default_factory=list, description="Details of microservices"
    )
    messaging_systems: Optional[List[str]] = Field(
        default_factory=list, description="Messaging or event streaming platforms used"
    )
    load_balancing: Optional[str] = Field(
        None, description="Load balancing strategy or tools"
    )
    caching_strategy: Optional[str] = Field(
        None, description="Caching mechanisms applied"
    )


class SecurityPlanning(BaseModel):
    authentication_mechanisms: List[str] = Field(
        default_factory=list, description="Authentication methods (OAuth, JWT, SAML)"
    )
    authorization_models: List[str] = Field(
        default_factory=list, description="Authorization patterns (RBAC, ABAC)"
    )
    data_encryption: Optional[str] = Field(
        None, description="Details on data encryption at rest/in transit"
    )
    compliance_requirements: Optional[List[str]] = Field(
        default_factory=list, description="Compliance or regulatory considerations"
    )


class PerformancePlanning(BaseModel):
    rps_target: Optional[int] = Field(None, description="Target requests per second")
    latency_sla_ms: Optional[int] = Field(
        None, description="Latency Service Level Agreement in milliseconds"
    )
    throughput_target: Optional[int] = Field(
        None, description="Target throughput, e.g., transactions per second"
    )
    monitoring_tools: Optional[List[str]] = Field(
        default_factory=list, description="Tools for monitoring performance metrics"
    )


class DeploymentPlanning(BaseModel):
    environment_strategy: List[str] = Field(
        default_factory=list,
        description="Dev, staging, production environment strategy",
    )
    container_orchestration: Optional[str] = Field(
        None, description="E.g., Kubernetes, ECS"
    )
    ci_cd_pipeline_tools: Optional[List[str]] = Field(
        default_factory=list, description="CI/CD tools and automation"
    )
    rollback_strategy: Optional[str] = Field(
        None, description="Mechanisms for rollback in deployments"
    )


class ResourceEstimation(BaseModel):
    cpu_cores: Optional[int] = Field(None, description="Estimated CPU cores required")
    memory_gb: Optional[int] = Field(
        None, description="Estimated memory required in GB"
    )
    storage_gb: Optional[int] = Field(
        None, description="Estimated storage required in GB"
    )
    network_bandwidth_mbps: Optional[int] = Field(
        None, description="Estimated network bandwidth requirement in Mbps"
    )


class PlannerAgentModel(BaseModel):
    project_name: str = Field(..., description="Project or system name")
    system_complexity: str = Field(
        ..., description="Complexity level e.g., simple, moderate, complex"
    )
    user_scale: str = Field(
        ..., description="User scale e.g., single user, thousands, millions"
    )
    architecture: SystemArchitecture = Field(
        ..., description="Architecture planning details"
    )
    scalability: Optional[ScalabilityStrategy] = Field(
        None, description="Scalability strategies and details"
    )
    security: Optional[SecurityPlanning] = Field(
        None, description="Security planning details"
    )
    performance: Optional[PerformancePlanning] = Field(
        None, description="Performance targets and monitoring"
    )
    deployment: Optional[DeploymentPlanning] = Field(
        None, description="Deployment strategies and tools"
    )
    resource_estimation: Optional[ResourceEstimation] = Field(
        None, description="Resource needs estimation"
    )
    notes: Optional[str] = Field(
        None, description="Any additional notes or considerations"
    )
