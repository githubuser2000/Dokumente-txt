#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Similarity & Fuzzy Hashing Checks
Author: OpenAI ChatGPT
Purpose: Compute fuzzy hashes, similarity metrics, and embeddings
for large text and compare versions robustly.
"""

# Install required packages first if not already installed:
# pip install ssdeep tlsh simhash sentence-transformers scikit-learn numpy

import ssdeep
import tlsh
from simhash import Simhash
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

# =========================
# 1. Prepare Texts
# =========================
# Replace these with your actual text versions
text_version_A = """
fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin timeMal byDurch oneEine byDurch theDie otherAndere soDaher onlyNur positivePositive notNoch yetNicht negativeNegative wholeGanze numbersZahlen valuesWerte hereHier yetBereits soDaher limitedBegrenzte rationalRationale numbersZahlen asAls mathematicalMathematische setMenge forZur currencyWährung outBestehend ofAus numbersZahlen butAber notNicht asWie nowJetzt butAber improvedVerbesserte economyWirtschaft systemSystem andUnd alsoAuch orderOrdnung asGenau wellAuch
"""
text_version_B = """
fractionsGebrochene ofZahlen numbersWerte twoZwei wholeGanze natürlicheNatural numbersZahlen dividedGeteilt byDurch eachJeweils oneEin timeMal byDurch oneEine byDurch theDie otherAndere soDaher onlyNur positivePositive notNoch yetNicht negativeNegative wholeGanze numbersZahlen valuesWerte hereHier yetBereits soDaher limitedBegrenzte rationalRationale numbersZahlen asAls mathematicalMathematische setMenge forZur currencyWährung outBestehend ofAus numbersZahlen butAber notNicht asWie nowJetzt butAber improvedVerbesserte economyWirtschaft systemSystem andUnd alsoAuch orderOrdnung asGenau wellAuch
"""

# Optional: pre-cleaning (remove punctuation, normalize whitespace)
import re
def clean_text(text):
    text = re.sub(r'[.,]', '', text)       # remove dots and commas
    text = re.sub(r'\s+', ' ', text)       # multiple spaces → single space
    return text.strip()

text_A_clean = clean_text(text_version_A)
text_B_clean = clean_text(text_version_B)

# =========================
# 2. Fuzzy Hashing
# =========================
print("=== Fuzzy Hashing ===")
ssdeep_A = ssdeep.hash(text_A_clean)
ssdeep_B = ssdeep.hash(text_B_clean)
ssdeep_similarity = ssdeep.compare(ssdeep_A, ssdeep_B)
print("ssdeep A:", ssdeep_A)
print("ssdeep B:", ssdeep_B)
print("ssdeep similarity (%):", ssdeep_similarity)

# TLSH
tlsh_A = tlsh.hash(text_A_clean.encode())
tlsh_B = tlsh.hash(text_B_clean.encode())
# TLSH similarity (approximate)
try:
    tlsh_similarity = tlsh.diff(tlsh_A, tlsh_B)
except Exception:
    tlsh_similarity = "N/A"
print("TLSH A:", tlsh_A)
print("TLSH B:", tlsh_B)
print("TLSH difference (smaller=more similar):", tlsh_similarity)

# sdhash requires command line tool, cannot run directly here
print("sdhash: Use command line tool 'sdhash' to compute hash")

# =========================
# 3. SimHash / MinHash
# =========================
print("\n=== SimHash ===")
simhash_A = Simhash(text_A_clean)
simhash_B = Simhash(text_B_clean)
hamming_distance = simhash_A.distance(simhash_B)
simhash_similarity = 1 - hamming_distance / max(len(bin(simhash_A.value)), len(bin(simhash_B.value)))
print("SimHash similarity (~0-1):", simhash_similarity)

# =========================
# 4. Cosine Similarity / Jaccard
# =========================
print("\n=== Cosine & Jaccard Similarity ===")
vectorizer = CountVectorizer().fit([text_A_clean, text_B_clean])
vectors = vectorizer.transform([text_A_clean, text_B_clean])
cos_sim = cosine_similarity(vectors)[0,1]
print("Cosine similarity:", cos_sim)

# Jaccard Index (set of tokens)
tokens_A = set(text_A_clean.split())
tokens_B = set(text_B_clean.split())
jaccard_index = len(tokens_A & tokens_B) / len(tokens_A | tokens_B)
print("Jaccard index:", jaccard_index)

# =========================
# 5. Embedding Checks
# =========================
print("\n=== Embedding Cosine Similarity ===")
model = SentenceTransformer('all-MiniLM-L6-v2')
emb_A = model.encode([text_A_clean])
emb_B = model.encode([text_B_clean])
emb_cos_sim = cosine_similarity(emb_A, emb_B)[0,0]
print("Embedding cosine similarity:", emb_cos_sim)

