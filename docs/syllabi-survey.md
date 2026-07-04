# Survey of Graduate Curricula in Applied Generative AI for the Health Sciences
*2026-07-04 09:06 PDT*

This document records the survey of graduate-level courses on
generative AI and large language models for health sciences, biomedical
informatics, and public health that informed the chapter list of
*Applied Generative AI for Health Sciences Research*. It is referenced
from the preface. The survey was conducted by structured web search in
July 2026 and is confined to courses for which a syllabus, schedule, or
official course description could be located. Epistemic labels are used
throughout: **[verified]** denotes a syllabus or schedule page read
directly; **[partial]** a confirmed course with incomplete topic
detail; **[program]** a degree or track confirmed without a single
public syllabus.

## 1. Courses located

### Detailed syllabi read

- **Harvard Medical School, Biomedical Informatics, BMI 702, Biomedical
  Artificial Intelligence** (Zitnik Lab) [verified]. Six modules over
  fourteen weeks: clinical AI; trustworthy and efficient AI (bias,
  fairness, interpretability, evaluation); graph learning; language
  modelling and LLMs; biomedical imaging; generative AI. Standalone
  ethical and legal week. Primary-literature reading list, no assigned
  textbook. <https://zitniklab.hms.harvard.edu/BMI702/syllabus/>
- **Stanford, Biomedical Data Science, BIODS 271, Foundation Models for
  Healthcare** (Chaudhari, Zou, Syeda-Mahmood) [verified]. The most
  closely aligned peer course. Covers LLM fundamentals and instruction
  tuning; agentic LLMs and AI-scientist agents; evaluation and
  hallucination detection; vision-language models (CLIP, SigLIP) and
  MedSAM segmentation; RAG and prompting; alignment and regulatory
  considerations; foundation models for electronic health records; bias
  and ethics. <https://web.stanford.edu/class/biods271/>
- **Stanford, BIODS 220, AI in Healthcare** (Yeung) [verified, 2022
  archive]. Medical imaging, EHR, multimodal transformers, genomics,
  interpretability, fairness, privacy.
  <https://web.stanford.edu/class/biods220/>
- **Stanford, CS224N, NLP with Deep Learning** (Manning, Yang)
  [verified, partial]. Transformers, pretraining, instruction
  fine-tuning, RLHF, DPO, prompting, retrieval, evaluation. Companion
  text: Jurafsky and Martin, *Speech and Language Processing*.
  <https://web.stanford.edu/class/cs224n/>
- **Columbia, Biomedical Informatics, BINF G4003, Methods I, Symbolic
  Methods** [verified]. Clinical terminologies (ICD, SNOMED-CT, MeSH,
  UMLS), ontologies, knowledge representation, guidelines, text
  processing.
  <https://www.dbmi.columbia.edu/binf-g4003-methods-i-symbolic-methods/>

### Courses confirmed with partial detail

- **MIT, 6.7930 / HST.956, Machine Learning for Healthcare** [partial].
  Now includes LLMs; long-standing coverage of causality,
  interpretability, algorithmic fairness, disease-progression
  modelling. <https://mlhcmit.github.io/>
- **Johns Hopkins Bloomberg School of Public Health, 340.611.89, Using
  Generative AI to Improve Public Health** (Klaas) [description]. The
  clearest public-health-school generative-AI course located; hands-on
  tools, core concepts, ethics and policy.
- **NUS Saw Swee Hock School of Public Health, AI for Health and
  Healthcare** [verified topics]. Foundational AI, generative AI, prompt
  engineering, RAG, and agent workflows. A public-health school teaching
  agents and RAG explicitly.
- **Harvard Chan School, BST 261, Data Science II, Deep Learning**
  [partial]. Neural networks, CNN, RNN, biomedical applications;
  pre-LLM emphasis.
- **Stanford, CS25, Transformers United** [verified]. Seminar on
  transformer frontiers including health and biology.

### Open courses

- **DeepLearning.AI and AWS, Generative AI with LLMs** (Coursera)
  [verified]. Transformer architecture, LLM lifecycle, fine-tuning,
  PEFT, RLHF, deployment. The de facto canonical LLM MOOC.
- **Google Cloud, Generative AI for Healthcare** (Coursera) [verified].
  Medical foundation models, prompt design for healthcare, multimodal
  LLMs.

### Programs without a single public syllabus

Yale Biomedical Informatics and Data Science; Penn DBEI; the UC
Berkeley and UCSF Computational Precision Health PhD; Harvard Chan
Executive Education (Responsible AI for Health Care); Oxford OxML
Health. Dedicated generative-AI graduate courses with public syllabi
could not be verified at LSHTM, Imperial, ETH Zurich, Melbourne, UCLA
Fielding, Emory Rollins, or Toronto Dalla Lana as of this survey.

## 2. Topic coverage against this book

### Competitive or ahead of peers

Retrieval-augmented generation (Chapter 4); multimodal medical AI
(Chapter 6); agents, tool use, and the Model Context Protocol (Chapter
7); evaluation (Chapter 9); safety, bias, and red-teaming (Chapter 10);
regulation and the IRB (Chapter 11). The deep-research and
evidence-synthesis material (Chapter 8) is a genuine strength: no peer
course located teaches LLM-driven systematic review as a unit.

### Present but thinner than peers, now strengthened in this revision

Reasoning and verification (Chapter 3) now treats hallucination
detection, fact-checking, and inference-time verification as concrete
named techniques. Customisation (Chapter 12) now names instruction
tuning, RLHF, DPO, and PEFT/LoRA as distinguished methods. Safety
(Chapter 10) now reaches population-scale fairness quantitatively
(subgroup metrics, net benefit).

### Public-health white space, treated here as a differentiator

Digital and computational epidemiology, disease surveillance from
unstructured text, social determinants of health via NLP, health
misinformation, and population-scale algorithmic fairness are weak
across all peer courses surveyed. These are foregrounded in this book
(Chapters 2, 6, 8, 10, 13) as its distinguishing emphasis.

## 3. Remaining gaps identified but not yet closed

The survey identifies three topics common in informatics-side peer
curricula that this book still treats lightly, recorded here as
candidates for a future edition:

1. An explicit LLM technical-foundations unit (transformer
   architecture, tokenisation, pretraining, attention). Every
   foundational peer course opens here.
2. Clinical NLP, EHR phenotyping, and clinical or administrative coding
   (ICD, SNOMED, UMLS), taught at Columbia and Stanford.
3. Causal inference with and for LLMs, central to epidemiology and
   taught at MIT.

## 4. Textbooks

No surveyed course assigns a dedicated generative-AI-for-health
textbook; the norm is primary literature (CS224N is the exception, with
Jurafsky and Martin as background). This absence is the market position
the present book occupies.

---
*Compiled from a structured web survey conducted 2026-07-04. Course
details are as located on the dates searched and are subject to change.*
