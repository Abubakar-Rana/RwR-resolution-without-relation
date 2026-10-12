# LLaVA-UHD: An LMM Perceiving Any Aspect Ratio and High-Resolution Images

- **Authors**: Ronghao Xu, Yuan Yao, Zixuan Guo, Junbo Cui, Zanlin Ni, Chunjiang Ge, Tat-Seng Chua, Zhiyuan Liu, Maosong Sun, Gao Huang
- **Year**: 2024
- **Venue**: ECCV 2024
- **arXiv**: 2403.11703
- **URL**: https://arxiv.org/abs/2403.11703
- **BibTeX Key**: `xu2024llavauhd`

## Abstract
Standard Large Multimodal Models (LMMs) resize images to fixed square resolutions, causing severe geometric distortion and blur on non-square or high-resolution inputs. We present LLaVA-UHD, an efficient LMM architecture capable of perceiving any aspect ratio and high-resolution images. LLaVA-UHD adopts a dynamic modular division strategy that partitions an image into variable numbers of native-aspect-ratio slices without padding or distortion. A spatial compression module reduces slice tokens by 4x using spatial resampling. Crucially, a shared low-resolution overview is concatenated to maintain global scene structure. Extensive benchmarks demonstrate superior performance and 3x higher throughput compared to standard high-resolution baselines.

## Key Extracted Contributions
1. Preserving native aspect ratios without distortion is critical for fine-grained spatial recognition.
2. Spatial resampling ($2\times 2$ pooling) preserves 94% of fine detail while cutting visual token counts by 75%.
3. Concatenating an overview thumbnail with local crops partially preserves global context.
