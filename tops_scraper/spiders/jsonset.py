
import scrapy
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


import json
import os

def close(self, spider):
    file_path = "/tops_scraper/output.json"

    # Check if file is empty before reading
    if os.stat(file_path).st_size == 0:
        print("Error: output.json is empty.")
        return

    # Load the current JSON file safely
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON file - {e}")
        return

    # Create a new nested dictionary to organize data
    nested_data = {}

    for item in data:
        for main_category, details in item.items():
            # Ensure main category exists
            if main_category not in nested_data:
                nested_data[main_category] = {
                    "main_category_url": details["main_category_url"],
                    "subcategories": {}
                }

            for sub_category, sub_details in details["subcategories"].items():
                # Clean up subcategory names (remove newline characters)
                clean_sub_category = sub_category.replace("\n", " ").strip()

                # Ensure subcategory exists
                if clean_sub_category not in nested_data[main_category]["subcategories"]:
                    nested_data[main_category]["subcategories"][clean_sub_category] = {
                        "sub_category_url": sub_details["sub_category_url"],
                        "products": []
                    }

                # Append products without duplication
                nested_data[main_category]["subcategories"][clean_sub_category]["products"].extend(sub_details["products"])

    # Save the transformed data back to a JSON file
    output_path = "/tops_scraper/nested_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested_data, f, indent=4, ensure_ascii=False)

    print("JSON transformation complete! Data saved to nested_output.json.")


close()