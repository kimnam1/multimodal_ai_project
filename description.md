# Course Examination Details

## Project description (on Moodle)

The final examination for this course will be conducted as a poster session, as it provides a more interactive and collaborative experience.

During the session, you will have the opportunity to:

Present your work
View and learn from other teams' approaches and solutions
Engage in meaningful discussions about different methodologies with us and your classmates
Develop your presentation and communication skills
Experience a format commonly used in academic and industry settings
This approach allows us to evaluate not only your technical solutions but also your ability to communicate complex ideas clearly and concisely.

It also creates a valuable learning opportunity where you can gain insights from your peers' work and potentially discover alternative approaches to similar problems.

Exam Session
Location: Amphithéâtre Gay Lussac
Date: Monday, March 17th 2025
Time: 2:00 PM - 6:00 PM

Poster Requirements
Each team is required to create two posters \* (see examples below):

Poster 1
Introduction to the task
Bibliography and research setting
Proposed methodology
Poster 2
Additional methodological details (if needed)
Experimental setting
Qualitative and quantitative results
Failure cases or other interesting findings (if applicable)
Format Specifications
Size: A3 format (29.7 cm × 42 cm / 11.7 in × 16.5 in)
File Type: PDF
Examples:

In case it can help, you can find two repos here and here:, with poster examples.

If you get inspired by this, you should be careful with:
Number of columns -- 3 columns is too much for A3 (?)
Font size -- choose the font size so that it's readable for people when they are in front of it
The sections do not exactly match the guidelines written here but more or less overlap
Presentation Format
Teams should be ready to present their work within 2 minutes (short version) and 5-7 minutes (long version)
All students are encouraged to view other teams' posters
If you have visual results (especially videos), please bring your laptop/tablet
Important Deadlines
Deliverable Description Deadline
Posters Two A3 posters in PDF format Sunday, March 16th, 23:59
Report PDF format, up to ~5 pages Monday, March 24th, 23:59
Video Demo Showing results or method demonstration Monday, March 24th, 23:59
Code Complete project code Monday, March 24th, 23:59
Note: We will print the posters for you if submitted by the deadline.

You can submit your files in the "Exam deliverables" section on Moodle.

For any questions or clarifications, please contact Vicky Kalogeiton (vicky.kalogeiton@polytechnique.edu) and Xi Wang (xi.wang@lix.polytechnique.fr).
Part of this text is generated with Claude ;)

## idea

modals

• text
• image
• audio
• video
• motion
• depth / pose
• sensor data

video -> text
agent that generates most likable comments

## references

LiveBot: Generating Live Video Comments Based on Visual and Textual Contexts
https://github.com/lancopku/livebot
https://arxiv.org/abs/2409.15196

VideoIC: A Video Interactive Comments Dataset and Multimodal
https://dl.acm.org/doi/epdf/10.1145/3394171.3413890
Multitask Learning for Comments Generation

ViCo: Engaging Video Comment Generation with Human Preference Rewards
https://dl.acm.org/doi/epdf/10.1145/3696409.3700260

## Plan

### Dataset

1. Youtube-8M

URL : https://research.google.com/youtube8m/

from Youtube-8M get

- video ID
- video feature
- label / category

2. Video ID -> Youtube API

Using Video ID from youtube-8M
get

- title
- description
- comments
- comments likeCount

3. Dataset

input

- video features
- title (text)
- description (text)

output

- top-liked comment(s)
