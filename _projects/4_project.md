---
layout: page
title: 얼을 담아 (Ureul Dama)
description: Generating snapshot-style images with Korean landmarks as backgrounds
img: /assets/img/carat_ai_goal.jpg
importance: 3
category: work
---

> **Note:** Some content may be in Korean. Please be aware when reviewing the details below.

## Project Overview
This project was a university-industry collaboration between the academic club YBIGTA and Carat AI, a company specializing in image generation services. Our goal was to leverage advanced generative AI to create more engaging and realistic snapshot-style images set against iconic Korean landmarks.

## Project Goal
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_goal.jpg" title="Project Goal: Realistic Snapshots with Korean Landmarks" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
Our objective was to generate snapshot-style images that authentically reflect Korean culture by using real-world landmarks as backgrounds, moving beyond generic or repetitive settings.

## Problem Statement
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_issue.jpg" title="Problem: Limited Backgrounds and Poses" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
The existing Carat AI service was limited by monotonous backgrounds and uniform camera angles, which restricted the artistic and aesthetic quality of generated images. To overcome these limitations, we aimed to collect a diverse dataset and develop a system capable of producing snapshots that appear as if they were taken on location in Korea.

## Challenges Faced
- Ensuring consistent background generation
- Accurately reflecting camera angles and poses (prompt engineering required)

## Data Collection Process
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_data_collection.jpg" title="Data Collection: Diverse Angles and Backgrounds" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
We collected a large number of background images from the same locations and angles. This dataset was carefully curated to maximize diversity in both background and composition, enabling the model to learn realistic scene context and camera perspectives.

## Solution Approach
We fine-tuned a Stable Diffusion model using LoRA, incorporating both background and pose information into the prompts. By aligning textual descriptions with image data, we enabled the model to generate images with accurate camera angles and subject poses, closely matching real-world photography styles.

## Results: Before and After Fine-Tuning
<div class="row">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_before.jpg" title="Before Fine-Tuning" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_after.jpg" title="After Fine-Tuning (1)" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/carat_ai_after2.jpg" title="After Fine-Tuning (2)" class="img-fluid rounded z-depth-1" %}
  </div>
</div>

- **Camera angle and pose generation improved significantly after fine-tuning.**
- The model was especially successful in generating upper-body and thigh-up shots, closely matching the intended photographic style.
- Further discussion is ongoing regarding methods to maintain background consistency.

## My Role
- Dataset collection and preprocessing
- Model fine-tuning (LoRA on Stable Diffusion)
- Prompt engineering
- Academic research and literature review

## Key Takeaways & Growth
Through this project, I gained hands-on experience with industrial applications of AI, particularly in generative modeling and prompt engineering. I developed skills in problem diagnosis, ideation, and solution design, bridging the gap between academic research and real-world deployment. This experience has strengthened my ability to deliver practical AI solutions in both academic and industry settings.
