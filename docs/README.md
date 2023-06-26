# Using OpenAI embeddings for creation of LLM with custom corpus

# Introduction
LLMs like ChatGPT can be asked to perform a specific task and produce output that is a **likely continuation** of the input string. The generation of the output of the associated neural network is dependent upon its training data. OpenAI uses a large amount of training data from sources all over the internet. Some specific sources, though, will necessarily have to be skipped, since the amount of data on the internet is too large to be fed completely into the LLM. This "lack" of input data has a serious impact on the answers that the LLM generates. LLMs can "hallucinate", which is a term describing the tendency for LLMs to generate answers that are factually wrong, due to lack of training data on a specific problem.
Thus, creating a custom corpus, also known as a context for the LLM to fall back on is important, if one wants to avoid hallucinations.
The goal of this project will be to create a LLM with a custom corpus containing information about the University of Greifswald. (e.g. research of individual professors, study regulations, etc.)

# Acquiring data

