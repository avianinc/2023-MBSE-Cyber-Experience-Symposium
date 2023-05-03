The point here is to build models that inform rather than describe. Additionally, the items that are being informed should inform the model and help define its shape and content. Finally the some systems engineering teams do not understand the need for middleware to link the systems models to the informed simulation and analytical models. Its important to take into account the complexity of this middleware which is typically shown as a arrow on a diagram.

The sysml model should be created to both describe and inform. Inform simulation and analysis.
The sysml model is in the treeview not in the diagrams. The diagrams are views of the model. 
The middleware is usually denoted as an arrow :(... not that easy

Mission Critical Information --> Inform

Creating Mission Models using SysML and Cameo Systems Modeler

Im writing a presentation for a conference on the subject of mission modeling using cameo systems modeler. Im looking to describe the following [
1. Start with a talk about how a sysml model is more than just a set of diagrams. It actually consists of the items in the containment tree and the diagrams are really just views of the model.
2. When we build systems models we must create clear purpose, objectives, goals, and scope. What is the model going to do? It typically 'informs', it informs documentation, it informs simulation models, it informs simulation models, etc. 
3. But just as importantly the systems model is informed by all of the models it must inform. Building a mission model in a vacuum will result in a malformed model, a model that does not have the right shape or form and does not have the right information to inform. 
4. Then I want to discuss how to think about a model. What should it look like or what for should it take. For a mission model we typically receive a mission outline from a SME in powerpoint for textual form. We then decompse the nouns and the verbs into structure and function in a sysml model. But what do we want to do with this model. Do we want to define a mission? Do we want to be able to define many missions? Do we want to simulatie and analuyze these missions? Of course Yes...
5. If we want to do all of these things then what should the model look like. What information does the model need to be able to inform. What is it informing?
6. Lets take a step back and recall that the model in the treeview and not the canvas or diagrams. It similar to the way we work in typical enginering tools where we can build a model by right clicking in the treeview and adding a aircraft, right click the aircraft and add a sensor or a weapon, add a set of waypoint to the aircraft maybe, and lots of information. This model in the treeview is essentially an instance. Doing it this way makes it each to create many instances quickly using the tool. Im not considering the statiscial nature of the model at this time.
7. Now how do we use these instances to inform? Well there are several ways one is to export the model as xml and interrogate, or maybe we use the teamwork cloud api. I prefer the api method becasue one its easy to get started without having to use csm in the loop and the other is that it fits into my sysmlv2 plans as it comes with an API right out of the box. Note that there is an issue with the link between the concrete code and working from the json side of the model. Not sure where this is at for now... but its a real issue. 
8. Now lets demo builing a simple mission model. The model should include a sceanrio, vingette, packages, and performers. I'll do this my way and just use performers then back up and add an aircraft, sensor, and weapon. Maybe I work on the remote medical support system and do a rmss, hospital, drone, medicine, and comms.
8. Now create an instance table and create an instances of the drones, hosiptals, and medicine.
9. Then open the middleware and pull the instance from the model though the api. Spend some time investigating the interface and the data. Update an attribute and discuss the fact that we can pretty much do anything we like though the api. Like have vendors send models, update models, delete models, any CRUD operations they or we like. 
10. Then export the json file and pop upen natlogo and read in the data. I can update the instance and then show that netlogo can be reset with the new configuration.
11. Summarize the presentation and ask for any questions.

]


**Title:** Mission Modeling with Cameo Systems Modeler: Informed Models for Effective Decision Making

**Slide 1: Introduction**
- Introduce the topic of mission modeling using Cameo Systems Modeler
- Outline the presentation agenda

**Slide 2: SysML Models and Containment Trees**
- Explain that a SysML model is more than just diagrams
- Emphasize the importance of the containment tree, where diagrams are just views of the model

**Slide 3: Defining Purpose, Objectives, Goals, and Scope**
- Stress the need for clear purpose, objectives, goals, and scope
- Discuss how models inform documentation, simulation models, and other processes

**Slide 4: Informed Models**
- Explain the importance of building models that are informed by other models to avoid creating malformed models

**Slide 5: Thinking About Model Structure**
- Discuss how to approach creating mission models, decomposing nouns and verbs into structure and function in SysML
- Emphasize the desired outcomes, such as defining missions, analyzing, and simulating

**Slide 6: Model Information and Informed Outputs**
- Address the structure of the model and the information it needs to inform other processes

**Slide 7: Treeview and Model Instances**
- Highlight the relationship between the treeview and model instances
- Explain the benefits of using treeview to create multiple instances quickly

**Slide 8: Using Instances to Inform**
- Discuss different ways to export models (XML, Teamwork Cloud API)
- Explain the benefits of using the API and its compatibility with SysMLv2

**Slide 9: Demo - Building a Simple Mission Model**
- Demonstrate building a mission model with scenario, vignette, packages, and performers
- Use a remote medical support system as an example

**Slide 10: Creating Instance Tables**
- Show how to create instance tables for drones, hospitals, and medicine

**Slide 11: Middleware and API**
- Demonstrate accessing instances through the API and updating attributes
- Discuss the flexibility and CRUD operations the API offers

**Slide 12: Netlogo Integration**
- Export the JSON file and demonstrate integration with Netlogo
- Show how updating the instance affects the Netlogo simulation

**Slide 13: Summary and Q&A**
- Summarize the key points of the presentation
- Invite questions and open the floor for discussion

This outline covers the main points you wanted to include in your presentation. Adapt and expand on the slides as necessary to provide the desired level of detail and address the specific needs of your audience.

I want to see the Navy devlope this type of skill internally atleast at a cursury level so that they can be more informed when working wiht vendors.