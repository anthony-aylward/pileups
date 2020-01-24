# betabernsum
Sums of beta-bernoulli variables

## Installation

For Python:
```sh
pip3 install betabernsum
```
or
```
pip3 install --user betabernsum
```

For R:
```r
library(devtools)
install_github("anthony-aylward/betabernsum")
```


## Examples

In Python:
```python
from betabernsum import bbs_pmf, bbs_cdf, bbs_test
help(bbs_pmf)
help(bbs_cdf)
help(bbs_test)
bbs_pmf(5, [30, 12], [4, 5], [6, 5], independent=False)
bbs_cdf(5, [30, 12], [4, 5], [6, 5], independent=False)
bbs_test(5, [30, 12], [4, 5], [6, 5], independent=False)
```

In R:
```r
library(betabernsum)
help(dbbs)
help(pbbs)
help(bbs_test)
dbbs(5, c(30, 12), shape1 = c(4, 5), shape2 = c(6, 5), independent = FALSE)
pbbs(5, c(30, 12), shape1 = c(4, 5), shape2 = c(6, 5), independent = FALSE)
bbs_test(5, c(30, 12), shape1 = c(4, 5), shape2 = c(6, 5), independent = FALSE)
```