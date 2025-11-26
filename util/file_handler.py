import json
from pathlib import Path
from typing import Generator, Tuple
from util.cluster import Cluster
from util.game_data import GameData

class FileHandler:
    def __init__(self, notes: str, clusters: str):
        self.notes_path = Path(notes)
        self.clusters_path = Path(clusters)
        self.clusters_path.parent.mkdir(parents=True, exist_ok=True)
    
    def import_games(self) -> Generator[Tuple[GameData], None, None]:
        for file in self.notes_path.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            game = GameData.process_instance(raw_data)
            yield game

    def import_clusters(self) -> list:
        clusters_file = self.clusters_path 
        if clusters_file.exists() and clusters_file.stat().st_size > 0:
            with open(clusters_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            existing_clusters = Cluster.process_instance(raw_data)
            return existing_clusters
        return []
    
    def export_clusters(self, llm_clusters: list):
        data = self.import_clusters()
        existing_clusters = {c.cluster_id: c for c in data}

        # Merge clusters
        for cluster in llm_clusters:
            cid = cluster["cluster_id"]
            if cid in existing_clusters:
                # Append notes to existing cluster
                existing = existing_clusters[cid]
                existing.name = cluster.get("name", existing.name)
                existing.description = cluster.get("description", existing.description)
                existing.single_notes.extend(cluster.get("single_notes", []))
            else:
                # Create a new cluster entry
                new_cluster = Cluster(
                    cluster_id=cid,
                    name=cluster.get("name", ""),
                    description=cluster.get("description", ""),
                    single_notes=cluster.get("single_notes", [])
                )
                data.append(new_cluster)

        json_data = [c.to_dict() for c in data]
        with open(self.clusters_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)