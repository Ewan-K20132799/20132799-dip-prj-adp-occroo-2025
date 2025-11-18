# Overview

This document showcases design documentation that will be utilised in the creation of the occroo
project.


## Persona/User Profile

[Customer Profile/Persona 1:]
      [- Name:] 
        - Adelheid Smit
      [- Age:] 
        - 20
      [- Gender:] 
        - F
      [- Advantages:]
        - Good at listening
        - Willingness to learn
        - Strong growth-mindset
        - Grit
      [- Disadvantages:]
        - Blindness
        - Poor accessibility to resources due to slow loading system in screen reader
        - Limited time due to other obligations
      [- Motivation:]
        - Achieve certifications for employment
        - Have a genuine interest in programming
        - WFH opportunities
      [- Background:]
        - A programming student
        - Got to this point by studying hard
        - Dedicated to learning about software development
        - Born in Christchurch, NZ
        - Migrated to Australia as a child (parents were seeking better employment opportunities)
        - Mothers Dutch and Other Parent is from New Zealand
        - Has been in WA for 14 years
        - Did most of primary schooling as well as secondary schooling in WA and graduated with a WACE and CertII
        - Has spent a year so far studying programming at TAFE
        - Currently studying CertIV in programming
        - Is struggling at the tail-end of the course due to a lack of accessibility features in software
        - Is stressed out due to having many tasks to do at TAFE, Work and Home
        - Is getting confused and frustrated with the content and is struggling to keep up due to how un-intuitive the video lectures are
        - Aiming to complete Diploma at the end of 2026 (also aims to complete CertIV by end of 2025)
      [- Likes:]
        - Adjacent to more niche hobbies (i.e. DnD)
        - Gaming
        - Audio books
        - Music
        - Podcasts
        - Problem Solving
      [- Dislikes:]
        - Comics
        - really any literature she can't interpret properly
        - Birds
        - Politics


  [Customer persona/profile 2:]
     [- Name:] Johan Simons
     [- Age:] 21
     [- Gender:] M
     [- Advantages:]
        - Has a strong willingness to learn
        - Has a strong mindset
     [- Disadvantages:]
        - Poor accessibility to resources due to being unable to properly save transcriptions on screen reader
        - Limited time due to work
     [- Motivation:]
        - To get his dream job of being a developer for Apple
        - To gain his university undergrad degree in Software Development from UWA
        - WFH opportunities
        - To be able to view resources while also juggling workplace responsibilites successfully
     [- Background:]
        - A student at UWA
        - Studys hard
        - Dedicated to learing about all the ins and outs of CompSci
        - Born in Edmonton, Alberta (Canada)
        - Migrated with family at age 12
        - Did primary schooling in Canada and Secondary schooling in WA
        - Has been at UWA for 2 Years
        - Intends on getting undergrad
        - Intends on going for post grad degree
        - Has been struggling in the course due to a combination of workplace commitments and accessibility issues
        - Is anxious about failing the course
        - Is confused due to the screen reader giving poor information
     [- Likes:]
        - Niche hobbies
        - Gaming
        - Music
        - Music production (as a hobby)
        - Dogs
        - Problem solving
     [- Dislikes:]
        - Literature he can't accurately interpret
        - Politics
        - Spicy food

 Customer persona/profile 3:
     [- Name:] 
        - Leon Kennedy
     [- Age:] 
        - 19
     [- Gender:] 
        - M
     [- Advantages:]
        - Committed to learning new skills
        - has a strong mindset
     [- Disadvantages:]
        - Limited resource accessibility due to not being able to copy examples from the transcription
        - Limited time due to responsibilities at home
     [- Motivation:]
        - To achieve his diploma by the end of 2026
        - To use his credits from diploma to get a degree at UWA
        - To do freelance work for smaller businesses in the CBD
        - To get eventually develop an Office suite that out performs MS365
     [- Background:]
        - A student at SMTAFE
        - Studies hard
        - Is dedicated to learning more about OpenSource development
        - Born in Perth, WA
        - Attained WACE and a CertII
        - Has been at SMTAFE for six months
        - is beggining a CertIV in programming
        - is frustrated about the difficulties he is having with learning the content
        - aiming to get a degree from university by 2029 at the latest
        - is concerned about the progress he has made so far in the course
        - Is struggling with taking care of his grandfather while also juggling study
     [- Likes:]
        - Obscure music
        - Cats
        - Gaming
        - Listening to historical audio books
        - Problem solving
     [- Dislikes:]
        - Literature that can not be easily interpreted
        - politics
        - Dogs
        - AI

Notice: This project focuses on assistive technology for people with disabilities. It is important to treat the topic with respect and sensitivity.

Consider:

- People are not defined by their disabilities.
- People with disabilities are not a homogeneous group.

Your persona should reflect the diversity of people with disabilities and their experiences.

## Ideation 

    Ideation:
           1 - Feed video through AI:
                - Depends on quality of AI
                - Depends on programmer bias
                - Quality of response can be terrible
                - Usually cost a fair amount
                - Liability due to subscription
           2 - Restore sight
               - Expensive
               - Still quite experimental
           3 - Support person
                - cost can be high
                - would be more accurate than AI
           4 - virtual support person
               - Slightly less expensive
               - can be less helpful than local supprt
               - network connectivity and timezone differences
           5 - screen reader (Chosen solution)
               - Screen readers can only read text
               - could interpret text in a video
               - could cost a lot in terms of time
               - financal cost would be small
               - can integrate AI
           6 - utilise other resources
               - could be inaccurate
               - could lack resources in the desired format
               - cost would be low
           7 - change accessibility legislation
               - Would take a lot of time

## User Journey

What is the user journey? What are the steps the user takes to achieve their goals?

    User Story 1:
              - based on user profile
              As:
                - Adelheid
              I want:
                - to load any video transcriptions with ease
              So that:
                - I can better interpret the concepts that I am being taught
                - I can successfully complete the course

    User Story 2:
             As:
               - Johan
             I want:
               - to be able to save video transcriptions for future use
             So that:
               - I can deepen my hobby in software development
               - Achieve my dream job of working at Apple

    User Story 2 steps:
             1. Open application
             2. Select video via drop down menu entered by using keybind 
             3. Select transcribe gui button via clicking on it or via keybind
             4. Select save video gui button to save video via clicking on it or via a keybind

    User Story 3:
            As:
               - Leon
            I want:
              - To be able to copy and edit examples from transcription
            So that:
              - I can deepen my knowledge in software development
              - I deepen knowledge in OpenSource development
              - I can get degrees from TAFE and University

## UI Interaction Patterns (Wireframes)

What are the UI interaction patterns you will use in your project?
![Alt text](/design/resources/ADP_WireFrame.jpg "Image of Wireframe")

## AI Prompts

Write down any AI prompts you came up with after your first session

what would the code behind a python application for a ocr video screen reader look like?
What is the issue with this code: