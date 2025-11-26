from typing import List, Optional
from dataclasses import dataclass, asdict

# Structures to hold individual notes for clustering
@dataclass
class SingleNote:
    app_id: str
    title: str
    content: str

    def to_dict(self):
        return {
            "app_id": self.app_id,
            "title": self.title,
            "content": self.content,
        }

# Structures to hold cluster data
@dataclass
class Cluster:
    cluster_id: str
    name: str
    description: str
    single_notes: List[SingleNote] 

    @classmethod
    def process_instance(cls, raw_data: dict):
        if raw_data == []:
            return []
        clusters = []
        for cluster in raw_data:
            notes = [
                SingleNote(
                    app_id=note.get("app_id"),
                    title=note.get("title"),
                    content=note.get("content"),
                )
                for note in cluster.get("single_notes", [])
            ]
            clusters.append(
                cls(
                    cluster_id=cluster.get("cluster_id"),
                    name=cluster.get("name"),
                    description=cluster.get("description"),
                    single_notes=notes
                )
            )
        return clusters

    @classmethod
    def get_list(cls, clusters):
        c = [
                {
                    "cluster_id": cluster.cluster_id,
                    "name": cluster.name,
                    "description": cluster.description,
                }
                for cluster in clusters
            ]
        return c
    
    def to_dict(self):
        return asdict(self)
    