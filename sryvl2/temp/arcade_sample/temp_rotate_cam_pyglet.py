import pyglet
from pyglet.gl.gl_compat import glTranslatef
from pyglet.window import key


window = pyglet.window.Window(height=1000, width=1000)

def movement(keys):
    if keys[key.I]:
        glTranslatef(0, 10, 0)
    if keys[key.K]:
        glTranslatef(0, -10, 0)
    if keys[key.J]:
        glTranslatef(-10, 0, 0)
    if keys[key.L]:
        glTranslatef(10, 0, 0)


@window.event()
def on_key_press(symbol, modifiers):
    print(symbol)
    print(modifiers)
    glTranslatef(0.0, 10.0, 0.0)


def update(dt):
    window.clear()
    label.draw()


if __name__ == '__main__':
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    label = pyglet.text.Label('Hello, world',
                              font_size=36,
                              x=window.width // 2, y=window.height // 2)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()
