from treeBuilder import ContextTreeGenerator

if __name__ == "__main__":
    # Initialize the generator
    generator = ContextTreeGenerator()

    test_prompts = [
        "John is a software engineer who lives in New York. He can code in Python and is working on an AI project.",
        "The intelligent robot can navigate through complex environments and has advanced sensors. It communicates with humans using natural language.",
        "Maria owns a bakery in downtown Paris. She makes delicious croissants every morning and serves coffee to her customers."
    ]

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n=== Test Case {i} ===")
        print(f"Prompt: {prompt}")

        context_tree = generator.generate_context_tree(prompt)
        result = context_tree.to_dict()

        print(result)
