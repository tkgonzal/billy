# Billy 
A backlog manager for tracking user progress of media consumption and collection. 

## Usage
You can launch the app using the ***billy_gui.pyw*** file.

From the **File** tab:
* Use the **New** option to create new *Shelf* from which you (and possibly other users) can keep track of collections of different *Media List*s.
* Use the **Load** option to load a previously made *Shelf* object. (*Shelf* objects are loaded from an app generated *SAV* folder using File I/O)
* Use the **Save** option to save the changes you've made to your current *Shelf* (*Shelf* objects are saved to the aforementioned *SAV* folder using File I/O)

From the **Edit** tab:
* Use the **Add Media** option to create a new *Media List* on your current shelf, from which you can track media you are currently progressing through/wish to obtain and media you recently completed/obtained. 
* Use the **Add Entry** option to create a new entry on an opened *Media List*. All inputs on the entry form aside from the "Notes" category must be filled out before submitting the entry to the *Media List*.

From the **View** tab:
* Use the **Refresh** option to refresh the current UI (To be used whenever the app misses out rendering certain components, generally whenever the user has to scroll through the app)
* Use the **Back** option to return from an opened *Media List* to the *Shelf* view (which displays all of the *Media List*s on that *Shelf*)
* Use the **Sort** option to sort all of the media on an opened *Media List*

**IMPORTANT:** The app stores user created *Shelf* data in an app generated *SAV* folder. As such, it is important not to tamper with the files in the folder.

## Dev Thoughts
Made with the intent of streamlining the process of tracking my own progress in different types of media in college, and as a practice in making a, at the time, larger scale of project than I was used to in my coding classes. Considering I only had UCI's ICS 30 series under my belt and that I personally made use of the app throughout all of my college experience, I still feel somewhat proud of the app despite how rudimentary it is.

It does certainly still feel aged however, as my lack of UI/UX experience making the app feels very evident. The "backend" being managed by File I/O rather than sort of proper DB also leaves much to be desired in terms of both storage efficiency and scalability. If I would return to fleshing out this app, those would probably be the first aspects of the app I would try to overhaul.