# **Subject:** A9 Mega (128 GB) for local LLMs: what I could verify, and what real users could show

Hello Geekom team,

I write a tech blog, and I recently spent a few hours researching the A9 Mega in its 128 GB configuration with the Ryzen AI Max+ 395. A mini PC that can hold 70B-class and 100B+ MoE models locally is an exciting idea, and I wanted to see how much of it I could confirm from primary sources.

Here is the result: https://iamjeremie.me/post/2026-11/can-a-geekom-a9-mega-with-128-gb-really-run-big-llms-locally/

The short version: the hardware looks promising. 128 GB of unified memory and up to 96 GB available to the GPU on Windows put it in a class of its own for local LLMs. Same-chip benchmarks from a Framework Desktop owner also show strong results with MoE models.

However, I couldn’t find answers to a few questions specific to the A9 Mega:

- Measured tokens per second on the A9 Mega itself, for any model, and with long contexts (what a coding assistant actually sends).
- Whether the BIOS exposes a GPU memory allocation setting, and its maximum, especially on Linux.
- Sustained power limits, fan noise and clock speeds over a long load.
- The exact LPDDR5X speed shipped in this model.

I also couldn’t find the test conditions behind some of the claims on the product page, such as the “2.2x faster inference on LM Studio than RTX 4090” and “models up to 180 billion parameters”. Your FAQ mentions 70B models at 4-bit and MoE models around 120B, which seems more realistic. I’m sure there is work behind these figures, and publishing the methodology would make them much more convincing.

At 3,999 euros, I think buyers would find long-term reviews from real users the most useful thing of all: a few months of daily use, with published numbers on real workloads. That would turn a promising spec sheet into a confident purchase.

Thanks for building an interesting machine, and I’d be happy to update the article if you can share any of these details or maybe propose a partnership.

Best regards,
Jérémie Litzler
https://iamjeremie.me
