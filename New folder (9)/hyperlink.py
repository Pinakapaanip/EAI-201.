from browser_use_sdk import BrowserUseSdk

PEOPLE = [
    {
        "name": "PINAKAPAANI P",
        "location": "Bengaluru, India",
        "interested_in": "higher education and universities",
    },
]

api_key = "bu_OB1i0Pz4-YDW5RfPJZmkXMsABFMj9AnObTUkmxWrQO0"

sdk = BrowserUseSdk(api_key=api_key)

for person in PEOPLE:
    result = sdk.run(
        llm_model="o3",
        task="""
Go to wikipedia.com and search for "Chanakya University".
Navigate to the main article on Chanakya University.
From there, find and visit the official website of Chanakya University.
On the official website, search for "course fees" or "tuition fees".
Extract and provide the information about course fees.
At the end, provide the URLs for each of these pages.
"""
    )
    print(result)

    print("Links:")
    print("Chanakya University Wikipedia:", "https://en.wikipedia.org/wiki/Chanakya_University")
