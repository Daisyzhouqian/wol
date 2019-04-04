# ASTRAL tree

The tree was built using the gene tree summary tool: [ASTRAL](https://github.com/smirarab/ASTRAL).

Go to [GitHub directory](https://github.com/biocore/wol/tree/master/data/trees/astral).

### Branch supports

The internal branch of an ASTRAL tree typically receive three support statistics:

1. `EN` (effective number of genes): number of gene trees that contain some quartets around that branch.
2. `QT` (quartet score) ([Sayyari and Mirarab, 2016](https://academic.oup.com/mbe/article/33/7/1654/2579300)): Proportion of the quartets in the gene trees that support this branch.
3. `LPP` (local posterior probability): the probability this branch is the true branch given the set of gene trees (computed based on the quartet score and assuming ILS).

We recommend using **LPP** as a general measure of the confidence of a branch. Note that this metric should not be confused with the posterior probability calculated using the Bayesian method.

We also provide trees in which branches with EN <= 5 or LPP <= 0.5 (abbr.: `e5p50`) are **collapsed**. We recommend using the collapsed tree, which has higher confidence in the accuracy of topology, for downstream applications.


### Branch lengths

In an original ASTRAL tree, the branch lengths are in **coalescence units**. The trees under the `branch_length` directory have the same topology (and node IDs) to the original tree, but with branch lengths re-estimated using ML, based on three concatenated alignments:

- `cons`: Up to 100 most conserved sites per gene, as selected using the Trident algorithm.
- `rand`: 100 sites randomly selected from sites with less than 50% gaps.
- `rpls`: 30 ribosomal proteins instead of the 381 global markers. We do not recommend using this tree as a reference.

The resulting branch lengths represent the **expected number of amino acid substitutions per site**, which is the conventional metric used in most phylogenetic trees, including the CONCAT trees.

We also provide **ultrametric** trees (i.e., all tips have equal distance to root), which may be useful in some applications. They were generated using [**r8s**](https://academic.oup.com/bioinformatics/article/19/2/301/372781).
