# Poyml

Poyml is a document processing system for free-verse poetry. 

## Why

My editing process needed more structure and I wanted to track and archive individual poems as well as collections of poems submitted to various journals. I started readying about yaml and things snowballed from there.

The goal is to make editing faster, with automation at specific points. 

## Usage

Poyml has three main functions:

- Serialize poem txt file into the poyml format
- Extract information from serialized poyml poems
- Build collections of poems via Pandoc

This markup / serialization uses yaml for ease of preserving formatting; for single files, the "body" block should use the "literal block" in yaml. the poyml script for single files  essentially just serializes the poem with metadata. 


```yaml
# file: houses.yaml
title: houses
date: !!timestamp 2023-03-02
body: |
  burned and cherished
  and filled with doubt
  and ended by a vision.

  the beginning and the end
    and the same, every step forward
    making room for the treatment
    of an unknown number of betweens.
comments: |
  this is part of a poem called houses being used as an example
  for this poetry serialization / markup / etc thing. 
```

Poyml can generate yaml formatted argument docuement to be used with Pandoc. This document should specify the files to include in the final collection and be directly runnable with something similar to `pandoc --defaults="collection.yaml" -i file.md`.


Below is a sample pandoc file. The poyml script currently does not handle this yaml generation - title, includes and output file name should be script args. TBD

```yaml
# file: collection.yaml
standalone: true
css: "../pandoc/style.css"
from: commonmark_x
to: pdf
pdf-engine: wkhtmltopdf
title: "Adroit Submission 3/1/2023"
include-after-body:
  - interstate.md
  - push.md
  - to_be_new.md
  - wooded_land.md
  - you_are_going_to_be_here.md
output-file: adroit.pdf
```
