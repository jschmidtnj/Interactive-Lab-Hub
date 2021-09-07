# Staging Interaction

In the original stage production of Peter Pan, Tinker Bell was represented by a darting light created by a small handheld mirror off-stage, reflecting a little circle of light from a powerful lamp. Tinkerbell communicates her presence through this light to the other characters. See more info [here](https://en.wikipedia.org/wiki/Tinker_Bell). 

There is no actor that plays Tinkerbell--her existence in the play comes from the interactions that the other characters have with her.

For lab this week, we draw on this and other inspirations from theatre to stage interactions with a device where the main mode of display/output for the interactive device you are designing is lighting. You will plot the interaction with a storyboard, and use your computer and a smartphone to experiment with what the interactions will look and feel like. 

_Make sure you read all the instructions and understand the whole of the laboratory activity before starting!_



## Prep

### To start the semester, you will need:
1. Set up your own Github "Lab Hub" repository to keep all you work in record by [following these instructions](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md).
2. Set up the README.md for your Hub repository (for instance, so that it has your name and points to your own Lab 1) and [learn how to](https://guides.github.com/features/mastering-markdown/) organize and post links to your submissions on your README.md so we can find them easily.
3. (extra: Learn about what exactly Git is from [here](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F).)

### For this lab, you will need:
1. Paper
2. Markers/ Pens
3. Scissors
4. Smart Phone -- The main required feature is that the phone needs to have a browser and display a webpage.
5. Computer -- We will use your computer to host a webpage which also features controls.
6. Found objects and materials -- You will have to costume your phone so that it looks like some other devices. These materials can include doll clothes, a paper lantern, a bottle, human clothes, a pillow case, etc. Be creative!

### Deliverables for this lab are: 
1. Storyboard
1. Sketches/photos of costumed device
1. Any reflections you have on the process
1. Video sketch of the prototyped interaction
1. Submit the items above in the lab1 folder of your class [Github page], either as links or uploaded files. Each group member should post their own copy of the work to their own Lab Hub, even if some of the work is the same from each person in the group.

### The Report
This README.md page in your own repository should be edited to include the work you have done (the deliverables mentioned above). Following the format below, you can delete everything but the headers and the sections between the **stars**. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in your README.md for the lab.

## Lab Overview
For this assignment, you are going to:

A) [Plan](#part-a-plan)

B) [Act out the interaction](#part-b-act-out-the-interaction) 

C) [Prototype the device](#part-c-prototype-the-device)

D) [Wizard the device](#part-d-wizard-the-device) 

E) [Costume the device](#part-e-costume-the-device)

F) [Record the interaction](#part-f-record)

Labs are due on Mondays. Make sure this page is linked to on your main class hub page.

## Part A. Plan 

To stage the interaction with your interactive device, think about:

_Setting:_ Where is this interaction happening? (e.g., a jungle, the kitchen) When is it happening?

_Players:_ Who is involved in the interaction? Who else is there? If you reflect on the design of current day interactive devices like the Amazon Alexa, it’s clear they didn’t take into account people who had roommates, or the presence of children. Think through all the people who are in the setting.

_Activity:_ What is happening between the actors?

_Goals:_ What are the goals of each player? (e.g., jumping to a tree, opening the fridge). 

The interactive device can be anything *except* a computer, a tablet computer or a smart phone, but the main way it interacts needs to be using light.

In this lab I will be making a tool for showing information about public transit options on Roosevelt Island. This tool will consist of a 3D map of the island, along with multicolored lights signifying whether the public transit option is on-time or delayed, what the best time is to leave, and if it is running at all.

- **Setting**: The map and display will be situated in the kitchen of my apartment in the House, so that I can see what the best time to leave is before I try to make the subway, tram, or ferry. It will be on all the time, but will only be used outside of class-hours, when my roommates or I need to leave.
- **Players**: The people involved include me and my roommates, or anyone else who will be inside of the apartment at a given time. Most likely there will not be any children or younger individuals in the space.
- **Activity**: The user looks at the 3D map and sees the colored LED lights. Based on the color, the user will realize whether they can make it to the public transit option or not, and if it's running on time or delayed. From there the user can make a decision of what time it is best to leave and what transit option thy should use.
- **Goals**: The goal is to provide the user the most up-to-date information on transit options so that they can make it to the subway, tram, or ferry on time.

Sketch a storyboard of the interactions you are planning. It does not need to be perfect, but must get across the behavior of the interactive device and the other characters in the scene.

\*\***Include a picture of your storyboard here**\*\*

Present your idea to the other people in your breakout room. You can just get feedback from one another or you can work together on the other parts of the lab.

Overall my group liked the idea and thought that it would be useful for them. They mentioned that light may not be the best medium to communicate this information, as you may not be looking at the map when it is the optimal time to leave to go to the public transit option. Most likely, the best implementation is having a combination of visual and auditory interaction, where users can see what the timing is for the given public transit option and hear when it is the best time to leave. They also mentioned that it might be a good idea to have a text display in addition to the LED lights, in case you forget what the colors mean, or to show the exact time the public transit option is leaving. This is a good idea if I can come up with a way to incorporate the display on the model in an intuitive way.

## Part B. Act out the Interaction

Try physically acting out the interaction you planned. For now, you can just pretend the device is doing the things you’ve scripted for it.

After acting it out, I realized that the 3D model needs to be bigger than I initially planned for in order to distinguish between the different transit options. It might work better in 3D with the objects distinguishing between the modes of transport, but I do think that it needs to be bigger. On paper I also thought that it would be useful to have a text display showing the times when the transit option is leaving on the bottom of the model. However, this would require the user to pick up the model and look on the bottom. In practice this is not as useful / intuitive as I originally thought it would be.

One new idea that we came up with after acting it out was to use the color yellow to signify that the public transit option is delayed, and red to show that it is not running at all / not an option at this time. Green means that it is possible to make it to the public transit option by the time it leaves. We also realized that it would be important to be able to configure the amount of time it takes to get to each transit option from the apartment, as some people live near the top of the House and others live towards the bottom. The elevator will take longer to transport the user to the ground floor for the people in the top-floor apartment, and alter the ability of the user to make it to the public transit option.

## Part C. Prototype the device

You will be using your smartphone as a stand-in for the device you are prototyping. You will use the browser of your smart phone to act as a “light” and use a remote control interface to remotely change the light on that device. 

Code for the "Tinkerbelle" tool, and instructions for setting up the server and your phone are [here](https://github.com/FAR-Lab/tinkerbelle).

We invented this tool for this lab! 

If you run into technical issues with this tool, you can also use a light switch, dimmer, etc. that you can can manually or remotely control.

I did not use Tinkerbelle for this lab, and am instead using passive interactions to communicate between the user and the device. No input is required besides a WiFi connection and REST api's.

## Part D. Wizard the device
Take a little time to set up the wizarding set-up that allows for someone to remotely control the device while someone acts with it. Hint: You can use Zoom to record videos, and you can pin someone’s video feed if that is the scene which you want to record. 

\*\***Include your first attempts at recording the set-up video here.**\*\*

Now, change the goal within the same setting, and update the interaction with the paper prototype. 

\*\***Show the follow-up work here.**\*\*


## Part E. Costume the device

Only now should you start worrying about what the device should look like. Develop a costume so that you can use your phone as this device.

Think about the setting of the device: is the environment a place where the device could overheat? Is water a danger? Does it need to have bright colors in an emergency setting?

\*\***Include sketches of what your device might look like here.**\*\*

\*\***What concerns or opportunities are influencing the way you've designed the device to look?**\*\*


## Part F. Record

\*\***Take a video of your prototyped interaction.**\*\*

Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

I had many influences when completing this lab, including Hayden Daly and Rohan Divate, my roommates, as well as the Maker Lab, which helped me with prototyping and design. The MQTT documentation helped greatly with prototyping and designing the model.


# Staging Interaction, Part 2 

This describes the second week's work for this lab activity.


## Prep (to be done before Lab on Wednesday)

You will be assigned three partners from another group. Go to their github pages, view their videos, and provide them with reactions, suggestions & feedback: explain to them what you saw happening in their video. Guess the scene and the goals of the character. Ask them about anything that wasn’t clear. 

\*\***Summarize feedback from your partners here.**\*\*

## Make it your own

Do last week’s assignment again, but this time: 
1) It doesn’t have to (just) use light, 
2) You can use any modality (e.g., vibration, sound) to prototype the behaviors! Again, be creative!
3) We will be grading with an emphasis on creativity. 

\*\***Document everything here. (Particularly, we would like to see the storyboard and video, although photos of the prototype are also great.)**\*\*
