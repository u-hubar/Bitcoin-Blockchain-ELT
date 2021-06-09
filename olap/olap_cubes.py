from __future__ import print_function
from cubes import Workspace
from utils import config

# 1. Create a workspace
workspace = Workspace()
workspace.register_default_store(
      "sql",
      url=f"postgresql://postgres:{config.PG_USR}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_DBNAME}"
)
workspace.import_model("olap/model.json")

# 2. Get a browser
browser = workspace.browser("Transactions")

# 3. Play with aggregates
result = browser.aggregate()

print("Total\n"
      "----------------------")

print("Record count : %8d" % result.summary["record_count"])
print("Total amount : %8d" % result.summary["amount_sum"])
print("Double amount: %8d" % result.summary["double_amount_sum"])
