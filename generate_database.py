#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: generate_data.py
__orgname__ = "PlugNPlay"
__docformat__ = "numpy"
__version__ = "0.0.2"

import asyncio
import functools
import itertools as it
import json
import logging
from collections import defaultdict
from typing import Any

import requests
from bs4 import BeautifulSoup
from icecream import ic
from rich import print
from rich.logging import RichHandler

from models import BaseRequestResponse

root = logging.getLogger()
if root.handlers:
    for h in root.handlers:
        root.removeHandler(h)()

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            logging.info("Creating event loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def key_mapper(key):

    def cond_mapper(fn, iterable):

        def output(d: dict):
            return sum(fn(d[key], x) if key in d.keys() else 0 for x in iterable)

        return output

    return cond_mapper


class GenerateData(object):

    def __init__(self, user: str = "budswa") -> None:
        # parametrize user
        self.user = user
        self.user_fmt = ic.format(self.user)
        # just grab whole thing not page by page!
        self.base_url = "https://api.github.com/users/{}/starred".format(self.user)
        self.client_id = "7fe0a33f01d1a6b60b08"
        self.client_secret = "f4abd5a32d99a3f48a16743f134fcdd55e967eaa"

        # perhaps export to a `constants` module
        self.wanted_fields = [
            "full_name", "description", "default_branch", "fork", "archived", "private",
            "clone_url", "commits_url", "created_at", "updated_at", "stargazers_count",
            "subscribers_count", "forks_count", "language", "open_issues_count", "topics", "owner",
        ]
        # this is not accurate but it will be good enough for now.
        self.unwanted_config = [
            "dotfiles", "dots", "nvim-dotfiles", "nvim-qt", "nvim-config", "neovim-lua",
            "vim-config", "nvim-lua", "config-nvim",
        ]
        self.ignore_list = ["lspconfig", "lsp_config", "cmp", "coq", "neorg", "norg"]
        self.dotfile_count = 1
        self.plugins = {}
        self.dotfiles = {}

        # Stats
        self.count = 1
        self.plugin_count = 1
        self.filter_count = 0
        self.req = 0
        self.extract_jobs: list[tuple[dict, bool]] = []

    def load_stars(self) -> BaseRequestResponse:
        """

        Returns
        -------
        BaseRequestResponse

        """
        logging.info("Querying github stars for {}".format(self.user_fmt))
        response = requests.get(self.base_url, auth=(self.client_id, self.client_secret))
        out = BaseRequestResponse(responses=response.json()
                                 )  # validates the response is good, otherwise will raise an error
        if len(out.responses) == 0:
            logging.warning("No stars for {} found!".format(self.user_fmt))
        logging.info("Star query: done!")
        return out

    def extract_data(self, plugin_dict: dict, is_plugin: bool) -> dict:
        plugin_data = defaultdict()
        plugin_name = ""

        for field in plugin_dict.keys():
            if field == "name":
                plugin_name = plugin_dict[field]
            if field in self.wanted_fields:
                plugin_data[field] = plugin_dict[field]

        if "commits_url" in plugin_dict:
            commit_req = requests.get(
                plugin_dict["commits_url"][:-6], auth=(self.client_id, self.client_secret),
            )

            if commit_req.status_code == 200:
                commit = commit_req.json()[-1]
                plugin_data["commit"] = commit["sha"]

            del plugin_data["commits_url"]
        plugin_data = {k: v for k, v in plugin_data.items()}

        # iS there  a better way of doing this ?
        out = {
            'name': plugin_name,
            'data': plugin_data
        }
        out['type'] = 'plugin' if is_plugin else 'dotfile'
        ic.configureOutput(prefix="Parsed: ")
        logging.info(ic.format(out['name']))

        return out

    def make_jobs(self, base: BaseRequestResponse) -> None:
        logging.info("Generating jobs!")
        name_mapper = key_mapper('name')
        fullname_mapper = key_mapper('full_name')
        description_mapper = key_mapper('description')
        ends_nvim = fullname_mapper(lambda x, y: x.endswith(y), ['.nvim', '-nvim', '.vim'])
        begins_dot = name_mapper(lambda x, y: x.startswith(y), '.')

        plugin_conds = [
            lambda d: max(0,
                          ends_nvim(d) - begins_dot(d)),  # extensions_support
            name_mapper(lambda x, y: y in x, self.ignore_list),  # ignore list
        ]
        dotfile_conds = [
            fullname_mapper(lambda x, y: y in x, self.unwanted_config),
            description_mapper(lambda x, y: y in x if x is not None else 0, self.unwanted_config)
        ]
        conds = (plugin_conds, dotfile_conds)
        cases = {
            # mappings for conditions based on conditions
            (1, 0): "plugin_count",
            (0, 1): "dotfile_count"
        }
        for response in base.responses:
            plugin_data = response.dict()
            case = tuple(map(lambda c: sum(cn(plugin_data) for cn in c), conds))
            case = tuple(map(lambda x: min(1, x), case))
            if case in cases.keys():
                self.extract_jobs.append((plugin_data, bool(case[0])))
            else:
                current_url_info = defaultdict(str)
                soup = BeautifulSoup(requests.get(plugin_data["html_url"]).content, "html.parser",)
                for item in soup.find_all("a", {"class", "js-navigation-open"}):

                    dir_info = item.get("href")
                    if "/" in dir_info:
                        current_url_info[item.text] = item.get("href")

                # Is there a cleaner way to this ?
                if ("init.lua" in current_url_info or "init.vim" in current_url_info):
                    self.extract_jobs.append((plugin_data, True))

                elif current_url_info["plugin"] != "":
                    self.extract_jobs.append((plugin_data, False))

                else:
                    pass
        ic.configureOutput("Created: ")
        logging.info(ic.format(len(self.extract_jobs)))

    async def run_jobs(self):
        loop = asyncio.get_running_loop()
        results = await asyncio.gather(*[
            loop.run_in_executor(None, functools.partial(self.extract_data, *j),
                                ) for j in self.extract_jobs
        ])
        return results

    @staticmethod
    def sort_results(results: list[dict]) -> dict[str, list[dict]]:
        results = sorted(results, key=lambda x: x['type'])
        grouped = {k: list(g) for k, g in it.groupby(results, lambda x: x['type'])}
        ic.configureOutput("Group Counts: ")
        logging.info(ic.format(len(grouped['plugin'])))
        logging.info(ic.format(len(grouped['dotfile'])))
        for k in grouped.keys():
            for item in grouped[k]:
                item.pop('type')
        return grouped

    @staticmethod
    def write_results(results: dict[str, list[dict]]) -> None:
        logging.info("writing plugins")
        plugin_dict = {}
        for item in results['plugin']:
            plugin_dict[item['name']] = item['data']
        with open("database.json", "+w") as f:
            f.write(json.dumps(plugin_dict, sort_keys=True, indent=4))

        logging.info("writing dots")
        dotfile_dict = {}
        for item in results['dotfile']:
            dotfile_dict[item['name']] = item['data']
        with open("dotfiles.json", "+w") as f:
            f.write(json.dumps(dotfile_dict, sort_keys=True, indent=4))

    def __call__(self, *args: Any, write_results: bool = True, **kwds: Any) -> Any:
        base = self.load_stars()
        self.make_jobs(base)
        logging.info("Running jobs!")
        loop = get_or_create_eventloop()
        results = loop.run_until_complete(self.run_jobs())
        results_grouped = self.sort_results(results)
        if write_results: self.write_results(results_grouped)
        return results_grouped


def main() -> None:
    """Main Function"""
    dg = GenerateData()
    dc = dg(write_results=False)
    __import__('pdb').set_trace()


if __name__ == "__main__":
    main()
