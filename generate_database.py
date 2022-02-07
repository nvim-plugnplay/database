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
from typing import Any, Callable
import os
import sys

import requests
import tqdm
from bs4 import BeautifulSoup
from icecream import ic
from joblib import Parallel, delayed
from rich.logging import RichHandler

from models import BaseRequestResponse

root = logging.getLogger()
if root.handlers:
    for h in root.handlers:
        root.removeHandler(h)()

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])


def get_or_create_eventloop() -> Any:
    """
    Gets the current asyncio event loop. Asyncio only
    opens an event loop when called in the main thread,

    Returns
    -------
    the current or created asyncio event loop
    """
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            logging.info("Creating event loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def key_mapper(key):
    """
    helper for working with annoying dicts and lists of dicts
    runs a function over external iterable on a specific dict key

    Examples:
    --------

    >>> d = {'a':1, 'b':2}
    >>> d2 = {'a':0, 'b':2}
    >>> l = [0,2,3,4,5,6,7]
    >>> a_mapper = key_mapper('a')
    >>> b_mapper = key_mapper('b')
    >>> equals_l = b_mapper(lambda x,y: x == y, l)
    >>> equals_l(d)
    >>> # 0
    >>> equals_l(d2)
    >>> # 1

    Parameters
    ----------
    key : key to map a function over



    Returns
    -------
    cond_mapper : function which takes in a function which asserts a condition over an iterable, and returns a function which runs the supplied function over the supplied iterable and the input

    """

    def cond_mapper(fn, iterable):
        """

        Parameters
        ----------
        fn : a callable, which takes in 2 positional args, the first of which is supplied later on, and the second of which comes from the supplied iterable

        iterable : list of parameters to supply to fn


        Returns
        -------
        output : a function which takes in a dict, indexes it with previously supplied key, and compares that index to a previously supplied iterable

        """

        def output(d: dict):
            return sum(fn(d[key], x) if key in d.keys() else 0 for x in iterable)

        return output

    return cond_mapper


class GenerateData(object):
    """

    Attributes
    ----------
    batch_size : batch size for asyncrhonous API calls.
    use_batches : whether or not batches are used
    user : the user
    user_fmt : formatted version of the user
    base_url : url for users starpage
    client_id : client id
    client_secret : secret
    wanted_fields : fields we care about
    unwanted_config : fields we dont care about
    ignore_list : i am confused about this one
    extract_jobs : jobs to extract plugin data
    html_jobs : jobs to extract html data
    """


    def __init__(self, user: str = "budswa", batch_size: int = -1) -> None:
        """

        Parameters
        ----------
        user : str, the username

        batch_size : int, batch size for asyncio, if < 1 do not use batches at all (saves a couple of requests, uses way more memory, batch size only really needed if github limits our concurrent api requests)

        """
        ic.configureOutput(prefix="")
        # parametrize user
        self.batch_size = batch_size
        self.use_batches = self.batch_size > 0
        self.user = user
        self.user_fmt = ic.format(self.user)
        # just grab whole thing not page by page!
        self.base_url = "https://api.github.com/users/{}/starred?per-page=1&per_page=100&page=".format(
            self.user)
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['SECRET_ID']

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
        self.extract_jobs: list[tuple[dict, bool]] = []
        self.html_jobs: list[tuple[str]] = []

    def async_helper(self, fn: Callable[[tuple], Any], iterable: list) -> list:
        """
        Helper for simple async usages. Complicated stuff should be done normally

        Parameters
        ----------
        fn : Callable[[tuple], Any], function to run asynchronously

        iterable : list, list of parameters for fn


        Returns
        -------
        list of fn(iterable_item)

        """

        async def run_jobs():
            loop = get_or_create_eventloop()
            results = []
            if self.use_batches:
                for i in tqdm.tqdm(
                        range(0,
                              len(iterable) + self.batch_size, self.batch_size), desc=fn.__name__):
                    results += await asyncio.gather(*[
                        loop.run_in_executor(None, functools.partial(fn, *j),
                                            ) for j in iterable[i:i + self.batch_size]
                    ])
            else:
                results += await asyncio.gather(
                    *[loop.run_in_executor(None, functools.partial(fn, *j),
                                          ) for j in iterable])

            return results

        return asyncio.run(run_jobs())

    def load_stars_by_page(self, page: int) -> BaseRequestResponse:
        """

        Parameters
        ----------
        page : int


        Returns
        -------
        BaseRequestResponse

        """
        logging.debug("Querying github stars for {}, {}".format(self.user_fmt, ic.format(page)))
        response = requests.get(
            self.base_url + str(page), auth=(self.client_id, self.client_secret))
        if response.status_code != 200:
            logging.info("using load stars by page")
            logging.critical("Bad request {}".format(ic.format(response.json)))
            sys.exit("Cannot create database")

        out = BaseRequestResponse(
            responses=response.json(),
        )  # validates the response is good, otherwise will raise an error
        if len(out.responses) == 0:
            logging.warning("No stars for {}, {} found!".format(self.user_fmt, ic.format(page)))
        return out

    async def get_pages(self) -> BaseRequestResponse:
        """
        gets all starpages for a user, works by grabbing 10 pages at a time, when all pages are empty, stops making more pages

        Returns
        -------
        response: BaseRequestResponse


        """
        loop = get_or_create_eventloop()
        results = []
        finished = False
        start = 0
        batch_size = 10
        while not finished:
            tmp = await asyncio.gather(*[
                loop.run_in_executor(None, functools.partial(self.load_stars_by_page, start + i),
                                    ) for i in range(1, batch_size + 1)
            ])
            tmp = BaseRequestResponse(responses=list(it.chain(*[t.responses for t in tmp])))
            if len(tmp.responses) == 0:
                finished = True
            results += tmp.responses
            start += batch_size
        response = BaseRequestResponse(responses=results)
        return response

    def extract_data(self, plugin_dict: dict, is_plugin: bool) -> dict:
        """
        extracts commit data from a plugin or dotfile

        Parameters
        ----------
        plugin_dict : dict, dict describing dotfile or plugin

        is_plugin : bool, is it a plugin? or a dotfile?


        Returns
        -------
        dict containing the plugin name, plugin data, and whether it is a plugin or dotfile('type')

        """
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
            else:
                logging.info("using extractdata ")
                logging.critical("Bad request {}".format(ic.format(commit_req.json())))
                sys.exit("Cannot create database")

            del plugin_data["commits_url"]

        plugin_data = {k: v for k, v in plugin_data.items()}

        # iS there  a better way of doing this ?
        out = {
            'name': plugin_name,
            'data': plugin_data
        }
        out['type'] = 'plugin' if is_plugin else 'dotfile'
        ic.configureOutput(prefix="Parsed: ")
        logging.debug(ic.format(out['name']))

        return out

    @staticmethod

    def make_html_request(d: dict):
        "https://api.github.com/repos/[USER]/[REPO]/git/trees/[BRANCH]?recursive=1"
        response = requests.get(d['html_url'])
        if response.status_code != 200:
            logging.info("using make_html_request")
            logging.critical("Bad request {}".format(ic.format(response.json())))
            sys.exit("Cannot create database")
        __import__('pdb').set_trace()
        return response

    def make_jobs(self, base: BaseRequestResponse) -> None:
        """
        Given a response list, generate jobs(read: sets of parameters) for extract_data to run asynchronously
        Iterates through the response list, and for each one, creates a plugin or dotfile job. For some edge cases,
        it creates a list of jobs to parse some html relating to the plugin or dotfile, and uses the result of that to create more jobs

        Parameters
        ----------
        base : BaseRequestResponse


        """
        logging.info("Generating jobs!")
        name_mapper = key_mapper('name')  # uses d['name']
        fullname_mapper = key_mapper('full_name')  # uses d['full_name']
        description_mapper = key_mapper('description')  # uses d['description']
        ends_nvim = fullname_mapper(
            lambda x, y: x.lower().endswith(y.lower()),
            ['.nvim', '-nvim', '.vim'])  # checks if d['full_name'] ends with .nvim, -nvim, .vim
        begins_dot = name_mapper(lambda x, y: x.lower().startswith(y.lower()),
                                 '.')  # check if d['name'] starts with '.'
        plugin_conds = [
            lambda d: max(0,
                          ends_nvim(d) - begins_dot(d)
                         ),  # 1 if ends_nvim, 0 if ends_nvim and begins dot, 0 otherwise
            name_mapper(
                lambda x, y: y.lower() in x.lower(), self.ignore_list
            )  # checks if any values from the ignore list are present in d['name'], does this belong here or does this remove things to be requested?
        ]
        dotfile_conds = [
            fullname_mapper(lambda x, y: y.lower() in x.lower(), self.unwanted_config
                           ),  # checks if any of the unwanted config names are in d['full_name']
            description_mapper(
                lambda x, y: y.lower() in x.lower() if x is not None else 0, self.unwanted_config
            ),  # check if any of the unwanted config names are in d['description']
            begins_dot,  # check if it begins with a dot
        ]
        conds = (plugin_conds, dotfile_conds)
        cases = {
            # mappings for conditions based on conditions
            (1, 0): "plugin_count",
            (0, 1): "dotfile_count"
        }

        # for response in tqdm.tqdm(base.responses):
        def make_jobtype(response):
            # helper for joblib
            plugin_data = response.dict()
            case = tuple(map(lambda c: sum(cn(plugin_data) for cn in c), conds))
            case = tuple(map(lambda x: min(1, x), case))
            if case in cases.keys():
                return (plugin_data, bool(case[0]))
            else:
                return (plugin_data,)

        initial_jobs = Parallel(-1)(
            delayed(make_jobtype)(response)
            for response in base.responses)  # gets all the jobtypes, in parallel over all cores
        self.html_jobs.extend([j for j in initial_jobs if len(j) == 1])
        self.extract_jobs.extend([j for j in initial_jobs if len(j) == 2])
        __import__('pdb').set_trace()
        html_results = self.async_helper(lambda x: (x, self.make_html_request(x)), self.html_jobs)
        for res in html_results:
            current_url_info = defaultdict(str)
            plugin_data = res[0]
            html = res[-1]
            soup = BeautifulSoup(html.content, "html.parser")
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
        # __import__('pdb').set_trace()
        ic.configureOutput("Created: ")
        logging.info(ic.format(len(self.extract_jobs)))

    async def run_jobs(self):
        """
        Runs jobs

        Returns
        -------
        results : list of star pages

        """
        loop = get_or_create_eventloop()
        results = []
        for i in tqdm.tqdm(range(0, len(self.extract_jobs) + self.batch_size, self.batch_size)):
            results += await asyncio.gather(*[
                loop.run_in_executor(None, functools.partial(self.extract_data, *j),
                                    ) for j in self.extract_jobs[i:i + self.batch_size]
            ])
        return results

    @staticmethod
    def sort_results(results: list[dict]) -> dict[str, list[dict]]:
        """
        sorts results by plugin or not

        Parameters
        ----------
        results : list[dict]


        Returns
        -------
        dict[str, list[dict]]

        """
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
        """
        Writes sorted results to database

        Parameters
        ----------
        results : dict[str, list[dict]]

        """
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
        """

        Parameters
        ----------
         *args: Any

        write_results : bool

         **kwds: Any


        Returns
        -------
       dict[str, list[dict]]

        """
        loop = get_or_create_eventloop()
        logging.info("Getting stars for {}".format(self.user_fmt))
        base = asyncio.run(self.get_pages())
        self.make_jobs(base)
        ic.configureOutput(prefix="")
        logging.info("Running {} jobs!".format(
            ic.format(len(self.html_jobs) + len(self.extract_jobs))))
        results = self.async_helper(self.extract_data, self.extract_jobs)
        results_grouped = self.sort_results(results)
        if write_results: self.write_results(results_grouped)
        return results_grouped


def main() -> None:
    """Main Function"""
    dg = GenerateData(batch_size=10)
    dc = dg()
    return dc


if __name__ == "__main__":
    __import__('dotenv').load_dotenv('dev.env')

    main()
