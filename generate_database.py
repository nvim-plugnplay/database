#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: generate_data.py
__org_name__ = "PlugNPlay"
__docformat__ = "numpy"
__version__ = "0.0.2"

import json
import os
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from rich import print

try:
    from icecream import ic
except ImportError:
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

#  ╭────────────────────────────────────────────────────────────────────╮
#  │ TODO: Look through plugin categories and check whether they have   │
#  │  "Neovim" in them                                                  │
#  │ or just implement some sort of smarter filtering in general        │
#  ╰────────────────────────────────────────────────────────────────────╯


class GenerateData:
    """Generate data for plugins

    Attributes
    ----------
    client_id: str
        The client id for the github api
    client_secret: str
        The client secret for the github api
    wanted_fields: list
        The fields that we want to extract from the json
    plugins: dict
        The plugins that we want to extract data from
    count: int
        The current page we are on
    plugins: dict
        The plugins that we want to extract data from
    """

    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        self.wanted_fields = [
            "full_name",
            "description",
            "default_branch",
            "fork",
            "archived",
            "private",
            "clone_url",
            "commits_url",
            "created_at",
            "updated_at",
            "stargazers_count",
            "subscribers_count",
            "forks_count",
            "language",
            "open_issues_count",
            "topics",
            "owner",
        ]
        # this is not accurate but it will be good enough for now.
        self.unwanted_config = [
            "dotfiles",
            "dots",
            "nvim-dotfiles",
            "nvim-qt",
            "nvim-config",
            "config",
            "configuration",
            "neovim-lua",
            "vim-config",
        ]
        self.ignore_list = ["lspconfig", "lsp_config", "cmp", "coq", "neorg", "norg"]
        self.dotfile_count = 1
        self.not_plugin_or_dotfile = 1
        self.plugins = {}
        self.dotfiles = {}
        self.count = 1
        self.plugin_count = 1
        self.generator()

        self.get_stats()

    def get_stats(self) -> None:
        """Get stats for the data"""
        print("\n\n")
        print("Stats")
        print("-----")
        ic("Success! Dumped", self.count - 1, "pages worth of plugins")
        ic("Total plugins:", self.plugin_count)
        # ic("Total unwanted fields:", self.not_plugin_or_dotfile)
        # ic(
        #     "Percentage of unwanted fields:",
        #     (self.unwanted_field_count / self.plugin_count) * 100,
        # )
        # # Mean
        # ic("Mean number of plugins per page:", self.plugin_count / self.count)
        print("\n\n")

    def filter_plugin(self, plugin_data: dict) -> int:
        if any(
            [
                unwanted_field in plugin_data["full_name"]
                or (
                    plugin_data["description"]
                    and unwanted_field in plugin_data["description"]
                )
                for unwanted_field in self.unwanted_config
            ]
            or plugin_data["full_name"] == "nvim"
        ):
            self.dotfile_count += 1
            return 1

        return 0

    def extract_data(self, plugin_data_json: dict) -> None:
        """Extract data from the json

        Parameters
        ----------
        plugin_data_json: dict
            The json data for the plugin
        """
        # This should avoid key error
        plugin_data = defaultdict()
        plugin_name = ""

        for field in plugin_data_json.keys():
            if field == "name":
                plugin_name = plugin_data_json[field]
            if field in self.wanted_fields:
                plugin_data[field] = plugin_data_json[field]

        # rename to total_repos
        self.plugin_count += 1

        if "commits_url" in plugin_data:
            commit_req = requests.get(
                plugin_data["commits_url"][:-6],
                auth=(self.client_id, self.client_secret),
            )

            if commit_req.status_code == 200:
                commit = commit_req.json()[-1]
                plugin_data["commit"] = commit["sha"]

        del plugin_data["commits_url"]
        plugin_data = {k: v for k, v in plugin_data.items()}
        self.plugins = {**self.plugins, f"{plugin_name}": {**plugin_data}}
        print("Parsed", plugin_data["full_name"])

    def check_rate(self, req: requests) -> None:
        """Check rate is being limited.

        Parameters
        ----------
        req: requests
                Request type to check limits.
        """
        if req.find("API rate limit exceeded") != -1:
            print("API rate limit exceeded")
            print(req)
            exit(-1)

    def generator(self) -> None:
        """Generate the data for the plugins"""
        countter = 0
        with open("database.json", "+w") as file, open(
            "dotfiles.json", "+w"
        ) as dotfile:
            while True:

                req = requests.get(
                    "https://api.github.com/users/budswa/starred?per-page=1&page="
                    + str(self.count),
                    auth=(self.client_id, self.client_secret),
                )
                print("Grabbed page", self.count)
                # For test cases grab only 5 pages
                if countter == 5:
                    break

                countter += 1
                self.count += 1
                self.check_rate(req.text)
                for plugin_data_json in req.json():

                    current_url_info = defaultdict(str)
                    soup = BeautifulSoup(
                        requests.get(plugin_data_json["html_url"]).content,
                        "html.parser",
                    )
                    for item in soup.find_all("a", {"class", "js-navigation-open"}):

                        dir_info = item.get("href")
                        if "/" in dir_info:
                            current_url_info[item.text] = item.get("href")

                    ic(current_url_info)

                    __import__("pdb").set_trace()

                    # self.extract_data(plugin_data_json)

                if "next" not in req.links:
                    break

            file.write(json.dumps(self.plugins, sort_keys=True, indent=4))
            dotfile.write(json.dumps(self.dotfiles, sort_keys=True, indent=4))


def main() -> None:
    """Main Function"""
    GenerateData()


if __name__ == "__main__":
    main()
