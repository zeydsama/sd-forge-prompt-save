# SD Forge Prompt Save Extension

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-supported-orange.svg)

**SD Forge Prompt Save** is a seamless extension for [sd-webui-forge-neo](https://github.com/Haoming02/sd-webui-forge-classic) (and compatible WebUI forks) that natively integrates a prompt-saving mechanism into the Extra Networks tab. 

Tired of juggling text files or relying on external tools to store your best prompt formulas? This extension lets you save, preview, and apply your prompts with the exact same workflow used for Loras and Checkpoints.

---

## 🌟 Features

- **Native Extra Networks Integration**: Adds a brand-new **Prompts** tab directly to the Extra Networks pane.
- **Visual Prompt Cards**: Assign cover images to your prompts, creating an elegant visual gallery of your favorite styles and concepts.
- **One-Click Application**: Click any prompt card to instantly append its positive and negative formulas directly to your generation textboxes.
- **In-App Editing**: Hover over any saved prompt card and click the **Edit (Pencil)** icon to bring up a metadata editor overlay. Easily tweak positive/negative texts, add notes, or replace cover images without leaving the WebUI.
- **Integrated Add Prompt UI**: Click the **"+" button** inside the Extra Networks Prompts tab to quickly save a new prompt, assign a cover image, and set its name—all without leaving your workflow.

## 📦 Installation

1. Navigate to the `extensions` directory in your WebUI folder:
   ```bash
   cd extensions
   ```
2. Clone this repository (or copy the extension folder if downloading manually):
   ```bash
   git clone https://github.com/zeydsama/sd-forge-prompt-save.git
   ```
3. Restart the WebUI completely, or click **Reload UI** from the settings.

## 🚀 Usage

### Saving a New Prompt

1. Open the **Extra Networks** pane (the icon under the "Generate" button).
2. Click on the **Prompts** tab.
3. Click the **"+" (Add) button** located right next to the refresh button.
4. A popup will appear. Fill out the **Name**, **Positive Prompt**, **Negative Prompt**, **Description**, and upload a **Preview Image**.
5. Click **Save Prompt**. The popup will close and the tab will automatically refresh to show your new prompt card!

### Applying a Saved Prompt

1. Below the "Generate" button, open the **Extra Networks** pane.
2. Click on the **Prompts** tab. (If you don't see your newly saved prompt, click the **Refresh** button).
3. Click on the visual card of your saved prompt.
4. The positive and negative prompt data will be seamlessly appended to your current generation setup!

### Editing an Existing Prompt

1. Open the **Prompts** tab within Extra Networks.
2. Hover your mouse over the prompt you wish to edit and click the **Pencil icon** (Edit metadata).
3. An overlay will appear. Here, you can edit the **Description**, **Notes**, **Positive Prompt**, and **Negative Prompt**.
4. Click **Save**. Your changes are instantly written to the underlying configuration file.

## 📂 File Structure

Saved prompts are cleanly stored in `models/saved_prompts/` inside your WebUI data path. 
- `<prompt_name>.json`: Contains the prompt metadata (positive, negative, description, notes).
- `<prompt_name>.png`: The cover image used for the Extra Networks card.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
