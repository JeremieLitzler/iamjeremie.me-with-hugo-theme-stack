---
title: "Can a Geekom A9 Mega with 128 GB Run Big LLMs Locally?"
description: "I dug into the Geekom A9 Mega, a mini PC with a Ryzen AI Max+ 395 and 128 GB of unified memory, and kept only the claims I could verify against primary sources."
image: 2026-11-11-geekom-a9-mega-held-by-robot-arms-in-a-dark-scene.jpg
imageAlt: A geekom a9 mega held by robot arms in a dark scene
date: 2026-11-11
categories:
  - Artificial Intelligence
tags:
  - Hardware
  - AMD
  - Local LLM
---

A 4,000 euro mini PC that fits in a 170 x 170 mm box and promises to run language models that some strong consumer graphic card can hold. That is the pitch of the Geekom A9 Mega in its 128 GB configuration, and it made me curious enough to stop and check what is actually proven.

So I researched it. My rule was simple: I only keep a claim if it is backed by a primary source, meaning Geekom’s own page, AMD’s product page and blogs, and the documentation of the tools involved.

I made one exception. Valérian de Thézan de Gaussan owns a Framework Desktop with the same Ryzen AI Max+ 395 and 128 GB of memory, and published benchmarks originally in November 2025 and refreshed it in October 2026. It is not a Geekom, so the cooling and power limits differ, but it is the closest thing to real measurements on this chip that I found. I flag every number that comes from that machine below.

## What Is Inside the Box

The 128 GB version of the A9 Mega is built around the Ryzen AI Max+ 395. According to AMD, that is 16 Zen 5 cores and 32 threads, a 3 GHz base clock and up to 5.1 GHz boost, 64 MB of L3 cache, and a configurable TDP between 45 and 120 W. The integrated GPU is a Radeon 8060S with 40 RDNA 3.5 compute units running up to 2900 MHz.

The memory is a 256-bit LPDDR5x interface, up to LPDDR5x-8000, soldered on the board. Geekom’s FAQ gives a theoretical bandwidth of 256 GB/s, which matches the math: 256 bits divided by 8, times 8000 MT/s. It is a theoretical peak, not something anyone has measured on this chassis.

Geekom lists a system TDP of up to 154 W with a 330 W adapter, while its FAQ mentions about 120 W under sustained load. What it does not say is which power limits are configured in the BIOS.

## Memory Seems to Be the Real Selling Point

What’s interesting about this machine comes from the unified memory. The CPU and the GPU share the same 128 GB, so the GPU can reach into a pool far larger than what a typical discrete card offers.

How much of it the GPU can really use depends on the platform. Geekom’s FAQ says up to 96 GB can be allocated as Variable Graphics Memory on the 128 GB configuration, on Windows. AMD’s blog from July 2025 backs that number for a Ryzen AI Max+ 395 with 128 GB, with the Adrenalin Edition 25.8.1 WHQL drivers. But that is a driver capability, and the blog does not say whether a given vendor’s BIOS exposes it.

On Linux, AMD’s ROCm blog tells a different story. On its 128 GB test system, the GPU-accessible portion was 64 GB by default, “configurable” to 64 GB or more depending on “system vendor and BIOS support”. No maximum is given.

Valérian’s Framework Desktop shows how far “or more” can go. In the October 2026 follow-up, running llama.cpp with Vulkan on Linux (Mesa RADV driver), the driver exposed 111.56 GiB to Vulkan, with about 109.84 GiB free at startup. Valérian explicitly corrects an earlier assumption of a 96 GB budget: no strict 96 GB cap was enforced on that machine.

So the honest answer to “how much can the GPU use?” is: 96 GB on Windows according to Geekom and AMD, 64 GB by default on Linux according to AMD’s ROCm blog, over 110 GiB through Vulkan on one Framework Desktop under Linux, and I would verify it on the actual Geekom unit, because it depends on the BIOS.

## Which Models Fit

Geekom’s page says the machine handles models “up to 180 billion parameters”. Its own FAQ is far more conservative: 70B models at 4-bit, and MoE models around 120B. The two statements conflict, and the FAQ feels the more plausible one.

The only measured numbers I found come from AMD’s ROCm blog. They were taken on a single test system, not on a Geekom, with 128 GB of memory, 64 GB given to the GPU, Q4_K_M quantization, and Ollama on ROCm 7.2.1 under Ubuntu 24.04:

| Model                   | Size    | Placement       | Generation speed                             |
| ----------------------- | ------- | --------------- | -------------------------------------------- |
| Qwen3.5 9B (dense)      | 6.2 GB  | 100% GPU        | 29.84 tok/s                                  |
| Qwen3.5 35B-A3B (MoE)   | 20.5 GB | 100% GPU        | 42.04 tok/s (154.52 tok/s prompt processing) |
| Qwen3.5 122B-A10B (MoE) | 76 GB   | 61% GPU/39% CPU | 8.59 tok/s                                   |

The last line deserves attention. The 122B model exceeded the 64 GB allocation, so it was split automatically between GPU and CPU, and the speed dropped to 8.59 tokens per second. AMD notes that a larger allocation could offload more layers, but it provides no measurement for that case.

On Windows with LM Studio, AMD’s slides show the memory footprint of 4-bit models: 68 GB for Mistral Large 123B, 66 GB for Llama 4 Scout 109B, 18 GB for Qwen3 30B-A3B and 17 GB for Gemma 3 27B. Context length matters a lot too. Llama 4 Scout takes 66 GB at the default 4096 tokens of context, but 92 GB at 256,000 tokens with Flash Attention on and a Q8 KV cache. AMD also claims “up to 15 tokens per second” for that model, with no test conditions, so I treat it as a vendor claim.

Valérian’s benchmarks give a much wider picture. They use llama.cpp with the Vulkan backend, all layers on the GPU, a 512-token prompt and 128 generated tokens. The pattern is clear: dense models slow down with size, and mixture-of-experts (MoE) models break that rule.

On the dense side, Llama 3.3 70B at 4-bit (about 40 GB) decoded at 5.05 tokens per second, and Mistral Large 123B at 4-bit (68 GB) at only 2.97. A 27B to 31B dense model from 2026, like Qwen3.8 27B or Gemma 4 31B, sits around 11 to 13 tokens per second at 4-bit and drops to 6.5 to 7.5 at 8-bit. Lower precision means fewer bytes to read per token, so decoding gets faster.

On the MoE side, gpt-oss-120b in MXFP4 (59 GB) reached 54 tokens per second in decode and 500 in prompt processing. Mistral Small 4 119B, with about 6.5B active parameters, reached 32.72 tokens per second at 4-bit (68.7 GiB) and 29.83 at 5-bit (83 GiB). Llama 4 Scout at 4-bit decoded at 20.2 tokens per second, above AMD’s own “up to 15” claim, though on a different backend and OS. Only the active parameters are read for each token, which explains why a 120B MoE model can run ten times faster than a 70B dense one.

From these allocations, I draw a rule of thumb. A 4-bit model of about 70 to 76 GB fits in memory, but with a 64 GB GPU allocation, part of it runs on the CPU. With the 96 GB setting that Geekom advertises, models in the 70 to 90 GB range should fit entirely on the GPU. **I want to be clear that this is an inference from the stated numbers, not a measured result on the Geekom unit.** The Framework Desktop supports it, though: Valérian ran Mixtral 8x22B (79.7 GB) and GLM-5.3-Flash at a 1-bit quantization (86.7 GiB, 19 tokens per second) fully on the GPU.

Two caveats apply to all of Valérian’s numbers. First, they are short-context runs, so they say nothing about speed with a 32,000-token or 128,000-token prompt, which is what a coding agent would send. Second, output quality was not evaluated, and a 1-bit quantization fitting in memory does not mean it answers well.

## What About the NPU?

The NPU is advertised at up to 50 TOPS by AMD, for a platform total of up to 126 TOPS. Geekom’s page is inconsistent here, quoting 118 TOPS in the Ryzen AI Max+ 388 section and 126 TOPS in the 395 section and FAQ. For the 395, 126 matches AMD.

More important for LLM work, none of the sources I reviewed say that the large-model paths (llama.cpp with Vulkan or HIP, Ollama on ROCm, LM Studio) run on the NPU. In AMD’s ROCm blog, the models run on the GPU and the CPU. I would not count on the NPU to contribute to any token-per-second figure.

## Marketing Claims I Could Not Verify

Geekom makes several bold statements, and none of them comes with a methodology:

- “2.2x faster inference on LM Studio than RTX 4090 at just 13% power”.
- An iGPU “comparable to an RTX 4070 Laptop in some scenarios”.
- Game frame rates of “100+ FPS” and “200+ FPS”, with no resolution, settings or titles.
- “72% improved cooling” and “ultra-quiet at 32 dB”, with no baseline and no test conditions.
- A 120-hour thermal test from -20 C to 55 C and 330 hours of load testing, with no results.

The page also contradicts itself on TOPS and on the maximum model size. I am not saying the claims are false. I am saying that nothing I read lets me call them true.

## What Nobody Has Published

Here is what I could not find in any primary source:

- Cinebench, Geekbench or compile-time scores for this chassis.
- Measured tokens per second on a Geekom A9 Mega, for any model. Same-chip numbers exist from the Framework Desktop, but it doesn’t Geekom A9 Mega would mean similar outcome.
- Measured speeds with long contexts, on any Ryzen AI Max+ 395 machine.
- The memory bandwidth actually delivered in clear real-life scenarios, as opposed to the theoretical 256 GB/s.
- Sustained power limits per mode, fan noise under load, and clock speeds over time.
- The exact LPDDR5X speed shipped in this model. AMD only gives a maximum of 8000.
- Whether this machine’s BIOS exposes a GPU allocation setting and its maximum.
- Whether gfx1151, the Radeon 8060S target, is officially supported by every runtime version. The llama.cpp build documentation describes a Vulkan backend and a HIP backend, but does not name gfx1151.

## Price

Geekom France lists two configurations: 2,499 euros for the 64 GB version with the Ryzen AI Max+ 388, and 3,999 euros for the 128 GB version with the Ryzen AI Max+ 395. It’s not the _250 euros discount of November 2026_ that will make it easier to swallow the bill…

## Sources

- [Geekom A9 Mega mini PC (France)](https://www.geekom.fr/geekom-a9-mega-mini-pc/)
- [AMD Ryzen AI Max+ 395 product page](https://www.amd.com/en/products/processors/laptop/ryzen/ai-300-series/amd-ryzen-ai-max-plus-395.html)
- [AMD: AI Inference on AMD Ryzen AI Max Processor (ROCm Blogs)](https://rocm.blogs.amd.com/artificial-intelligence/ryzen-uma-llm/README.html)
- [AMD: Ryzen AI Max+ upgraded, run up to 128 billion parameter LLMs on Windows with LM Studio](https://www.amd.com/en/blogs/2025/amd-ryzen-ai-max-upgraded-run-up-to-128-billion-parameter-llms-lm-studio.html)
- [llama.cpp build documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)
- [LM Studio system requirements](https://lmstudio.ai/docs/app/system-requirements)
- [Valérian de Thézan de Gaussan: LLM on the AMD AI Max 395+, what can it run locally? (November 2025)](https://valerian.dtdg.fr/blog/2025/amd-strix-halo-ai-395-llm-benchmark/)
- [Valérian de Thézan de Gaussan: Local AI is not ready yet (November 2025)](https://valerian.dtdg.fr/blog/2025/local-ai-not-ready-yet/)
- [Valérian de Thézan de Gaussan: AMD Strix Halo LLM benchmark follow-up (October 2026)](https://valerian.dtdg.fr/blog/2026/amd-strix-halo-llm-benchmark-follow-up/)

## Conclusion

The 128 GB Geekom A9 Mega is a credible choice if your main goal is running large quantized LLMs locally, but I would not buy it on Geekom’s performance claims alone.

Memory is the real advantage. With 128 GB of unified LPDDR5X and up to 96 GB allocatable to the GPU on Windows, it could host 70B-class dense models and 100B+ MoE models that exceed any consumer discrete GPU. But speed is bounded by bandwidth.

The 256 GB/s theoretical peak is shared with the CPU, and AMD’s own example shows 8.59 tokens per second for a 76 GB MoE model that spilled partly onto the CPU.

The Framework Desktop numbers point to the same lesson: MoE models with only 5 to 7B active parameters, like gpt-oss-120b and Mistral Small 4, are the sweet spot, at 30 to 54 tokens per second, while dense models of 70B and more crawl at 3 to 5 tokens per second.

If you use a coding assistant like Claude Code every day, that is a big difference, so expect modest speeds on the largest models. I am not trying to reach the performance of frontier cloud models. I am simply saying that the experience will be very different in terms of speed.

The memory is also soldered, so the 128 GB decision cannot be corrected later. Before relying on the machine, I would test the GPU allocation I can really reach (64 GB or 96 GB), the tokens per second on my own target models with Vulkan and ROCm, the sustained power, fan noise and clocks over a 30-minute load, the real Ethernet port speed, and the final price.

Valérian, who owns this class of machine, is blunt about it: local AI on a consumer desktop “is not a replacement for frontier intelligence today”, and cloud flagships are cheap because of subsidies and strategic pricing, which makes local hardware “economically irrational today”.

Its value lies elsewhere: narrow workflows like field extraction, classification or internal assistants with validated outputs, and data sovereignty for organizations that cannot send sensitive data to external servers. If that is your use case, the machine makes sense. If you hope to replace your cloud subscription, it does not, yet.

But can you afford 3,999 euros to _test_?

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Image from the product page of the mini PC Geekom (`https://www.geekom.fr/geekom-a9-mega-mini-pc/`).
