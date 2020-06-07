# open.Entex
Computer vision web app developed for HackNortheast

## Inspiration
As a business owner, do you ever wonder how many people actually pass by the promotional sign you left outside your store? Or consider what might be the most profitable store hours for you to stay open?  With the menacing threat of COVID-19, what if you could provide your customers with the comfort of knowing that your store won’t be crowded at the time they arrive? Imagine being able to count the people entering and leaving your store without needing to hire a human to do so!
As retail struggles to reopen in the wake of the COVID-19 shutdown, we designed open.ENTEX to help answer the aforementioned issues that businesses might be struggling with. Our goal is to provide small business owners with a tool that allows them to gather additional data for analysis and help optimize their businesses during these trying times.

## What it does
open.ENTEX is a deployable computer vision application that analyzes camera footage to track people and their movement within the video frame. It is able to identify how many people walk by in each direction and count people entering and exiting a building. This data is then pushed to the cloud and can be viewed through the open.ENTEX-Web, our Svelte based Web-App.
Both business owners and customers benefit from open.ENTEX! Business owners could use our software to identify peak hours, potential sales, and marketing opportunities. Furthermore, during COVID-19 open.ENTEX can ensure that retail is adhering to guidelines and provide help with monitoring available capacity. Users can utilize the open.ENTEX web-tool to view the current number of people in a store and browse historical traffic data, helping them avoid crowds and rush hours.

## How we built it & how it works
The open.ENTEX pipeline consists of three principal components: our custom Computer Vision algorithm, a Cloud Firestore, and a Svelte based Web App. 

### The Computer Vision Algorithm:
Using Python and OpenCV, our program processes a video feed and recreates a static background image using a technique called background subtraction. This allows our program to separate moving pixels from static ones and create a background image. The result is a generated foreground mask that filters the active pixels, leaving a predominantly black image with select white pixels to represent movement.
Next, we filter the foreground mask again and highlight subsections that pass a high enough threshold. However, the video still has excess noise due to the motion of shadows or changes in lighting. To resolve this, we implemented the number of islands strategy to detect large clumps of nearby neighboring highlighted pixels. This allows the algorithm to remove any loose pixels that were originally detected and isolate moving people. This data is then used to calculate the current location of each person and track their velocity. Using this information, we can determine whether a person was entering or exiting the frame. Finally, the data points are pushed to the cloud.

### The Database:
Every time a person is detected walking in or out of the store, an update call is made to the database in Firebase. The database is sorted into collections and documents; each unique store is a document and has a collection of data points indicating the number of people in the store with a timestamp.

### The Web App:
As we aimed to learn new technology, we decided to build our Web App using Svelte, an open-source JavaScript framework. When a user arrives at open.ENTEX-Web they are prompted to pick from the selection of store deployments. The data is visualized in three ways:
*A store headcount
* An “available capacity percentage bar” 
* A graph showing past and current data in relation to time 
Data is loaded in parallel to all these components to increase speed for the user.

## Challenges we ran into and what we learned
When developing the CV algorithm, our biggest challenge was identifying clumps of movement and tagging them as unique objects. We struggled to track these people over a series of frames, especially when an object disappeared only to reappear a few frames later. We were able to solve this by looking to see if any objects existed in past frames in a similar spot before disappearing and measuring the Pythagorean distance to decipher if it could be a realistic guess.
The main front-end difficulty was populating asynchronous data into the DOM of the Web App. We used Svelte, a newer alternative to Shadow-DOM based frameworks like React and Vue. However, none of our team had prior experience with Svelte-based data visualization. Being a newer framework, there are not nearly as many community-made and open-source imports. In the end, we decided to prioritize making a visually appealing and easy to use front-end instead of focusing on live updates. This would be an important feature to implement in open.ENTEX-V2.

## Accomplishments that we’re proud of
First off, two of us are extremely proud of completing our first hackathon. Taking any compelling idea and compiling it into working software is always remarkably gratifying, and doing so in just under thirty-six hours is quite the achievement for any team. However, we are pleased that our project has many practical applications for both consumers and retailers. We hope that it can be used by the local community, and if it can have any impact during these troubling times, nothing would make us prouder.

## What's next for open.ENTEX
There is only so much we could accomplish in thirty-six hours. In the future, we aim to improve both the computer vision and the user interface. While the CV is accurate most of the time, there are still a few edge cases in which it is slightly inaccurate, occasionally missing a person when people are too close to each other or are passing behind another object. The UI shows the data well and is easy to use. However, we lacked the time to add anything other than basic functionally.
From a business perspective, our next step would be to gauge interest with nearby retailers. This means coordinating test runs at the local supermarket and identifying the next steps before deployment.
