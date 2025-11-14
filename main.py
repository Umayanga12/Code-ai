import json
import os
import sys

from pydantic import ValidationError

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(1, os.path.join(".", "agent"))
sys.path.insert(1, os.path.join(".", "responce_model"))

from agent.requirment_graph import GraphState, RequirementGraph
from responce_model.requrementModel import CompleteRequirement


def print_separator():
    print("\n" + "=" * 80 + "\n")


def display_requirements(requirements: dict):
    """Display the current requirements in a readable format"""

    print_separator()
    print("📋 CURRENT REQUIREMENTS STATUS:")
    print_separator()

    # Project Metadata
    metadata = requirements.get("project_metadata", {})
    project_info = metadata.get("project_info", {})

    print(f"🎯 Project Name: {project_info.get('name', 'Not specified')}")
    print(f"📝 Description: {project_info.get('description', 'Not specified')}")
    print(
        f"💻 Programming Language: {metadata.get('programming_language', 'Not specified')}"
    )
    print(f"🗄️  Database: {metadata.get('database_type', 'Not specified')}")

    # Deployment
    deployment = metadata.get("deployment", {})
    print(f"\n🚀 Deployment:")
    print(f"   - Docker: {deployment.get('use_docker', 'Not specified')}")
    print(f"   - Deploy: {deployment.get('deploy_project', False)}")
    print(f"   - Terraform: {deployment.get('use_terraform', False)}")
    print(f"   - Cloud Provider: {deployment.get('cloud_provider', 'Not specified')}")

    # CI/CD
    cicd = metadata.get("cicd", {})
    print(f"\n🔄 CI/CD:")
    print(f"   - Enabled: {cicd.get('enable_cicd', False)}")
    print(f"   - Provider: {cicd.get('ci_cd_provider', 'Not specified')}")

    # Entities
    entities = requirements.get("entities", [])
    print(f"\n📦 Entities ({len(entities)}):")
    for entity in entities:
        print(
            f"   - {entity.get('name', 'Unknown')}: {entity.get('description', 'No description')}"
        )
        if entity.get("properties"):
            print(f"     Properties: {len(entity.get('properties', []))}")
        if entity.get("behaviors"):
            print(f"     Behaviors: {len(entity.get('behaviors', []))}")

    # Relationships
    relationships = requirements.get("relationships", [])
    print(f"\n🔗 Relationships ({len(relationships)}):")
    for rel in relationships:
        print(
            f"   - {rel.get('source', 'Unknown')} -> {rel.get('target', 'Unknown')}: {rel.get('description', 'No description')}"
        )

    print_separator()


def validate_complete_requirement(requirements: dict) -> bool:
    """Validate if requirements match the CompleteRequirement model"""
    try:
        CompleteRequirement(**requirements)
        return True
    except ValidationError as e:
        print(f"\n⚠️  Validation errors found:")
        for error in e.errors():
            print(f"   - {' -> '.join(str(x) for x in error['loc'])}: {error['msg']}")
        return False


def main():
    """Main function to run the requirement gathering system"""

    print("\n🤖 AI Requirement Gathering Agent")
    print("=" * 80)
    print("Welcome! I'll help you gather detailed requirements for your project.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type 'show' to display current requirements.")
    print("Type 'validate' to check if requirements are complete.")
    print("=" * 80)

    # Initialize the graph
    graph = RequirementGraph()
    state = None

    while True:
        user_input = input("\n👤 You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit"]:
            print("\n👋 Goodbye! Your requirements have been saved.")
            if state and state.get("current_requirements"):
                # Save to file
                with open("requirements_output.json", "w") as f:
                    json.dump(state["current_requirements"], f, indent=2)
                print("💾 Requirements saved to 'requirements_output.json'")
            break

        if user_input.lower() == "show":
            if state and state.get("current_requirements"):
                display_requirements(state["current_requirements"])
            else:
                print("No requirements gathered yet.")
            continue

        if user_input.lower() == "validate":
            if state and state.get("current_requirements"):
                if validate_complete_requirement(state["current_requirements"]):
                    print("\n✅ All requirements are valid and complete!")
                else:
                    print(
                        "\n❌ Requirements validation failed. Please provide missing information."
                    )
            else:
                print("No requirements to validate yet.")
            continue

        # Process user input
        try:
            result = graph.invoke(user_input, state)
            state = result

            # Get the last AI message
            ai_messages = [
                msg
                for msg in result["messages"]
                if hasattr(msg, "type") and msg.type == "ai"
            ]
            if ai_messages:
                last_message = ai_messages[-1].content
                print(f"\n🤖 Agent: {last_message}")

            # Check if complete
            if result.get("is_complete"):
                print("\n✅ Requirements gathering complete!")
                display_requirements(result["current_requirements"])

                # Validate the final requirements
                if validate_complete_requirement(result["current_requirements"]):
                    print("\n✅ All requirements are valid!")

                    # Save to file
                    with open("requirements_output.json", "w") as f:
                        json.dump(result["current_requirements"], f, indent=2)
                    print("💾 Requirements saved to 'requirements_output.json'")

                    cont = (
                        input("\nWould you like to make any changes? (yes/no): ")
                        .strip()
                        .lower()
                    )
                    if cont != "yes":
                        break
                    else:
                        # Reset completion flag to continue
                        state["is_complete"] = False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
