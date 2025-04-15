import datetime
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
import json


class SharePointService:
    def __init__(self, config: dict):
        self.config = config
        
    def connect(self):
        auth_ctx = AuthenticationContext(self.config["url"])
        auth_ctx.acquire_token_for_user(
            self.config["username"],
            self.config["password"]
        )
        return ClientContext(self.config["url"], auth_ctx)
    

    def get_metadata(self) -> str:
        """
        Return all metadata fields for files in a specific SharePoint library
        as a structured string suitable for LLM context (in JSON Lines format).
        """
        ctx = self.connect()
        lib = ctx.web.lists.get_by_title(self.config["library_name"])
        items = lib.items.get().execute_query()

        metadata_lines = []

        for item in items:
            file = item.file
            ctx.load(file)
            ctx.execute_query()

            # Safely convert all metadata to a regular dictionary (if not already)
            metadata_dict = dict(file.properties)

            # Optionally clean up nested objects or non-serializable data
            for key, value in metadata_dict.items():
                if hasattr(value, 'properties'):
                    metadata_dict[key] = dict(value.properties)
                elif isinstance(value, bytes):
                    metadata_dict[key] = str(value)
                elif isinstance(value, (int, float, str, list, dict, type(None))):
                    continue
                else:
                    metadata_dict[key] = str(value) 

            metadata_lines.append(json.dumps(metadata_dict, ensure_ascii=False))

        return "\n".join(metadata_lines)
