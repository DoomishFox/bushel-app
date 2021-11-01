from bushelapp.edit import leaf, root
from .models import Leaf

class LeafDetailsResult:
    def __init__(self, leaf_obj, branch_obj, root_obj, plaintext):
        self.id = leaf_obj.id
        self.uri = leaf_obj.uri
        self.name = leaf_obj.name
        self.date = leaf_obj.date
        self.branch_id = leaf_obj.parent_id
        self.branch_name = branch_obj.name
        self.branch_uri = branch_obj.uri
        self.root_id = root_obj.id
        self.root_uri = root_obj.uri
        self.plaintext = plaintext

    def serialize(self):
        return {
            "id": self.id,
            "uri": self.uri,
            "name": self.name,
            "date": self.date,
            "plaintext": self.plaintext,
            "branch": {
                "id": self.root_id,
                "name": self.branch_name,
                "uri": self.branch_uri,
                "root": {
                    "id": self.root_id,
                    "uri": self.root_uri
                }
            }
        }

class LeafResult:
    def __init__(self, leaf_obj):
        self.id = leaf_obj.id
        self.uri = leaf_obj.uri
        self.name = leaf_obj.name
        self.date = leaf_obj.date
        self.parent_id = leaf_obj.parent_id

    def serialize(self):
        return {
            "id": self.id,
            "uri": self.uri,
            "name": self.name,
            "date": self.date,
            "parent_id": self.parent_id,
        }

class LeafListResult:
    def __init__(self, leaf_list):
        self.leaf_list = leaf_list
    
    def serialize(self):
        leafresult_list = []
        for leaf in self.leaf_list:
            leafresult_list.append(LeafResult(leaf).serialize())
        return {
            "leaves": leafresult_list
        }