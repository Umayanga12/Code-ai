"""
Main AI Agent Pipeline
Complete workflow: Requirement → User Approval → Planner → Architecture → Builder
"""

import json
import os
from datetime import datetime

from langchain.messages import HumanMessage

from agent.requirment.requirment_system_graph import (
    requirment_system_graph,
    RequirementSystemState,
)
from agent.planner.system_generation_graph import (
    SystemGenerationState,
    system_generation_graph,
)

init_prompt = """
Create a simple Point of Sale (POS) system with the following features:

### User Accounts
- **Users**: username, password, user_type (admin, regular)
- **Admin**: Can manage everything in the system
- **Regular User**: Can only process sales and view products

### Supplier Management
- **Supplier Details**: name, email, address, contact_number
- **Operations**: Add, edit, view, and remove suppliers

### Product Categories
- **Category Details**: category_name, category_code
- **Operations**: Create, modify, and delete categories

### Product Catalog
- **Product Details**: item_name, item_code, price, stock_quantity
- **Relationships**: Link products to suppliers and categories
- **Operations**: Add new products, update prices, manage inventory

### Sales Processing
- **Shopping Cart**: Add products, change quantities, remove items
- **Checkout System**:
  - Calculate totals (subtotal, tax, final amount)
  - Accept different payment methods
  - Print receipts
  - Automatically reduce stock levels
- **Sales History**: View all past transactions

### Inventory Tracking
- **Stock Monitoring**: See current stock levels
- **Low Stock Alerts**: Get warnings when products are running low
- **Automatic Updates**: Stock decreases when items are sold

### Basic Reports
- **Sales Reports**: View sales by day, week, or month
- **Popular Items**: See best-selling products
- **Stock Reports**: Check inventory status

### System Requirements
- Secure login system
- Easy product search during sales
- Simple and clean interface
- Data validation for all inputs
- Reliable data storage

Focus on creating a system that is easy to use for daily sales operations while allowing administrators to manage products, suppliers, and categories efficiently.
"""


def print_separator(title=""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
    else:
        print("=" * 60)


def get_user_approval(requirements_data):
    """
    Display requirements to user and ask for approval.
    
    Args:
        requirements_data: The requirements dictionary from requirement agent
        
    Returns:
        bool: True if user approves, False otherwise
    """
    print_separator("REQUIREMENTS SUMMARY")
    
    try:
        requirements = requirements_data.get("requirements", {})
        
        # Display project info
        project_info = requirements.get("project_metadata", {}).get("project_info", {})
        print(f"\nProject Name: {project_info.get('name', 'N/A')}")
        print(f"Description: {project_info.get('description', 'N/A')}")
        print(f"Type: {project_info.get('type', 'N/A')}")
        
        # Display entities
        entities = requirements.get("entities", [])
        print(f"\n\nEntities ({len(entities)}):")
        for entity in entities:
            print(f"  - {entity.get('name', 'N/A')}: {entity.get('description', 'N/A')}")
        
        # Display user types
        sys_users = requirements.get("sys_user", [])
        print(f"\n\nUser Types ({len(sys_users)}):")
        for user in sys_users:
            user_types = user.get("user_types", [])
            for user_type in user_types:
                print(f"  - {user_type.get('role', 'N/A')}: {user_type.get('access_level', 'N/A')}")
        
        # Display tech stack
        tech_stack = requirements.get("project_metadata", {}).get("programming_language", {})
        print(f"\n\nTech Stack:")
        print(f"  Frontend: {tech_stack.get('for_frontend', 'N/A')}")
        print(f"  Backend: {tech_stack.get('for_backend', 'N/A')}")
        
        print_separator()
        
    except Exception as e:
        print(f"\nError displaying requirements: {str(e)}")
        print("\nRaw requirements data:")
        print(json.dumps(requirements_data, indent=2))
    
    # Ask for user approval
    while True:
        response = input("\n\nDo you approve these requirements? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            print("\nRequirements not approved. Exiting...")
            return False
        else:
            print("Please answer 'yes' or 'no'")


def main():
    """Main execution function."""
    print_separator("AI AGENT PIPELINE")
    print("Complete workflow: Requirement → Planner → Architecture → Builder")
    print_separator()
    
    # Get initial user input
   # user_input = input("\nDescribe your project: ").strip()
    
    # if not user_input:
    #     print("No input provided. Exiting...")
    #     return
    
    config = {"configurable": {"thread_id": f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"}}
    
    # ====================
    # STEP 1: Requirement Gathering
    # ====================
    print_separator("STEP 1: REQUIREMENT GATHERING")
    
    initial_state = RequirementSystemState(
        messages=[init_prompt],#[HumanMessage(content=user_input)],
        requirements=None,
        itinerary=None,
    )
    
    try:
        requirement_result = requirment_system_graph.invoke(initial_state, config)
        print(requirement_result)
        print("\n✓ Requirements gathered successfully")
    except Exception as e:
        print(f"\n✗ Error gathering requirements: {str(e)}")
        return
    
    # ====================
    # USER APPROVAL CHECK
    # ====================
    if not get_user_approval(requirement_result):
        return
    
    print("\n✓ Requirements approved by user")
    
    # ====================
    # STEP 2: System Planning
    # ====================
    print_separator("STEP 2: SYSTEM PLANNING")
    
    planner_state = SystemGenerationState(
        requirments=requirement_result
    )
    
    try:
        planner_result = system_generation_graph.invoke(planner_state, config)
        print("\n✓ System plan generated successfully")
        print(planner_result)
        
        # Display brief summary
        final_output = planner_result.get("final_output", {})
        plan = final_output.get("plan", {})
        print(f"\nProject Complexity: {plan.get('system_complexity', 'N/A')}")
        print(f"User Scale: {plan.get('user_scale', 'N/A')}")
        
    except Exception as e:
        print(f"\n✗ Error generating system plan: {str(e)}")
        return
    
    # ====================
    # STEP 3: Code Generation
    # ====================
    print_separator("STEP 3: CODE GENERATION")
    
    # Extract necessary data
    # requirements_data = requirement_result.get("requirements", {})
    # final_output = planner_result.get("final_output", {})
    # plan_data = final_output.get("plan", {})
    # architecture_data = final_output.get("architecture", {})
    
    # # Determine project name
    # project_metadata = requirements_data.get("project_metadata", {})
    # project_info = project_metadata.get("project_info", {})
    # project_name = project_info.get("name", "generated_project").lower().replace(" ", "_")
    
    # # Create output directory
    # output_dir = os.path.join(os.getcwd(), "generated_projects")
    # os.makedirs(output_dir, exist_ok=True)
    
    # builder_state = BuilderGraphState(
    #     messages=[],
    #     architecture=architecture_data,
    #     planner_output=plan_data,
    #     requirements=requirements_data,
    #     project_name=project_name,
    #     output_directory=output_dir,
    #     project_structure=None,
    #     generated_files=[],
    #     tasks_completed=[],
    #     current_step="initial",
    #     build_status="pending",
    #     errors=[],
    # )
    
    # try:
    #     builder_result = builder_graph.invoke(builder_state, config)
        
    #     build_status = builder_result.get("build_status", "unknown")
    #     generated_files = builder_result.get("generated_files", [])
        
    #     print_separator("BUILD COMPLETE")
    #     print(f"\nBuild Status: {build_status}")
    #     print(f"Files Generated: {len(generated_files)}")
    #     print(f"\nProject Location: {os.path.join(output_dir, project_name)}")
        
    #     print("\n\nNext Steps:")
    #     print(f"  1. cd {os.path.join(output_dir, project_name)}")
    #     print("  2. pip install -r requirements.txt")
    #     print("  3. python main.py")
    #     print("  4. Visit http://localhost:8000/docs for API documentation")
        
    #     print_separator()
        
    # except Exception as e:
    #     print(f"\n✗ Error during code generation: {str(e)}")
    #     import traceback
    #     traceback.print_exc()
    #     return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()