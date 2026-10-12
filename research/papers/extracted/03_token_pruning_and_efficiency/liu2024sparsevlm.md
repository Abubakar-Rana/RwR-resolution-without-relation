# SparseVLM: Visual Token Sparsification for Efficient Multimodal LLMs

- **Authors**: Yuan Liu, Chengyuan Wang, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2410.04417
- **URL**: https://arxiv.org/abs/2410.04417
- **BibTeX Key**: `liu2024sparsevlm`

## Abstract
The quadratic complexity of self-attention in large language models imposes severe latency bottlenecks when processing high-resolution visual inputs. We introduce SparseVLM, a framework that dynamically sparsifies visual tokens prior to LLM injection. SparseVLM employs a query-guided gating network to evaluate semantic relevance and clusters redundant background tokens using spatial feature similarity. Evaluated on multiple visual QA benchmarks, SparseVLM retains 99.2% of baseline accuracy while reducing visual token count by 75% and cutting end-to-end memory usage by 60%.

## Key Extracted Contributions
1. Sparsifying tokens before the LLM saves KV-cache memory and attention compute throughout all layers.
2. Clustering spatially adjacent similar tokens outperforms blind token dropping.
