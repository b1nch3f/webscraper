import os

import pandas as pd

data_dir = "data"
salary = {
    "company_name": [],
    "company_rating": [],
    "salary_min_lakhs": [],
    "salary_max_lakhs": [],
    "salary_frequency": [],
    "median_pay_lakhs": [],
    "job_title": [],
    "positions": [],
}

# iterate through all the text files in data directory
for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(data_dir, filename)
        print(f"Processing file: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            # read line by line, 9 lines at a time
            lines = file.readlines()
            for i in range(0, len(lines) - 3, 9):
                # extract the first 9 lines
                block = lines[i : i + 9]
                # the first lines is company name
                # the second line is company rating
                # the third line is salary range
                # the fort lines is salary frequency
                # ignore the fifth line
                # the sixth line is median pay
                # ignore the seventh line
                # the eight line is job title
                # the ninth lines has the number of positions extract the integer part, if not found, set to 0
                company_name = block[0].strip()
                # if company_name == "Tech Data":
                #     import pdb

                #     pdb.set_trace()
                company_rating = block[1].strip()
                salary_range = block[2].strip()

                salary_min = salary_range.split(" - ")[0]
                salary_min = salary_min.replace("₹", "")
                if "L" in salary_min:
                    salary_min = salary_min.replace("L", "")
                    salary_min = str(float(salary_min) * 100000)
                if "Cr" in salary_min:
                    salary_min = salary_min.replace("Cr", "")
                    salary_min = str(float(salary_min) * 10000000)
                if "K" in salary_min:
                    salary_min = salary_min.replace("K", "")
                    salary_min = str(float(salary_min) * 1000)

                salary_max = salary_range.split(" - ")[1]
                salary_max = salary_max.replace("₹", "")
                if "L" in salary_max:
                    salary_max = salary_max.replace("L", "")
                    salary_max = str(float(salary_max) * 100000)
                if "Cr" in salary_max:
                    salary_max = salary_max.replace("Cr", "")
                    salary_max = str(float(salary_max) * 10000000)
                if "K" in salary_max:
                    salary_max = salary_max.replace("K", "")
                    salary_max = str(float(salary_max) * 1000)

                salary_frequency = block[3].strip()

                median_pay = block[5].strip()
                median_pay = median_pay.replace("₹", "")
                if "L" in median_pay:
                    median_pay = median_pay.replace("L", "")
                    median_pay = str(float(median_pay) * 100000)
                if "Cr" in median_pay:
                    median_pay = median_pay.replace("Cr", "")
                    median_pay = str(float(median_pay) * 10000000)
                if "K" in median_pay:
                    median_pay = median_pay.replace("K", "")
                    median_pay = str(float(median_pay) * 1000)

                if salary_frequency == "/mo":
                    salary_min = str(float(salary_min) * 12)
                    salary_max = str(float(salary_max) * 12)
                    median_pay = str(float(median_pay) * 12)
                    salary_frequency = "/yr"
                elif salary_frequency == "/hr":
                    salary_min = str(float(salary_min) * 8 * 5 * 52)
                    salary_max = str(float(salary_max) * 8 * 5 * 52)
                    median_pay = str(float(median_pay) * 8 * 5 * 52)
                    salary_frequency = "/yr"

                job_title = block[7].strip()
                positions = block[8].strip()
                positions = "".join(filter(str.isdigit, positions))
                if positions == "":
                    positions = 0
                else:
                    positions = int(positions)

                salary["company_name"].append(company_name)
                salary["company_rating"].append(company_rating)
                salary["salary_min_lakhs"].append(salary_min)
                salary["salary_max_lakhs"].append(salary_max)
                salary["salary_frequency"].append(salary_frequency)
                salary["median_pay_lakhs"].append(median_pay)
                salary["job_title"].append(job_title)
                salary["positions"].append(positions)

# create a dataframe from the dictionary
df = pd.DataFrame(salary)
df.to_csv("salary.csv", index=False)
print(f"DataFrame saved to salary.csv")
