# getterGen - rudimentary Generator

This so called application is basically a testament to my unability to find something that does this. The purpose is so basic that someone else surely wrote this already. A thousand times over, but i couldnt find something simple. Really, i thought i was good at google.

## What does it do?

It just generates some generic getter & setter for when you first set up a python data class. The most basic stuff that is always the same:
```python
@property
def name(self):
    return self._name

@name.setter
def name(self, name: str):
    self._name = name
```
Super basic, there are generators for that. I also do some "fancy" checks and offer the option for including a basic type check but apart from that, this does not nothing intelligent.

## Usage

Start the thing and then type space seperated pairs of `name` `type` which are then the the things that get entered in the blocks. If you are done just send an empty line or `/q`, if you miss typed something you can always just overwrite it

### Special commands

While typing there are some special flags, all starting with a slash:
* `/q` quiting the application without copying
* `/f` finishing input, same as submitting an empty line
* `/del {name}` deletes the entry with that exact name
* `/c` changing check mode status (adds an `isinstance()` to the code)
* `/s` immediately copies current pairs as code to the clipboard