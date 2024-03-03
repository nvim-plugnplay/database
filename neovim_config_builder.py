# take all the names from json file
# ane make a file with lua format
#
# use{repo_name} in one big file
# json file is massive
import json

with open("lua_file.lua", "w") as f:
    with open("database.json", "r") as j:
        repo_list = json.load(j)
        for repo in repo_list:
            # not subscriptable
            json_repo = repo_list[repo]["full_name"]

            call = "use('{}')".format(json_repo)
            f.write(call + "\n")
# at the end of the file add a call to the main function

with open("lua_file.lua", "a") as f:
    with open("database.json", "r") as j:
        repo_list = json.load(j)
        for repo in repo_list:

            json_repo = repo_list[repo]["full_name"]
            replaceable = ["lua", "vim", "nvim"]
            new_ = None
            for word in replaceable:
                new_ = json_repo.replace("." + word, "")
            # name/repo
            # get rid of name/ and keep repo
            new_ = new_[new_.find("/") + 1:]
            pcal = "pcall(require,setup('{}'))".format(new_)

            f.write(pcal + "\n")
