### [Example site](https://plotree.aramieewen.repl.co/)
### [Example server](https://replit.com/@ARAMIEEWEN/plotreeserver#main.py)

## **Plotree: a module to help manage making a choose your own adventure game**
- Produces a json from the tabbing of a .txt file
    - Note: Tabbing and prefixes aren't cleaned, but you can clean with the clean_plotree method!

## **Dependencies:**
- copy.deepcopy

## **Usage example:**
```py
from plotree import plotree

with open('a_story.txt', 'r') as f:
    story = f.readlines()
branchy_story = plotree(text=story, opt_prefix="#")
clean = branchy_story.clean_plotree()
```
This returns a "jsonable" structure (i.e., a python dictionary) following the format:

```
{
    "plot" : "This is the first line in your .txt file",
    "opts" : [
        {
            "opt" : "This action was marked with the prefix #",
            "opt_to" : {
                "plot" : "The prefix and tabbing was removed by clean_plotree",
                "opts" : [
                    // Another nested option listing
                ]
            },
        },
        {
            "opt" : "# Only the first # was removed, but this is an opt",
            "opt_to" : {
                "plot" : "The story could continue along this branch",
                "opts" : [] // When there is no story left
            },
        },
    ]
}
```

The .txt file to produce this would look like:
```
This is the first line in your .txt file
    # This action was marked with the prefix #
        The prefix and tabbing was removed by clean_plotree
    # # Only the first # was removed, but this is an opt
        The story could continue along this branch
```
