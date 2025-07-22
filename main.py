import pandas as pd
from datetime import datetime
import sys
import os
import csv

# importing the database file and formatting
database = pd.read_csv(r"startup_funding_project\startup_funding_data.csv")
database.columns = [i.title() for i in list(database.columns)]

# replacing invalid dates, converting data into date and adding years column
database["Date"] = pd.to_datetime(database["Date"], format="%d/%m/%Y", errors="coerce")
database["Year"] = database["Date"].dt.year

# removing commas and converting amount into integer and handling invalid amounts
for index in range(0, len(database)):
    try:
        database.loc[index, "Amount_Usd"] = int(
            database.loc[index, "Amount_Usd"].replace(",", "")
        )
    except:
        database.loc[index, "Amount_Usd"] = pd.NA
# sorting the database before applying indexes
database = database.sort_values(by="Date", ascending=False)
database.index = [i for i in range(1, len(database) + 1)]

# adding no of investors column and reordering all the columns
database["No_Of_Investors"] = database["Investors"].apply(
    lambda x: pd.NA if pd.isna(x) else int(len(x.split(",")))
)
database = database.loc[
    :,
    [
        "Date",
        "Year",
        "Startup",
        "Sector",
        "Sub_Sector",
        "City",
        "Investors",
        "No_Of_Investors",
        "Investment_Type",
        "Amount_Usd",
    ],
]

filtered_startups = set(database["Startup"])
filtered_funding = [0, 99999999999]
filtered_years = [1, 9999]
filtered_sectors = set(database["Sector"])
filtered_sub_sectors = set(database["Sub_Sector"])
filtered_investors = set(database["Investors"])
filtered_investment_type = set(database["Investment_Type"])
filtered_no_investors = [0, 9999]
master_database = database.copy()


# to strip and lower the input
def get_input(prompt=""):
    return input(prompt).strip().lower()


# function to display output in display_data
def output(database, function, asc, no_results, arg=0):

    for index, (x, y) in enumerate(
        getattr(database["Amount_Usd"], function)().sort_values(ascending=asc).items(),
        start=1,
    ):
        if index <= no_results:
            if arg == 0:
                print(f"{index}. {x} : USD {y:,.0f}".replace(",", " "))
            else:
                print(f"{index}. {x} : {y:,.0f}".replace(",", " "))


# asks user how they want data to be sorted
def sort_data(database):
    print("\nYou can sort the data by default in following ways :")
    print("1. Date (New to Old) (Default)")
    print("2. Date (Old to New)")
    print("3. Amount (Max to Min)")
    print("4. Amount (Min to Max)")
    print("5. No of Investors (Max to Min)")
    print("6. No of Investors (Min to Max)")
    print("7. Alphabetical Order (A-Z)")
    print("8. Alphabetical Order (Z-A)")
    print("9. Sector (A-Z)")
    print("10. Sector (Z-A)")
    print("11. City (A-Z)")
    print("12. City (Z-A)")

    while True:
        choice = get_input("\nChoose the option number : ")

        match choice:
            case "1":
                database = database.sort_values(by="Date", ascending=False)
                break
            case "2":
                database = database.sort_values(by="Date", ascending=True)
                break
            case "3":
                database = database.sort_values(by="Amount_Usd", ascending=False)
                break
            case "4":
                database = database.sort_values(by="Amount_Usd", ascending=True)
                break
            case "5":
                database = database.sort_values(by="No_Of_Investors", ascending=False)
                break
            case "6":
                database = database.sort_values(by="No_Of_Investors", ascending=True)
                break
            case "7":
                database = database.sort_values(by="Startup", ascending=True)
                break
            case "8":
                database = database.sort_values(by="Startup", ascending=False)
                break
            case "9":
                database = database.sort_values(by="Sector", ascending=True)
                break
            case "10":
                database = database.sort_values(by="Sector", ascending=False)
                break
            case "11":
                database = database.sort_values(by="City", ascending=True)
                break
            case "12":
                database = database.sort_values(by="City", ascending=False)
                break
            case _:
                print("\nEnter a valid choice")
    return database


# displays all the raw data, user can select if they want upto a specific no of rows
def display_data(database):

    # setting changes to display the table properly
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", 25)
    pd.set_option("display.width", 1000)

    # changing the values into formatted ones
    database["Amount_Usd"] = database["Amount_Usd"].apply(
        lambda x: f"{x:,}".replace(",", " ")
    )

    # accepting correct input only
    while True:
        print("\nThe startups are sorted by your preferance")
        cases = get_input("Enter how many startups you want to see (or 'all') : ")
        try:
            if cases == "all" or int(cases) > len(database):
                cases = len(database)
                break
            elif int(cases) < 1:
                print("\nThe number of cases cannot be less than 1.")
            else:
                cases = int(cases)
                break
        except ValueError:
            print("\nThe number of cases must be a number.")

    # printing the data
    print(database.head(cases))
    return


# displays the stats
def display_funding_data(database, asc, no_results, arg=0):
    # if user wants to view overall data stats
    if arg == 1:
        print(f"Total Funding   : USD {database['Amount_Usd'].sum():.0f}")
        print(f"Average Funding : USD {database['Amount_Usd'].mean():.0f}")
        print(f"Median Funding  : USD {database['Amount_Usd'].median():.0f}")
        print(f"Maximum Funding : USD {database['Amount_Usd'].max():.0f}")
        print(f"Minimum Funding : USD {database['Amount_Usd'].min():.0f}")
        print(f"Total Startups  : {len(database)}")

    # if user wants to view grouped data stats
    else:
        print(f"\nTotal Funding   : ")
        output(database, "sum", asc, no_results)

        print(f"\nAverage Funding : ")
        output(database, "mean", asc, no_results)

        print(f"\nMaximum Funding :")
        output(database, "max", False, no_results)

        print(f"\nMinimum Funding :")
        output(database, "min", True, no_results)

        print(f"\nTotal Startups  :")
        output(database, "size", asc, no_results, 1)


# asking user which stats they want
def display_funding_overview(database):

    if len(database) < 1:
        print(
            "\nBased on your filters, there are no valid columns in dataframe, change your filters."
        )
        return

    # asking how the data should be sorted
    print("\nYou can sort the output in following ways :")
    print("1. Value (Amount/Number) descending")
    print("2. Value (Amount/Number) ascending")

    while True:

        cases = get_input("\nEnter the code of the sorting preferance : ")
        match cases:
            case "1":
                asc = False
                break
            case "2":
                asc = True
                break
            case _:
                print("\nPlease choose a valid preferance option.")

    # asking how many results should be displayed
    print("\nChoosing too many results can lead to an overwhelming data as output.")
    while True:
        no_results = get_input(
            "\n Maximum how many results you want to view (or 'all') : "
        )

        if no_results == "all":
            no_results = len(database)
            break
        else:
            try:
                no_results = int(no_results)
                if no_results < 1:
                    print("\nYou must select atleast one result to view.")
                else:
                    break
            except ValueError:
                print("\nEnter the number of results to view.")

    # displaying all available options
    print("\nYou can select the following options (seperated by a comma ',') :")
    print("1. Overall Data")
    print("2. City-wise Data")
    print("3. Sector-wise Data")
    print("4. Sub-Sector-wise Data")
    print("5. Year-wise Data")
    print("6. Investment Type Data")

    # ensuring only valid input is accepted, user can enter multiple options at once into a set

    while True:
        restart = False
        try:
            choice = get_input(
                "\nEnter the option codes (seperated by a comma ',' or 'all' to view all) : "
            )

            if choice == "all":
                choice = sorted({str(i) for i in range(1, 7)})
                break

            choice = sorted(set(choice))
            for i in choice:
                if int(i) not in [j for j in range(1, 7)]:
                    print(f"{i} is not a valid choice")
                    restart = True
                    break
            if restart:
                continue
            break

        except Exception as e:
            print(f"Please enter a valid input. {e}")

    # executing the stats functions according to the choice input
    for i in choice:
        match i:
            case "1":
                display_funding_data(database, asc, no_results, 1)
            case "2":
                display_funding_data(database.groupby("City"), asc, no_results)
            case "3":
                display_funding_data(database.groupby("Sector"), asc, no_results)
            case "4":
                display_funding_data(database.groupby("Sub_Sector"), asc, no_results)
            case "5":
                display_funding_data(database.groupby("Year"), asc, no_results)
            case "6":
                display_funding_data(
                    database.groupby("Investment_Type"), asc, no_results
                )


# select,add,remove values to filter
def filter(col_name, text_word, filtered=()):

    # copying list from master database
    full_list = set(master_database[col_name])

    # creating a filtered list if it doesnt exist
    if len(filtered) < 1:
        filtered = full_list.copy()

    # printing a full list of all {text_words}, can get messy for massive databases
    print(f"\nHere is a list of all {text_word}:")
    for index, i in enumerate(full_list):
        print(f"{index}. {i}")

    print(f"\nUsing 1. will only consider the selected {text_word}.")
    print("\n 1. Select")
    print("2. Add")
    print("3. Remove")
    print(f"4. Reset {text_word} Filter")
    while True:
        option = get_input("\nEnter the option code : ")

        match option:

            # all {text_word} are selected by default
            # using this will only keep selected values
            case "1":
                while True:
                    user_input = input(
                        f"\nEnter the {text_word} to select, seperated by comma (,) : "
                    ).strip()
                    try:
                        for i in set(user_input):
                            filtered = set(user_input).copy()
                            print(f"\nOnly your selected {text_word} will be shown.")
                            break
                    except Exception as e:
                        print(f"\nPlease enter valid input. {e}")
                break

            # adding to the filter
            case "2":
                while True:
                    user_input = input(
                        f"\nEnter the {text_word} to add, seperated by comma (,) : "
                    ).strip()
                    try:
                        filtered.union(set(user_input))
                        print(f"\nYour selected {text_word} have been added")
                        break
                    except Exception as e:
                        print(f"\nPlease enter valid input. {e}")
                break

            # removing from filter
            case "3":
                while True:
                    user_input = input(
                        "\nEnter the startups to remove, seperated by comma (,)."
                    ).strip()
                    try:
                        for i in set(user_input):
                            filtered.difference(user_input)
                            print(f"\nYour selected {text_word} have been removed")
                            break
                    except Exception as e:
                        print(f"\nPlease enter valid input. {e}")
                break

            # remove the filter
            case "4":
                filtered = full_list.copy()
                break
            case _:
                print("\nEnter a valid option code.")
    return filtered


# allows user to modify filters to ensure to the point output
def modify_filters(
    filtered_startups,
    filtered_funding,
    filtered_years,
    filtered_sectors,
    filtered_sub_sectors,
    filtered_investors,
    filtered_investment_type,
    filtered_no_investors,
    database,
):

    # ensures valid options are chosen
    while True:

        print("\nYou can add the following filters :")
        print("1. Startups")
        print("2. Funding")
        print("3. Years")
        print("4. City")
        print("5. Sectors")
        print("6. Sub-Sectors")
        print("7. Investors")
        print("8. Investment Type")
        print("9. Number of Investors")
        print("10. Reset all filters")

        choice = get_input("\nEnter the code of the filter (or 'apply') : ")

        match choice:

            case "apply":
                print("Your filters have been confirmed")
                break

            case "1":
                filtered_startups = filter("Startup", "startups", filtered_startups)

            case "2":
                while True:
                    try:
                        lower = int(
                            get_input(
                                "Enter the lower limit of funding ('0' to remove limit) : "
                            )
                        )
                        upper = int(
                            get_input(
                                "Enter the upper limit of funding ('0' to remove limit) : "
                            )
                        )
                        if lower > upper:
                            c = upper
                            upper = lower
                            lower = c
                        if lower <= 0:
                            lower = 0
                        if upper == 0:
                            upper = 99999999999
                        filtered_funding = [lower, upper]
                        break
                    except ValueError:
                        print("Enter a funding limit.")

            case "3":
                while True:
                    try:
                        lower = int(
                            get_input(
                                "Enter the lower limit of year ('0' to remove limit) : "
                            )
                        )
                        upper = int(
                            get_input(
                                "Enter the upper limit of year ('0' to remove limit) : "
                            )
                        )
                        if lower <= 1:
                            lower = 1
                        if upper < 1:
                            upper = 9999
                        if lower > upper:
                            c = upper
                            upper = lower
                            lower = c
                        filtered_years = [lower, upper]
                        break
                    except ValueError:
                        print("Enter a valid year limit.")

            case "4":
                filtered_cities = filter("City", "cities", filtered_cities)

            case "5":
                filtered_sectors = filter("Sector", "sectors", filtered_sectors)

            case "6":
                filtered_sub_sectors = filter(
                    "Sub_Sector", "sub-sectors", filtered_sub_sectors
                )

            case "7":
                filtered_investors = filter(
                    "Investors", "investors", filtered_investors
                )

            case "8":
                filtered_investment_type = filter(
                    "Investment_Type", "investment-type", filtered_investment_type
                )

            case "9":
                while True:
                    try:
                        lower = int(
                            get_input(
                                "Enter the lower limit of no. of investors ('0' to remove limit) : "
                            )
                        )
                        upper = int(
                            get_input(
                                "Enter the upper limit of no. of investors ('0' to remove limit) : "
                            )
                        )
                        if lower < 1:
                            lower = 0
                        if upper < 1:
                            upper = 9999
                        if lower > upper:
                            c = upper
                            upper = lower
                            lower = c
                        filtered_no_investors = [lower, upper]
                        break
                    except ValueError:
                        print("Enter a valid no of investors limit.")

            case "10":
                return (
                    filtered_startups,
                    filtered_funding,
                    filtered_years,
                    filtered_sectors,
                    filtered_sub_sectors,
                    filtered_investors,
                    filtered_investment_type,
                    filtered_no_investors,
                    master_database.copy(),
                )

            case _:
                print("Enter a valid filter choice.")

    filtered_database = master_database.loc[
        master_database["Startup"].isin(filtered_startups)
        & master_database["Amount_Usd"].between(
            filtered_funding[0], filtered_funding[1]
        )
        & master_database["Year"].between(filtered_years[0], filtered_years[1])
        & master_database["Sector"].isin(filtered_sectors)
        & master_database["Sub_Sector"].isin(filtered_sub_sectors)
        & master_database["Investment_Type"].isin(filtered_investment_type)
        & master_database["No_Of_Investors"].between(
            filtered_no_investors[0], filtered_no_investors[1]
        ),
        :,
    ]
    remove = {}
    for row, investor in filtered_database["Investors"].items():
        add = False
        startup_investors = [x.strip() for x in investor.split(",")]
        for j in startup_investors:
            if j in filtered_investors:
                add = True
        remove[row] = add
    for index, value in remove.items():
        if not value:
            filtered_database = filtered_database.drop(index)

    return (
        filtered_startups,
        filtered_funding,
        filtered_years,
        filtered_sectors,
        filtered_sub_sectors,
        filtered_investors,
        filtered_investment_type,
        filtered_no_investors,
        filtered_database,
    )


def export_data(database):
    while True:
        print("\neg : C:/Users/Username/Downloads/filtered_data.csv")
        file = input(
            "\nEnter the path of the file to be created (or 'cancel'): "
        ).strip()

        if file.strip().lower() == "cancel":
            break

        if not file.endswith(".csv"):
            file += ".csv"

        try:

            # checking if the path already exists
            if os.path.exists(file):
                brk = False
                print("\nThis file already exists.")
                while True:
                    confirm = get_input("\nDo you want to overwrite it ('Y'/'N')? : ")
                    if confirm == "y":
                        brk = True
                        break
                    elif confirm == "n":
                        print("\nPlease enter a different path then.")
                        break
                    else:
                        print("\nPlease enter a valid choice ('Y'/'N').")

                # restarts the loop so user can enter a different path
                if not brk:
                    continue

            # creating the new file/overwriting it
            database.to_csv(file, index=False)
            print(
                f"\nNew file containing the filtered & sorted data has been created at {os.path.abspath(file)}"
            )
            break

        except Exception as e:
            print(f"\nAn Error Occured!")
            print(e)


def main(
    filtered_startups,
    filtered_funding,
    filtered_years,
    filtered_sectors,
    filtered_sub_sectors,
    filtered_investors,
    filtered_investment_type,
    filtered_no_investors,
    database,
):

    # asking a sort preferance before starting
    database = sort_data(database)

    while True:
        # allows user to run the program unlimited times')
        print("\nYou can choose from following options :")
        print("1. Display Raw Data")
        print("2. Display Analysed Data")
        print("3. Modify Filters")
        print("4. Modify Sorting")
        print("5. Export Database")
        print("0. Exit")

        choice = get_input("\nEnter the option to choose : ")
        match choice:
            case "1":
                display_data(database)

            case "2":
                display_funding_overview(database)

            case "3":
                (
                    filtered_startups,
                    filtered_funding,
                    filtered_years,
                    filtered_sectors,
                    filtered_sub_sectors,
                    filtered_investors,
                    filtered_investment_type,
                    filtered_no_investors,
                    database,
                ) = modify_filters(
                    filtered_startups,
                    filtered_funding,
                    filtered_years,
                    filtered_sectors,
                    filtered_sub_sectors,
                    filtered_investors,
                    filtered_investment_type,
                    filtered_no_investors,
                    database,
                )

            case "4":
                database = sort_data(database)

            case "5":
                export_data(database)

            case "0":
                print("Thank you for using the program.")
                sys.exit()


main(
    filtered_startups,
    filtered_funding,
    filtered_years,
    filtered_sectors,
    filtered_sub_sectors,
    filtered_investors,
    filtered_investment_type,
    filtered_no_investors,
    database,
)
