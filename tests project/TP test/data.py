import sys

file = r"c:\Users\Administrateur\Documents\GitHub\Selenium_test\tests project\TP test\data_RDV.csv"

with open(file, mode='r', encoding="utf8") as f1:
    next(f1) # Skip the first line
    for idx, line in enumerate(f1):
        fields = line.strip().split(";")
        test_data = {}
        facility = {
            "Tokyo Cura": "//*[@id='combo_facility']/option[1]",
            "HongKong Cura": "//*[@id='combo_facility']/option[2]",
            "Seoul Cura": "//*[@id='combo_facility']/option[3]"
        }
        Hosp_Read = {
            "Not": "",
            "Yes": "//*[@id='chk_hospotal_readmission']"
        }
        Program = {
            "Medicaid": "radio_program_medicaid",
            "Medicare": "radio_program_medicare",
            "None": "radio_program_none"
        }
        Date = {
            "Past month": -1,
            "Next month": 1,
            "current Month": 0
        }
        Comment = {
            "Empty": "",
            "With": "Merci pour votre prise de rendez vous, a bientot"
        }
        test_data[fields[1]] = facility[fields[1]]
        test_data[fields[2]] = Hosp_Read[fields[2]]
        test_data[fields[3]] = Program[fields[3]]
        test_data[fields[4]] = Date[fields[4]]
        test_data[fields[5]] = Comment[fields[5]]
        print(idx, test_data)
        print("\n")
        

                
            