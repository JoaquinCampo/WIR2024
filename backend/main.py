from politician import Politician

# politicians_2024 = [
#     {"name": "Joe Biden", "party": "Democratic"},
#     {"name": "Donald Trump", "party": "Republican"},
#     {"name": "Ron DeSantis", "party": "Republican"},
#     {"name": "Nikki Haley", "party": "Republican"},
#     {"name": "Mike Pence", "party": "Republican"},
#     {"name": "Mitch McConnell", "party": "Republican"},
#     {"name": "Chuck Schumer", "party": "Democratic"},
#     {"name": "Kamala Harris", "party": "Democratic"},
#     {"name": "Elizabeth Warren", "party": "Democratic"},
#     {"name": "Ted Cruz", "party": "Republican"}
# ]

# # List to store the politicians.
# politician_instances = []

# for politician_info in politicians_2024:
#     new_politician = Politician(name=politician_info["name"], party=politician_info["party"])
#     politician_instances.append(new_politician)

# for politician in politician_instances:
#     politician.retrieve_info()

Trump = Politician(name="Donald Trump", party="Republican")
Trump.retrieve_info

print(Trump.opinions)
