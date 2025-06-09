# A Divide-and-Conquer Strategy for IPs

This repository contains the Matlab implementation of the algorithm framework for Adaptive Batch-ParEGO in the research paper: A Divide-and-Conquer Strategy for Integer Programming Problems.


## Dataset
Dataset of the proposed method can be found [here](https://drive.google.com/drive/folders/15MoqpG_FaMdh3ALYhfIvz34nszzy8o9Y?dmr=1&ec=wgc-drive-hero-goto).

## Benchmark
Benchmarks used in this paper includes [the Maximum Independent Set (MIS)](https://dx.doi.org/https://doi.org/10.1016/0196-6774(86)90032-5), 
 [Minimum Vertex Cover (MVC)](https://hochbaum.ieor.berkeley.edu/html/pub/Approx-Alg-book-ch3.pdf), [Set Cover (SC)](https://dl.acm.org/doi/10.1145/780542.780558) and [Combinatorial Auction (CA)](https://www.cramton.umd.edu/papers2005-2009/cramton-shoham-steinberg-combinatorial-auctions-introduction.pdf).

## Baselines
To benchmark the performance of our approach, we compare it against several state-of-the-art solvers [Gurobi](https://www.dcc.fc.up.pt/~jpp/seminars/azores/gurobi-intro.pdf) and [SCIP](https://dx.doi.org/https://doi.org/10.1007/s12532-008-0001-1), and advanced Large Neighborhood Search (LNS) variants, including [Random-LNS](https://papers.nips.cc/paper/2020/hash/e769e03a9d329b2e864b4bf4ff54ff39-Abstract.html), [Least-Integral (LI)](https://homes.di.unimi.it/righini/Didattica/ComplementiRicercaOperativa/MaterialeCRO/2000%20-%20Mitchell%20-%20branch-and-cut.pdf), [Least-Integral (LI)](https://homes.di.unimi.it/righini/Didattica/ComplementiRicercaOperativa/MaterialeCRO/2000%20-%20Mitchell%20-%20branch-and-cut.pdf), [Most-Integral (MI)](https://homes.di.unimi.it/righini/Didattica/ComplementiRicercaOperativa/MaterialeCRO/2000%20-%20Mitchell%20-%20branch-and-cut.pdf), [Relaxation Induced Neighborhood Search (RINS)](https://dx.doi.org/https://doi.org/10.1007/s10107-004-0510-0).

## References
<a name="1">
</a>

[1] J. M. Robson, [Algorithms for maximum independent sets, Journal of Algorithms](J. M. Robson, Algorithms for maximum independent sets, Journal of Algorithms, 7 (1986), 425–440.), 7 (1986), 425–440.

<a name="2">
</a>

[2] D. S. Hochbaum, [Approximating covering and packing problems: set cover, vertex cover, independent set, and related problems, Approximation Algorithms for NP-Hard Problems](https://hochbaum.ieor.berkeley.edu/html/pub/Approx-Alg-book-ch3.pdf), (1997), 94–143. PWS Publishing.

<a name="3">
</a>

[3] N. Alon, B. Awerbuch and Y. Azar, [The online set cover problem](https://dl.acm.org/doi/10.1145/780542.780558), in Proceedings of the Thirty-Fifth Annual ACM Symposium on Theory of Computing, (2003), 100–105.


<a name="4">
</a>

[4] P. Cramton, Y. Shoham, and R. Steinberg, [Introduction to combinatorial auctions, Combinatorial Auctions](https://www.cramton.umd.edu/papers2005-2009/cramton-shoham-steinberg-combinatorial-auctions-introduction.pdf), 1–14, MIT Press Cambridge, MA, 2006.


<a name="5">
</a>

[5] J. P. Pedroso, [Optimization with Gurobi and Python](https://www.dcc.fc.up.pt/~jpp/seminars/azores/gurobi-intro.pdf), INESC Porto and Universidade do Porto, Porto, Portugal, 1 (2011).


<a name="6">
</a>

[6] T. Achterberg, [SCIP: Solving constraint integer programs](https://dx.doi.org/https://doi.org/10.1007/s12532-008-0001-1), Mathematical Programming Computation, 1 (2009), 1–41. 


<a name="7">
</a>

[7] J. Song, Y. Yue and B. Dilkina, [A general large neighborhood search framework for solving integer linear programs](https://papers.nips.cc/paper/2020/hash/e769e03a9d329b2e864b4bf4ff54ff39-Abstract.html), Advances in Neural Information Processing Systems, 33 (2020), 20012–20023.


<a name="8">
</a>

[8] V. Nair, M. Alizadeh et al., [Neural large neighborhood search](https://homes.di.unimi.it/righini/Didattica/ComplementiRicercaOperativa/MaterialeCRO/2000%20-%20Mitchell%20-%20branch-and-cut.pdf), in Learning Meets Combinatorial Algorithms at NeurIPS, (2020).

<a name="9">
</a>

[9] E. Danna, E. Rothberg and C. Le Pape, [Exploring relaxation induced neighbor- hoods to improve MIP solutions](https://dx.doi.org/https://doi.org/10.1007/s10107-004-0510-0), Mathematical Programming, 102 (2005), 71–90.

