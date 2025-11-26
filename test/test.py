import json
from pathlib import Path

NOTES_DIR = Path("data/notes")
CLUSTERS_PATH = Path("data/clusters/taxonomy.json")

def validate_notes_present():

    taxonomy_file = CLUSTERS_PATH
    notes_path = NOTES_DIR

    taxonomy = json.loads(taxonomy_file.read_text(encoding="utf-8"))

    taxonomy_titles = set()
    for cluster in taxonomy:
        for note in cluster.get("single_notes", []):
            taxonomy_titles.add(note.get("title", "").strip())

    input_titles = set()
    for note_file in notes_path.glob("*.json"):
        data = json.loads(note_file.read_text(encoding="utf-8"))
        for note in data.get("patch_notes", []):
            title = note.get("title", "").strip()
            if title:
                input_titles.add(title)

    missing = list(input_titles - taxonomy_titles)

    if missing:
        return False, "Failed : missing notes: " + ", ".join(missing)

    return True, "OK"


def validate_taxonomy():
    taxonomy_file = CLUSTERS_PATH

    try:
        taxonomy = json.loads(taxonomy_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False, "Failed : taxonomy is not valid JSON"

    if not isinstance(taxonomy, list):
        return False, "Failed : taxonomy must be a LIST of clusters"

    if len(taxonomy) == 0:
        return False, "Failed : taxonomy has no clusters"

    for idx, cluster in enumerate(taxonomy):

        required_cluster_fields = ["cluster_id", "name", "description", "single_notes"]
        for key in required_cluster_fields:
            if key not in cluster:
                return False, f"Failed : Cluster #{idx} missing field '{key}'"

        if len(cluster["single_notes"]) == 0:
            return False, f"Failed : Cluster #{idx} has no notes"

        for n_idx, note in enumerate(cluster["single_notes"]):
            required_note_fields = ["app_id", "title", "content"]
            for key in required_note_fields:
                if key not in note:
                    return False, (
                        f"Failed : Cluster #{idx}, Note #{n_idx} missing note field '{key}'"
                    )

    return True, "OK"


def run_eval():
    print("OFFLINE EVALUATION STARTING...")

    print("==============================")
    print("Validating if all the notes are present...")
    ok2, msg = validate_notes_present()
    print(msg)

    print("==============================")
    print("Validating taxonomy structure...")
    ok3, msg = validate_taxonomy()
    print(msg)

    if ok2 and ok3:
        print("ALL TESTS PASSED!")


if __name__ == "__main__":
    run_eval()
