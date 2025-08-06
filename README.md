# AVILA: Alt-text via Vision-Language AI

## Beyond "This Image May Contain..."

This project explores uses of cutting-edge AI vision-language models (VLMs) to generate "alt text" image descriptions for digital collections at scale, as well as further potential applications of such technologies, including providing free-text “evocative” search in multiple languages, object detection, and other methods for improving discovery within image collections.

*Peter Broadwell, Manager of AI Modeling & Inference, Research Data Services, Stanford University Libraries
Lindsay King, Head Librarian, Art and Architecture Library, Stanford University Libraries*

## Capabilities of VLMs

Some vision-language models can generate image captions based not only on the visual contents of the images but also through "conditioning" via accompanying free-text descriptions of the images and specific instructions regarding desired aspects of the captions. These instructions are also known as "prompts" - a concept that should be familiar to anyone who has conversed with a large language model chatbot. This raises two promising possibilities:

1. **Minimal to no fine-tuning needed:** AI models are "taught" how to complete tasks like image captioning by showing them many examples of the task being completed successfully. But models that already have undergone quite a lot of such foundational instruction (often referred to as "pre-training") may need further "fine-tuning" on specific examples to gain facility with the task in a certain domain; e.g., a model that can generate good long-form captions may need further fine-tuning to generate concise alt text. Fine-tuning, however, can be a time-consuming and computing-intensive task, and sufficient training examples may not be readily available in some specialized domains. A vision-language model that responds properly to instructions provided via the text prompt may not need such expensive fine-tuning.
2. **Outputs can be conditioned on context at the per-item level:** Because some vision-language AI models can "condition" their resulting image descriptions based on a different text prompt for each image, it is possible to incorporate any available metadata, however partial, when generating alt text for an image, and perhaps even text that is proximate on the page to where the image is to appear. 

### The experiments

Potential alt-text descriptions were generated for significant portions of several digital image collections covering a range of subjects and formats. The following pages display the results of using [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL), a powerful vision-language model, to produce both "unprompted" alt-text image descriptions solely on the basis of a "system" prompt asking it to describe the image (🤖), and descriptions that are additionally "conditioned" on a "user" prompt containing available human-provided metadata fields (🗃) and/or natural-language image descriptions (🧑‍🏫).

* [Images from the Douglas Menuez Photography Collection documenting the rise of Silicon Valley](https://web.stanford.edu/~pmb/cni2025/menuez_Qwen2.5-VL-7B-Instruct.html) (an [exhibit](https://exhibits.stanford.edu/menuez) about the collection)
* [Images from the Library of Congress's public domain collection of historical Japanese art](https://web.stanford.edu/~pmb/cni2025/japanese_loc_Qwen2.5-VL-7B-Instruct.html)