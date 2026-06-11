import os
import json
import gradio as gr
from PIL import Image

from modules import script_callbacks, shared, ui_extra_networks
from modules.ui_extra_networks import quote_js
from modules.ui_extra_networks_user_metadata import UserMetadataEditor

prompts_dir = os.path.join(shared.data_path, "models", "saved_prompts")
os.makedirs(prompts_dir, exist_ok=True)

class PromptSaveUserMetadataEditor(UserMetadataEditor):
    def __init__(self, ui, tabname, page):
        super().__init__(ui, tabname, page)

    def save_prompt_user_metadata(self, name, desc, prompt, negative_prompt, notes):
        user_metadata = self.get_user_metadata(name)
        user_metadata["description"] = desc
        user_metadata["prompt"] = prompt
        user_metadata["negative_prompt"] = negative_prompt
        user_metadata["notes"] = notes

        self.write_user_metadata(name, user_metadata)

    def put_values_into_components(self, name):
        user_metadata = self.get_user_metadata(name)
        values = super().put_values_into_components(name)

        return [
            *values,
            user_metadata.get("prompt", ""),
            user_metadata.get("negative_prompt", "")
        ]

    def create_editor(self):
        self.create_default_editor_elems()

        self.edit_prompt = gr.TextArea(label="Positive Prompt", lines=4)
        self.edit_negative_prompt = gr.TextArea(label="Negative Prompt", lines=4)
        self.edit_notes = gr.TextArea(label="Notes", lines=4)

        self.create_default_buttons()

        viewed_components = [
            self.edit_name,
            self.edit_description,
            self.html_filedata,
            self.html_preview,
            self.edit_notes,
            self.edit_prompt,
            self.edit_negative_prompt,
        ]

        self.button_edit.click(
            fn=self.put_values_into_components, 
            inputs=[self.edit_name_input], 
            outputs=viewed_components
        ).then(
            fn=lambda: gr.update(visible=True), 
            inputs=[], 
            outputs=[self.box]
        )

        edited_components = [
            self.edit_description,
            self.edit_prompt,
            self.edit_negative_prompt,
            self.edit_notes,
        ]

        self.setup_save_handler(self.button_save, self.save_prompt_user_metadata, edited_components)

    def create_ui(self):
        super().create_ui()

        self.btn_open_add_prompt = gr.Button(visible=False, elem_id=f"{self.tabname}_{self.page.extra_networks_tabname}_add_prompt_btn")

        with gr.Group(visible=False, elem_id=f"{self.tabname}_{self.page.extra_networks_tabname}_add_prompt_modal", elem_classes="edit-user-metadata") as add_box:
            self.add_box = add_box
            gr.HTML("<h2>Save New Prompt</h2>")
            self.add_name = gr.Textbox(label="Name", placeholder="Name of the prompt")
            self.add_prompt = gr.TextArea(label="Positive Prompt", lines=4)
            self.add_negative_prompt = gr.TextArea(label="Negative Prompt", lines=4)
            self.add_description = gr.TextArea(label="Description", lines=2)
            self.add_image = gr.Image(label="Preview Image", type="pil", interactive=True)

            with gr.Row():
                self.add_cancel = gr.Button("Cancel", elem_id=f"{self.tabname}_{self.page.extra_networks_tabname}_add_cancel_btn")
                self.add_save = gr.Button("Save Prompt", variant="primary")
            self.add_status = gr.HTML()

        self.btn_open_add_prompt.click(
            fn=lambda: gr.update(visible=True),
            outputs=[self.add_box]
        )
        
        self.add_cancel.click(
            fn=lambda: gr.update(visible=False),
            outputs=[self.add_box]
        ).then(
            fn=None,
            _js="closePopup"
        )
        
        self.add_save.click(
            fn=save_prompt,
            inputs=[self.add_name, self.add_prompt, self.add_negative_prompt, self.add_description, self.add_image],
            outputs=[self.add_status]
        ).then(
            fn=lambda: gr.update(visible=False),
            outputs=[self.add_box]
        ).then(
            fn=None,
            _js=f"function(){{ closePopup(); document.getElementById('{self.tabname}_{self.page.extra_networks_tabname}_extra_refresh_internal').click(); }}"
        )

class ExtraNetworksPagePromptSave(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__("Prompts")
        self.allow_negative_prompt = True

    def refresh(self):
        pass

    def create_html(self, tabname, *, empty=False):
        html = super().create_html(tabname, empty=empty)
        
        add_btn = f'''
        <div id="{tabname}_{self.extra_networks_tabname}_extra_add" class="extra-network-control--refresh"
            style="display: flex; justify-content: center; align-items: center;"
            title="Add new prompt"
            onclick="popupId('{tabname}_{self.extra_networks_tabname}_add_prompt_modal'); document.getElementById('{tabname}_{self.extra_networks_tabname}_add_prompt_btn').click();">
            <span style="font-size: 24px; font-weight: bold; line-height: 14px; margin-top: -2px;">+</span>
        </div>
        '''
        
        html = html.replace(
            f'<div id="{tabname}_{self.extra_networks_tabname}_extra_refresh"',
            add_btn + f'\n        <div id="{tabname}_{self.extra_networks_tabname}_extra_refresh"'
        )
        return html

    def list_items(self):
        if not os.path.isdir(prompts_dir):
            return

        index = 0
        for filename in os.listdir(prompts_dir):
            if filename.endswith(".json"):
                item = self.create_item(filename, index)
                if item is not None:
                    yield item
                index += 1

    def create_item(self, filename, index=None, enable_filter=True):
        file_path = os.path.join(prompts_dir, filename)
        if not os.path.isfile(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

        name = data.get("name", os.path.splitext(filename)[0])
        path = os.path.splitext(file_path)[0]

        item = {
            "name": name,
            "filename": file_path,
            "preview": self.find_preview(path),
            "description": data.get("description", ""),
            "search_terms": [name, self.search_terms_from_path(file_path)],
            "local_preview": f"{path}.png",
            "prompt": quote_js(data.get("prompt", "")),
            "negative_prompt": quote_js(data.get("negative_prompt", "")),
            "sort_keys": {"default": index, **self.get_sort_keys(file_path)},
        }

        self.read_user_metadata(item)
        return item

    def allowed_directories_for_previews(self):
        return [prompts_dir]

    def create_user_metadata_editor(self, ui, tabname):
        return PromptSaveUserMetadataEditor(ui, tabname, self)

def save_prompt(name, prompt, negative_prompt, description, image):
    if not name:
        return "<div style='color:red;'>Please provide a name for the prompt.</div>"
    
    # Sanitize the name for the file system
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()
    if not safe_name:
        safe_name = "unnamed_prompt"
    
    file_path = os.path.join(prompts_dir, f"{safe_name}.json")
    
    data = {
        "name": name,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "description": description
    }
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        if image is not None:
            image_path = os.path.join(prompts_dir, f"{safe_name}.png")
            image.save(image_path)
            
        return f"<div style='color:green;'>Successfully saved prompt as {safe_name}</div>"
    except Exception as e:
        return f"<div style='color:red;'>Failed to save prompt: {str(e)}</div>"

def on_before_ui():
    ui_extra_networks.register_page(ExtraNetworksPagePromptSave())

script_callbacks.on_before_ui(on_before_ui)
