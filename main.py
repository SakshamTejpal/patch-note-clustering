
from util.file_handler import FileHandler 
from src.prepare_prompts import PreparePrompts 
from util.cluster import Cluster
from src.llm_call import call_gemini
from util.helper_funtions import HelperFunctions
import argparse


def main(notes_dir: str = "data/notes", clusters_dir: str = "data/clusters/taxonomy.json"):
    file = FileHandler(notes_dir, clusters_dir)
    batch_counter = 0

    # Process notes in batches
    for batch in HelperFunctions.generate_batches(file):
        print(f"Processing batch {batch_counter + 1}")
        batch_counter += 1
        
        clusters = Cluster.get_list(file.import_clusters()) #getting existing clusters
        preparer = PreparePrompts(notes=batch, clusters=clusters)
        if HelperFunctions.contains_injection(preparer.user_prompt()):
            raise ValueError("Prompt injection detected in user prompt.")
        user_prompt = preparer.user_prompt()
        system_prompt = preparer.system_prompt()

        # debugging
        # print(user_prompt)
        # print(system_prompt)

        response = call_gemini(system_prompt=system_prompt, user_prompt=user_prompt, batch=batch_counter)
        cleaned_response = HelperFunctions.extract_json(response) # Extract JSON from LLM response

        # Merge clusters and notes back to taxonomy file
        file.export_clusters(cleaned_response)
    
    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes_dir", default="data/notes")
    parser.add_argument("--clusters_dir", default="data/clusters/taxonomy.json")
    args = parser.parse_args()
    main(notes_dir=args.notes_dir, clusters_dir=args.clusters_dir)