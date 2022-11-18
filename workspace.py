from battlemap import Entity, Actor

e = Entity("E")
a = Actor("A")

if isinstance(a, Actor):
    print("a is an actor")
else:
    print("wait... a isn't an actor?")
if isinstance(e, Actor):
    print("e is too")
else:
    print("e is only an entity")