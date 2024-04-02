from pprint import pprint

if __name__ == '__main__':
    test_dict: dict = {
        "cooking": "app",
        "developing": True,
        "product_manager": "iceeye7",
        "teams": {
            "frontend": {
                "number_of_members": 9,
                "scrums_masters": ["Ana Maria Ursache"]
            },
            "backend": {
                "number_of_members": 15,
                "scrums_masters": ["Chirvasa Matei", "Ezaru Tudor"]
            },
            "database": {
                "number_of_members": 5,
                "scrums_masters": ["Mitreanu Alexandru"]
            },
            "testing": {
                "number_of_members": 7,
                "scrums_masters": ["Ana Maria Ursache"]
            }
        }
    }

    pprint(test_dict)
