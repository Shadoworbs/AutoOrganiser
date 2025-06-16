# AutoOrganiser

A Python script to automatically organize files in a directory based on a set of rules defined in a configuration file. It helps keep your folders tidy by moving files into designated subdirectories according to their type or other custom criteria.

## Features

* **Rule-Based Sorting:** Organize files based on their extensions using a simple mapping.
* **Custom Rules:** Define more complex rules based on file names or other attributes.
* **Dry-Run Mode:** Test your configuration without actually moving any files to see what changes would be made.
* **Desktop Notifications:** Get notified about the script's operations.
* **Logging:** All file operations are logged to a file for review.
* **Custom Configuration:** Use a custom path for your configuration file.

## Installation

1. **Python 3:** Ensure you have Python 3 installed on your system.
2. **Dependencies:** Install the required dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

## Configuration (`config.json`)

The `config.json` file is the heart of the AutoOrganiser script. It defines how your files should be sorted.

Here is an example `config.json` with an explanation of each key:

```json
{
  "source_directory": "C:\\Users\\YourUser\\Downloads",
  "enable_notifications": true,
  "category_mappings": {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".rar", ".7z"]
  },
  "custom_rules": [
    {
      "folder": "Invoices",
      "keywords": ["invoice", "receipt"]
    },
    {
        "folder": "Screenshots",
        "keywords": ["screenshot"]
    }
  ]
}
```

* `source_directory`: The full path to the directory you want to organize.
* `enable_notifications`: Set to `true` to receive Windows desktop notifications, or `false` to disable them.
* `category_mappings`: A dictionary where keys are folder names (e.g., "Images") and values are lists of file extensions to be moved into that folder.
* `custom_rules`: A list of rules for more specific sorting. Each rule is an object with:
  * `folder`: The name of the destination folder.
  * `keywords`: A list of keywords. If any of these keywords are found in the filename, the file will be moved to the specified folder.

## Usage

### Basic Usage

To run the script with the default `config.json` in the same directory, simply execute:

```bash
python organizer.py
```

### Dry Run

To see which files would be moved without actually performing any file operations, use the `--dry-run` flag. This is highly recommended for testing new configurations.

```bash
python organizer.py --dry-run
```

### Custom Configuration File

You can specify a different configuration file using the `--config` argument.

```bash
python organizer.py --config C:\\path\\to\\your\\custom_config.json
```

## Scheduling with Windows Task Scheduler

To run the AutoOrganiser script automatically at regular intervals, you can use the Windows Task Scheduler.

1. **Open Task Scheduler:** Press `Win + R`, type `taskschd.msc`, and press Enter.
2. **Create a New Task:** In the right-hand Actions pane, click "Create Task...".
3. **General Tab:**
   * Give your task a **Name** (e.g., "AutoOrganiser Script").
   * Optionally, provide a **Description**.
   * Select "Run whether user is logged on or not" for it to run in the background.
4. **Triggers Tab:**
   * Click "New...".
   * Choose how often you want the script to run (e.g., "Daily").
   * Set a start time and click "OK".
5. **Actions Tab:**
   * Click "New...".
   * For **Action**, select "Start a program".
   * In the **Program/script** field, you need to provide the full path to your Python executable. You can find this by running `where python` in your command prompt.
   * In the **Add arguments (optional)** field, enter the full path to your `organizer.py` script. For example: `"C:\path\to\your\project\organizer.py"`.
   * In the **Start in (optional)** field, enter the directory where your `organizer.py` script is located. This is important so the script can find the `config.json` and `organizer.log` files correctly. For example: `"C:\path\to\your\project\"`.
6. **Conditions/Settings Tabs:**
   * You can configure additional settings, like only running when on AC power.
7. **Save the Task:** Click "OK". You may be prompted to enter your user password.

The script will now run automatically based on the schedule you defined.

## Logging

All actions performed by the script, including file movements and errors, are recorded in the `organizer.log` file, which is created in the same directory as the script. This log is useful for troubleshooting and tracking the script's activity.

## Contributing

If you would like to contribute to the AutoOrganiser project, feel free to fork the repository and submit a pull request. Contributions are welcome!
