# Spaced Repetition Python Script

## Motivation

Software such as Anki uses a spaced repetition algorithm that is optimized for handling a large number of questions that do not require significant time to complete. 
As a software developer, I generally have to solve problems that take over 20 minutes to complete (e.g. DS/A questions).
Thus, I found software similar to Anki excessive and I only needed a method to automate the process of getting questions I wanted to consolidate using spaced repetition theory. 

## How to use

1. `docker image build -t [your tag] .`

2. `docker container run --rm [your tag]`

The Google spreadsheet I use have two important pieces of information:

1. A flag that decides whether I want to keep the question in my question bank.
2. The number of times I’ve repeated the question.

I believe this method works for me and is the best solution to improving my long term problem solving skills.
