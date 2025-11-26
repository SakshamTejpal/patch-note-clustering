from util.cluster import SingleNote, Cluster

class PreparePrompts:
    def __init__(self, notes: list[SingleNote], clusters: list[Cluster] = []):
        self.notes = notes
        self.clusters = clusters

    def user_prompt(self):
        prompt = f"""
        Following is the list of patch notes to be clustered:
        formated as a list of JSON objects as following:
        [{{"app_id": "<app_id>", "title": "<title>", "content": "<content>"}}]
        --------------------------------------------------------
        LIST OF PATCH NOTES:
        {self.notes}
        --------------------------------------------------------
        LIST OF EXISTING CLUSTERS (if any exists till now, could be empty):
        {self.clusters}
        """
        return prompt
    
    def system_prompt(self):
        prompt = """
            You are a data clustering expert. Your job is to cluster video game patch notes by diferent lables, based on the context of there content. 
            You must follow these rules:
            1. You need to assign a cluster to every patch note.
            2. Input comes in as a list of patch notes with existing cluster labels.Each note has an app_id, a title, content and an existing cluster_label (which may be "None")
            3. Input will also include existing list of clusters with names, ids and descriptions.You must reuse a cluster when a note matches the cluster.
            4. For each note:
            - Decide if it fits an existing cluster (exact semantic meaning match).
            - Or create a new cluster with a unique ID, description and name.
            - Justify all assignments implicitly through correct categorization.
            5. For new clusters:
            - Clusters cant be based on games, but the context of their content.
            - New cluster always needs to be relevant to the notes assigned.
            - Provide a very short and to the point human-readable name/label in 1-3 words.
            - Generate a unique ID: "C###" (incrementing).
            - Provide a clear description.
            6. Modifying existing cluster:
            - You can only modify an existing cluster, if you strogly believe a note can fit in with small modification rather than creating a new one.
            - When modifying, only change the lable name or description to better fit the new note.
            - Keep the cluster ID same when modifying.
            6. Output must ALWAYS be strictly valid JSON. Never include comments, markdown, extra text, or explanations. Dont wrap the output in any code blocks or markdowns.
            7. Output JSON structure MUST be:
            [
                {
                    "cluster_id": "<cluster_id>",
                    "name": "...",
                    "description": "...",
                    "single_notes": 
                    [
                        {
                        "app_id": "<app_id>",
                        "title": "<title>",
                        "content": "<content>"
                        }
                        ...
                    ]
                }
                ...
            ]
            You MUST follow these rules exactly. Your output MUST be only the JSON object.
        """
        return prompt