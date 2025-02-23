# Web Scraping Assignment - Tops Online

## Approach Used for Scraping

1.**Data Fetching Approach:**
   - I followed an approach using Scrapy by first fetching all the main category links, then fetching all the subcategory links, and then fetching the product links. In the end, I scraped and parsed the product data all done asynchronously via Scrapy.
   
5. **Data Processing and Formatting:**
   - Scrapy's built-in functionality is used to generate structured JSON.
   - A separate script was created to format the JSON data in a hierarchical structure.

6. **Error Handling & Reliability Measures:**
   - Implemented proper error handling.
   - Added retry logic to resend failed requests in case of server issues.

---

## Dependencies Required

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## How to Run the Script

1. **Clone the Repository:**
   ```bash
   git clone "https://github.com/Hammad-1/tops_crawler"
   cd tops_scraper/spiders/
   ```

2. **Run the Scrapy Spider:**
   ```bash
   scrapy crawl tops_spider
   ```
   - This will fetch the product data and save it in `output.json`.
   
3. **Format JSON Data (Optional):**
   ```bash
   python format_json.py
   ```
   - This script organizes data into a structured hierarchy.

4. **Review the Output:**
   - The final dataset is stored in JSON format and is ready for submission.

---

## Challenges Faced and Solutions

1. **Concurrency Issue With Scrapy:**
    - I was writing json file for every record i fetched to maintain hirerchy in json data, but the issue was data is misssing due to concurrent request to fix that issue i used Scrapy builtin json feature and created json file and to fix the hirarchy issue i created another script to convert raw json into formated json   

2. **Server Failures & Request Timeouts:**
   - Implemented retry logic with exponential backoff to handle network issues.

3. **Data Inconsistency:**
   - Some products had missing barcodes or images.
   - Solution: Skipped products missing critical data or flagged incomplete entries.

---

## Sample Output (First 5 Products)
[
{
    "Snacks And Desserts": {
        "subcategories": {
            "Chips\n354": {
                "products": [
                    {
                        "product_url": "https://www.tops.co.th/en/lays-classic-potato-salt-69g-8850718801213",
                        "name": "Lays Classic Potato Salt 69g.",
                        "images": [
                            "https://assets.tops.co.th/LAYS-LaysClassicPotatoSalt69g-8850718801213-1?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysClassicPotatoSalt69g-8850718801213-2?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysClassicPotatoSalt69g-8850718801213-3?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysClassicPotatoSalt69g-8850718801213-4?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysClassicPotatoSalt69g-8850718801213-5?$JPEG$"
                        ],
                        "quantity": "69g.",
                        "barcode": "8850718801213",
                        "details": "Properties\n:\nLay's Classic Potato Chips are now available in a newly designed packaging. This gluten-free product retails in a 75g pack featuring the Facebook, YouTube, Twitter and Instagram logos.\nThe product received may be subject to package modification and quantity from the manufacturer.\nWe reserve the right to make any changes without prior notice.\n*The images used are for advertising purposes only.\nIngredients\n:\npotato, palm vegetable oil, soybean vegetable oil, salt\nUsage\n:\nonce opened consume immediately",
                        "price": "31.00",
                        "labels": ""
                    }
                ]
            }
        }
    }
},
{
    "Snacks And Desserts": {
        "subcategories": {
            "Chocolate\n321": {
                "products": [
                    {
                        "product_url": "https://www.tops.co.th/en/mm-milk-chocolate-90g-9300682001304",
                        "name": "M&M Milk Chocolate 90g.",
                        "images": [
                            "https://assets.tops.co.th/MM-MMMilkChocolate90g-9300682001304-1",
                            "https://assets.tops.co.th/MM-MMMilkChocolate90g-9300682001304-2"
                        ],
                        "quantity": "90g.",
                        "barcode": "9300682001304",
                        "details": "Properties\n:\nThe product received may be subject to package modification and quantity from the manufacturer. We reserve the right to make any changes without prior notice. *The images used are for advertising purposes only.",
                        "price": "62.00",
                        "labels": "Product of Australia"
                    }
                ]
            }
        }
    }
},
{
    "Snacks And Desserts": {
        "subcategories": {
            "Chips\n354": {
                "products": [
                    {
                        "product_url": "https://www.tops.co.th/en/mantra-plant-based-prawn-crackers-original-flavor-25g-8859360701209",
                        "name": "Mantra Plant Based Prawn Crackers Original Flavor 25g",
                        "images": [
                            "https://assets.tops.co.th/TONGTIN-TongtinMantraPlantBasedPrawnCrackersOriginalFlavor25g-8859360701209-1?$JPEG$",
                            "https://assets.tops.co.th/TONGTIN-TongtinMantraPlantBasedPrawnCrackersOriginalFlavor25g-8859360701209-2?$JPEG$",
                            "https://assets.tops.co.th/TONGTIN-TongtinMantraPlantBasedPrawnCrackersOriginalFlavor25g-8859360701209-3?$JPEG$",
                            "https://assets.tops.co.th/TONGTIN-TongtinMantraPlantBasedPrawnCrackersOriginalFlavor25g-8859360701209-4?$JPEG$"
                        ],
                        "quantity": "25g",
                        "barcode": "8859360701209",
                        "details": "",
                        "price": "69.00",
                        "labels": ""
                    }
                ]
            }
        }
    }
},
{
    "Snacks And Desserts": {
        "subcategories": {
            "Biscuits Cookies & Crackers\n499": {
                "products": [
                    {
                        "product_url": "https://www.tops.co.th/en/glico-pretz-original-flavour-21g-8851019030975",
                        "name": "Glico Pretz Original Flavour 21g.",
                        "images": [
                            "https://assets.tops.co.th/GLICO-GlicoPretzOriginalFlavour21g-8851019030975-1?$JPEG$"
                        ],
                        "quantity": "21g.",
                        "barcode": "8851019030975",
                        "details": "",
                        "price": "10.00",
                        "labels": "Halal"
                    }
                ]
            }
        }
    }
},
{
    "Snacks And Desserts": {
        "subcategories": {
            "Chips\n354": {
                "products": [
                    {
                        "product_url": "https://www.tops.co.th/en/lays-rock-potato-salt-69g-8850718801121",
                        "name": "Lays Rock Potato Salt 69g.",
                        "images": [
                            "https://assets.tops.co.th/LAYS-LaysRockPotatoSalt69g-8850718801121-1?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysRockPotatoSalt69g-8850718801121-2?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysRockPotatoSalt69g-8850718801121-3?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysRockPotatoSalt69g-8850718801121-4?$JPEG$",
                            "https://assets.tops.co.th/LAYS-LaysRockPotatoSalt69g-8850718801121-5?$JPEG$"
                        ],
                        "quantity": "69g.",
                        "barcode": "8850718801121",
                        "details": "Properties\n:\nLay's Rock has released Salted Ridged Cut Potato Chips. The product is available in a 75g pack.\nThe product received may be subject to package modification and quantity from the manufacturer.\nWe reserve the right to make any changes without prior notice.\n*The images used are for advertising purposes only.\nIngredients\n:\nPotato 63.7%, vegetable oil 30%, seasoning 6.3%\nUsage\n:\nonce opened consume immediately",
                        "price": "31.00",
                        "labels": ""
                    }
                ]
            }
        }
    }
}
]