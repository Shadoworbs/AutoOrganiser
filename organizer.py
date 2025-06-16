import json
import logging
import argparse
import pathlib
import shutil
from datetime import datetime

# Attempt to import plyer, handle if not installed
try:
    from plyer import notification
    plyer_available = True
except ImportError:
    plyer_available = False

LOG_FILE = 'organizer.log'

def setup_logging():
    """Configures the logging module to write to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def load_config(config_path):
    """Loads and validates the configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Basic validation
        if "source_directory" not in config or "category_mappings" not in config:
            logging.error("Configuration file is missing required keys ('source_directory', 'category_mappings').")
            return None
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found at: {config_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file: {config_path}")
        return None

def handle_collision(destination_path, file_path):
    """Handles file name collisions by appending a numeric suffix."""
    base, extension = file_path.stem, file_path.suffix
    counter = 1
    while True:
        new_filename = f"{base} ({counter}){extension}"
        new_path = destination_path / new_filename
        if not new_path.exists():
            return new_path
        counter += 1

def main():
    """Main function to run the file organization script."""
    parser = argparse.ArgumentParser(description="Automate file organization.")
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate the process without moving files."
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help="Path to the configuration file (default: config.json)."
    )
    args = parser.parse_args()

    setup_logging()

    config = load_config(args.config)
    if not config:
        return

    source_dir_path = pathlib.Path(config['source_directory'])
    if not source_dir_path.exists() or not source_dir_path.is_dir():
        logging.error(f"Source directory '{source_dir_path}' does not exist or is not a directory.")
        return
        
    category_mappings = config.get('category_mappings', {})
    custom_rules = config.get('custom_rules', [])
    enable_notifications: bool = config.get('enable_notifications', False)

    moved_files_count = 0
    
    logging.info(f"Starting file organization in '{source_dir_path}'. Dry run: {args.dry_run}")

    for file_path in source_dir_path.iterdir():
        if file_path.is_file():
            destination_folder_name = None
            
            # 1. Check custom rules by keyword
            for rule in custom_rules:
                if rule['keyword'].lower() in file_path.name.lower():
                    destination_folder_name = rule['destination']
                    logging.info(f"Matched custom rule for '{file_path.name}' with keyword '{rule['keyword']}'.")
                    break
            
            # 2. If no custom rule, check by extension
            if not destination_folder_name:
                file_extension = file_path.suffix.lower()
                if file_extension: # Ensure there is an extension
                    for category, extensions in category_mappings.items():
                        if file_extension in extensions:
                            destination_folder_name = category
                            break

            # 3. Process the file if a destination was found
            if destination_folder_name:
                destination_path = source_dir_path / destination_folder_name
                
                try:
                    if not destination_path.exists():
                        if not args.dry_run:
                            destination_path.mkdir(parents=True)
                        logging.info(f"{'DRY RUN: ' if args.dry_run else ''}Created directory: '{destination_path}'")

                    final_destination = destination_path / file_path.name
                    
                    if final_destination.exists():
                        final_destination = handle_collision(destination_path, file_path)
                        logging.warning(f"Name collision for '{file_path.name}'. Will move to '{final_destination.name}'.")

                    if not args.dry_run:
                        shutil.move(str(file_path), str(final_destination))
                    
                    logging.info(f"{'DRY RUN: ' if args.dry_run else ''}Moved '{file_path.name}' to '{destination_folder_name}'")
                    moved_files_count += 1

                except PermissionError:
                    logging.error(f"Permission denied: Could not move '{file_path.name}'.")
                except IOError as e:
                    logging.error(f"IOError moving '{file_path.name}': {e}")
            else:
                logging.info(f"No rule found for '{file_path.name}'. Skipping.")

    summary_message = f"File organization complete. {'(DRY RUN) ' if args.dry_run else ''}Moved {moved_files_count if not args.dry_run else 0} files."
    logging.info(summary_message)

    if enable_notifications :#and not args.dry_run:
        if plyer_available:
            logging.info("Sending notification...")
            try:
                notification.notify(
                    title="AutoOrganiser",
                    message=summary_message,
                    app_name="AutoOrganiser",
                    app_icon="Assets/icon.ico"
                )
            except Exception as e:
                logging.error(f"Failed to send notification: {e}")
        else:
            logging.warning("plyer is not installed. Skipping notification.")


if __name__ == "__main__":
    main()