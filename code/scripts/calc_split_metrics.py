#!/usr/bin/env python3
"""Calculate splits-related metrics for all nodes in a tree.

Usage:
    calc_split_metrics.py input.nwk > output.tsv

Notes:
    The following metrics are calculated for each node:
    - taxa: number of descendants (tips)
    - splits: total number of splits from tips
    - postlevels: maximum number of splits from tips
    - prelevels: number of splits from root

    These metrics are not affected by branch lengths.
"""

import fileinput
from io import StringIO
import unittest
from unittest.mock import patch, mock_open
from skbio import TreeNode


def main():
    with fileinput.input() as f:
        tree = TreeNode.read(f)

    # calculate bottom-up metrics
    for node in tree.postorder(include_self=True):
        if node.name is None:
            raise ValueError('Error: Found an unnamed node.')
        if node.is_tip():
            node.n = 1
            node.splits = 0
            node.postlevels = 1
        else:
            node.n = sum(x.n for x in node.children)
            node.splits = sum(x.splits for x in node.children) + 1
            node.postlevels = max(x.postlevels for x in node.children) + 1

    # calculate top-down metrics
    for node in tree.preorder(include_self=True):
        if node.is_root():
            node.prelevels = 1
        else:
            node.prelevels = node.parent.prelevels + 1

    # print result
    print('name\ttaxa\tsplits\tpostlevels\tprelevels')
    for node in tree.levelorder():
        print('%s\t%d\t%d\t%d\t%d' % (node.name, node.n, node.splits,
                                      node.postlevels, node.prelevels))


class Tests(unittest.TestCase):
    def test_main(self):
        """Example from Fig. 9a of Puigbo, et al., 2009, J Biol.
                                                /-A
                                      /n9------|
                            /n8------|          \-B
                           |         |
                  /n4------|          \-C
                 |         |
                 |         |          /-D
                 |          \n7------|
                 |                    \-E
                 |
                 |                    /-F
        -n1------|          /n6------|
                 |         |          \-G
                 |-n3------|
                 |         |          /-H
                 |          \n5------|
                 |                    \-I
                 |
                 |          /-J
                  \n2------|
                            \-K
        """
        nwk = '((((A,B)n9,C)n8,(D,E)n7)n4,((F,G)n6,(H,I)n5)n3,(J,K)n2)n1;'
        exp = """name	taxa	splits	postlevels	prelevels
n1	11	9	5	1
n4	5	4	4	2
n3	4	3	3	2
n2	2	1	2	2
n8	3	2	3	3
n7	2	1	2	3
n6	2	1	2	3
n5	2	1	2	3
J	1	0	1	3
K	1	0	1	3
n9	2	1	2	4
C	1	0	1	4
D	1	0	1	4
E	1	0	1	4
F	1	0	1	4
G	1	0	1	4
H	1	0	1	4
I	1	0	1	4
A	1	0	1	5
B	1	0	1	5
"""
        with patch('builtins.open', mock_open(read_data=nwk)):
            with patch('sys.stdout', new=StringIO()) as m:
                main()
                self.assertEqual(m.getvalue(), exp)


if __name__ == '__main__':
    main()
