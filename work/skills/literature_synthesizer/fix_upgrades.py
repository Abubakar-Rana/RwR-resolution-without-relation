import re

with open('work/skills/literature_synthesizer/run_pedagogical_upgrades.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the raw string syntax warning
text = text.replace(r'$\tau \in [0.1, 0.9]$', 'tau in [0.1, 0.9]')

# Replace doesnt extraction with .get
text = text.replace('p["adds_vs_doesnt"]["doesnt"]', 'p["adds_vs_doesnt"].get("doesnt", [])')

# Fix Paper 10
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "The seminal framework proving visual marker overlays outperform numerical coordinate tokenization.",
                "Enables zero-shot spatial referencing on any off-the-shelf vision-language model.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "The seminal framework proving visual marker overlays outperform numerical coordinate tokenization.",
                "Enables zero-shot spatial referencing on any off-the-shelf vision-language model.",
            ],
            "doesnt": [
                "Relies on external object detectors or SAM segmentation models to generate mask proposals.",
                "Evaluates on natural consumer photos rather than ultra-high-resolution aerial satellite scenes.",
            ],
        },'''
)

# Fix Paper 11
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "The industry-standard token compression technique (Pixel Shuffle) for high-resolution VLMs.",
                "Proven scaling architecture capable of handling multi-tile inputs within memory bounds.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "The industry-standard token compression technique (Pixel Shuffle) for high-resolution VLMs.",
                "Proven scaling architecture capable of handling multi-tile inputs within memory bounds.",
            ],
            "doesnt": [
                "Processes all crops unconditionally, resulting in high latency when applied to full 8K scenes without selective pruning.",
                "Does not dynamically route queries based on problem difficulty.",
            ],
        },'''
)

# Fix Paper 12
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "Rigorous proof that excessive visual tokens actively harm multimodal reasoning.",
                "Demonstrates that aggressive pruning of background tokens improves both speed and accuracy.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "Rigorous proof that excessive visual tokens actively harm multimodal reasoning.",
                "Demonstrates that aggressive pruning of background tokens improves both speed and accuracy.",
            ],
            "doesnt": [
                "Focuses on within-crop token pruning rather than selecting which macro-crops to process across gigapixel images.",
                "Does not evaluate on aerial remote sensing benchmarks.",
            ],
        },'''
)

# Fix Paper 13
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "Practical serving optimization that eliminates padding overhead in variable-crop high-resolution VLMs.",
                "Enables high-throughput concurrent batch evaluation on benchmarks like XLRS-Bench.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "Practical serving optimization that eliminates padding overhead in variable-crop high-resolution VLMs.",
                "Enables high-throughput concurrent batch evaluation on benchmarks like XLRS-Bench.",
            ],
            "doesnt": [
                "Focuses purely on inference throughput and memory packing; does not solve the spatial relational accuracy tradeoff.",
                "Does not provide an active crop selection or grounding mechanism.",
            ],
        },'''
)

# Fix Paper 14
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "The core mathematical framework for uncertainty-guided early-exit routing in multimodal models.",
                "Proves that unconditional high-resolution processing on all queries is wasteful and unnecessary.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "The core mathematical framework for uncertainty-guided early-exit routing in multimodal models.",
                "Proves that unconditional high-resolution processing on all queries is wasteful and unnecessary.",
            ],
            "doesnt": [
                "Cascades between different foundation models rather than cascading between low-res overview and high-res anchored crops.",
                "Does not address the unique geometric distortions of satellite imagery.",
            ],
        },'''
)

# Fix Paper 15
text = text.replace(
'''        "adds_vs_doesnt": {
            "adds": [
                "The definitive mathematical formulation for logit-margin routing ($M = y_1 - y_2 < \\tau$).",
                "Proven benchmarking methodology from LMSYS for evaluating cascaded model performance.",
            ],
        },''',
'''        "adds_vs_doesnt": {
            "adds": [
                "The definitive mathematical formulation for logit-margin routing ($M = y_1 - y_2 < \\tau$).",
                "Proven benchmarking methodology from LMSYS for evaluating cascaded model performance.",
            ],
            "doesnt": [
                "Designed for text-only LLMs in chatbot settings; does not directly handle multi-crop visual token routing.",
                "Does not integrate visual grounding or object detection in its routing signals.",
            ],
        },'''
)

with open('work/skills/literature_synthesizer/run_pedagogical_upgrades.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied cleanly.")
