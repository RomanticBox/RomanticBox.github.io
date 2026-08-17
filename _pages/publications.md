---
layout: page
permalink: /publications/
title: publications
description: publications by categories in reversed chronological order.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<div class="mb-3 d-flex flex-wrap align-items-center" style="gap: 0.5rem">
  <a href="https://scholar.google.com/citations?user={{ site.data.socials.scholar_userid }}&hl=en" target="_blank" class="btn btn-outline-primary btn-sm">
    <i class="ai ai-google-scholar"></i> View on Google Scholar
  </a>
  <span class="ml-md-3">Sort by:</span>
  <button type="button" class="btn btn-primary active btn-sm" data-pub-sort="year">Year</button>
  <button type="button" class="btn btn-outline-primary btn-sm" data-pub-sort="alphabetical">Alphabetical</button>
  <button type="button" class="btn btn-outline-primary btn-sm" data-pub-sort="author-position">Author Position</button>
  <button type="button" class="btn btn-outline-primary btn-sm" data-pub-sort="venue">Venue</button>
</div>

<script defer src="{{ '/assets/js/pub-sort.js' | relative_url | bust_file_cache }}" type="module"></script>

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

{% bibliography %}

</div>
