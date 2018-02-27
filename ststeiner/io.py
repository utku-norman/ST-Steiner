'''
Copyright (C) 2018 Utku Norman

This file is part of ST-Steiner

ST-Steiner is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ST-Steiner is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# standard library imports
import json

# third party imports
import pathlib as pl
import networkx as nx

# local application imports
from ststeiner.utils import s_if_plural, is_none


def read_prizes(path, logger=None, upper=False):
    '''Read node prize data from file.'''

    prizes = dict()

    if logger is not None:
        logger.debug('Prizes read from {}'.format(path))

    with pl.Path(path).open() as f:
        for l in f:
            l = l.strip().split()
            if upper:
                prizes[l[0].upper()] = float(l[1])
            else: 
                prizes[l[0]] = float(l[1])
    return prizes


def read_network(file, logger=None, upper_nodes=True):

    if logger is not None:
        logger.debug('Reading network from {}'.format(file))

    G = nx.read_edgelist(str(file), data=(('weight', float), ))

    if logger is not None:
        n = G.number_of_nodes()
        m = G.number_of_edges()
        logger.debug('Network has {:,} node{}, {:,} edge{}.'.format(
            n, s_if_plural(n), m, s_if_plural(m)))

    if upper_nodes:
        G_upper = nx.Graph()
        for u, v, a in G.edges(data='weight'):
            G_upper.add_edge(u.upper(), v.upper(), weight=a)
        return G_upper
    else:
        return G


def read_json(file, logger=None):

    file = pl.Path(file)

    if not file.exists():
        if logger is not None:
            logger.debug('{} does not exist'.format(file))
        return None

    with file.open() as f:
        data = json.load(f)

    return data


def write_dict(path, dictionary, sep='\t'):

    path = pl.Path(path)

    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w') as f:
        for k, v in dictionary.items():
            print('{}{}{}'.format(k, sep, v), file=f)


def write_json(file, data, logger=None):

    file = pl.Path(file)

    if logger is not None:
        logger.debug('Saving to {}'.format(file))

    if not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=True)

    with file.open('w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


def write_result(G, logger=None):

    result = {**G.graph,
              'beta': beta,
              }

    write_json(result_file, result, logger)