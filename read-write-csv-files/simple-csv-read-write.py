# Import the csv module
import csv

def simpleReader():
    # Open the file with 'read' mode
    with open("tea-info.csv", "r") as infile:
        # Read the file with .reader()
        content = csv.reader(infile, delimiter=',')

        # Iterate through each row
        for row in content:
            print(row)

def dictionaryReader():
    # Open the file with 'read' mode
    with open("tea-info.csv", "r") as infile:
        # Read the file with .DictReader()
        content = csv.DictReader(infile)

        # Iterate through each row
        for row in content:
            print(row)

        # Print out only Water Temps
        for row in content:
            value = row["Water Temp"]
            print(value)

def simpleWriter():
    # Open the file with 'write' mode
    with open("new-file.csv", "w") as outfile:
        # Create a writer object
        myWriter = csv.writer(outfile, delimiter=',')

        # Write out the Headers for the CSV file
        myWriter.writerow(["Header 1", "Header 2", "Header 3"])

        # Write one row at a time
        myWriter.writerow(["R1 - First Col", "R1 - Second Col", "R1 - Third Col"])
        myWriter.writerow(["R2 - First Col", "R2 - Second Col", "R2 - Third Col"])

        # Write multiple rows with a loop
        # moreData is a 2 Dimensional List
        # where every sublist represents a row in the CSV file
        moreData = [
            ["R3 - First Col", "R3 - Second Col", "R3 - Third Col"],
            ["R4 - First Col", "R4 - Second Col", "R4 - Third Col"],
            ["R5 - First Col", "R5 - Second Col", "R5 - Third Col"]
            ]

        for row in moreData:
            myWriter.writerow(row)

def dictionaryWriter():
    # Open the file with 'write' mode
    with open("new-file.csv", "w") as outfile:

        # Define a list containing desired fieldnames for the CSV
        myFieldnames = ["Header 1", "Header 2", "Header 3"]

        # Create a DictWriter object with the fieldnames defined
        myWriter = csv.DictWriter(outfile, fieldnames=myFieldnames)
        # Write the Headers
        myWriter.writeheader()

        # Write one row at a time
        myWriter.writerow(
            {
                'Header 1': 'R1 - First Col',
                'Header 2': 'R1 - Second Col',
                'Header 3': 'R1 - Third Col'
                })

        # Write multiple rows with a loop
        # moreData is a List of Dictionaries
        moreData = [
            {
                myFieldnames[0]: "R2 - First Col",
                myFieldnames[1]: "R2 - Second Col",
                myFieldnames[2]: "R2 - Third Col",
            },
            {
                myFieldnames[0]: "R3 - First Col",
                myFieldnames[1]: "R3 - Second Col",
                myFieldnames[2]: "R3 - Third Col",
            }
        ]

        for row in moreData:
            myWriter.writerow(row)


if __name__ == "__main__":
    simpleReader()
    #dictionaryReader()
    #simpleWriter()
    #dictionaryWriter()
