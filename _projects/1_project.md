---
layout: page
title: StoryWeaver Text-to-Image generative model for cartoonists
description: A Text-to-Image model that generates storyboard-style images from scripts for webtoon artists, presented at YBIGTA conference
img: assets/img/12.jpg
importance: 1
category: work
related_publications: true
---

{% raw %}
{% include github_card.liquid repo="YBIGTA/24th-conference-text2storyboard" %}
{% endraw %}


## Project Overview

StoryWeaver is an innovative Text-to-Image generative model designed specifically for webtoon artists. The system takes a script as input and generates storyboard-style images, providing a powerful tool for visual storytelling in the digital comics industry.

## Key Features

- **Script-to-Storyboard Conversion**: Transforms written scripts into visual storyboard layouts
- **Webtoon-Optimized Output**: Generates images specifically tailored for webtoon format and style
- **AI-Powered Generation**: Utilizes advanced text-to-image generation techniques
- **Artist-Friendly Interface**: Designed with webtoon artists' workflow in mind

## Conference Presentation

This project was presented at the **YBIGTA Conference**, hosted by Yonsei University's Big Data Academic Club. The presentation showcased the technical implementation and potential applications of the StoryWeaver model in the webtoon industry.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/1.jpg" title="StoryWeaver Model Architecture" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/3.jpg" title="Generated Storyboard Example" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="Webtoon Application" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Left: Model architecture overview. Middle: Example of generated storyboard from script input. Right: Application in webtoon creation workflow.
</div>

## Technical Implementation

The StoryWeaver model leverages state-of-the-art text-to-image generation techniques, specifically optimized for storyboard-style output. The system processes natural language scripts and generates corresponding visual representations that maintain narrative coherence and artistic style consistency.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="Model Performance Metrics" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Performance evaluation showing the model's effectiveness in generating storyboard-style images from text inputs.
</div>

## Impact and Applications

This project addresses a significant need in the webtoon industry, where artists often spend considerable time converting scripts into visual storyboards. By automating this process, StoryWeaver can:

- **Accelerate Production**: Reduce the time needed for storyboard creation
- **Enhance Creativity**: Allow artists to focus on artistic refinement rather than basic layout
- **Improve Consistency**: Maintain visual style consistency across episodes
- **Support Collaboration**: Facilitate better communication between writers and artists

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/6.jpg" title="Workflow Integration" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/11.jpg" title="User Interface" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Integration of StoryWeaver into the webtoon creation workflow and the user-friendly interface designed for artists.
</div>

## Future Development

The project continues to evolve with plans for:
- Enhanced style customization options
- Multi-panel generation capabilities
- Integration with popular webtoon creation tools
- Real-time collaboration features

This work represents a significant step forward in bridging the gap between textual storytelling and visual art creation, particularly in the rapidly growing webtoon industry.
