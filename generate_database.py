#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: generate_data.py

import json
import os
from collections import defaultdict

import requests

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
        # Edge cases like lspconfig will be included in this
        # this is not accurate but it will be good enough for now.
        self.unwanted_config = [
            "dotfiles",
            "dots",
            "nvim-dotfiles",
            "nvim-qt",
            "nvim-config",
            "config",
            "configuration",
        ]
        self.unwanted_field_count = 1

        self.plugins = {}
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
        ic("Total unwanted fields:", self.unwanted_field_count)
        ic(
            "Percentage of unwanted fields:",
            (self.unwanted_field_count / self.plugin_count) * 100,
        )
        # Mean
        ic("Mean number of plugins per page:", self.plugin_count / self.count)
        print("\n\n")

    def check_unwanted_fields(self, plugin_data: dict) -> None:
        """Check if the plugin has unwanted fields

        Parameters
        ----------
        plugin_data_json: dict
            The json data for the plugin

        Returns
        -------
        bool
            True if the plugin has unwanted fields, False otherwise
        """
        if any(
            [
                unwanted_field in plugin_data["full_name"]
                or (
                    plugin_data["description"]
                    and unwanted_field in plugin_data["description"]
                )
                for unwanted_field in self.unwanted_config
            ]
        ):
            self.unwanted_field_count += 1

            if plugin_data["description"]:
                ic(
                    "Plugin",
                    plugin_data["full_name"],
                    plugin_data["description"],
                    self.unwanted_field_count,
                    self.plugin_count,
                )

            else:
                ic(
                    "Plugin",
                    plugin_data["full_name"],
                    self.unwanted_field_count,
                    self.plugin_count,
                )

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

        # Sorry ntb, this format is not ideal but it works for now.
        self.check_unwanted_fields(plugin_data)

        self.plugin_count += 1
        if "commits_url" in plugin_data:
            commit_req = requests.get(
                plugin_data["commits_url"][:-6],
                auth=(self.client_id, self.client_secret),
            )

            # This gives a key error if the plugin has no commits
            # This is a bug in the github api or when api intrupt happens
            # ensure that status is 200
            # ic(commit_req.status_code)
            if commit_req.status_code == 200:
                commit = commit_req.json()[-1]
                plugin_data["commit"] = commit["sha"]

        # TODO: Should the following code be in the if statement ?
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
        with open("database.json", "+w") as file:
            while True:
                req = requests.get(
                    "https://api.github.com/users/budswa/starred?per-page=1&page="
                    + str(self.count),
                    auth=(self.client_id, self.client_secret),
                )
                print("Grabbed page", self.count)
                self.count += 1
                self.check_rate(req.text)

                for plugin_data_json in req.json():
                    if (
                        not plugin_data_json["language"]
                        or plugin_data_json["language"] == "lua"
                    ):
                        continue
                    self.extract_data(plugin_data_json)

                if "next" not in req.links:
                    break

            file.write(json.dumps(self.plugins, sort_keys=True, indent=4))


if __name__ == "__main__":
    GenerateData()
